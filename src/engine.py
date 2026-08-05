"""
engine.py

The scoring core of the Account Intelligence Engine.

What it does, end to end:
  1. Loads the three data layers (objective layer, vendor catalog, patterns).
  2. Reads a company profile: the objectives the company has stated in its
     public filings, each with an emphasis and a value signal the analyst
     recorded while reading those filings.
  3. Builds candidate use cases by matching vendor solutions to the company's
     stated objectives through shared IDs.
  4. Scores each use case on the four-part rubric, keeping the per-dimension
     breakdown so nothing is a black box.
  5. Sequences the use cases into a crawl, walk, run roadmap, proving
     governance first in regulated industries.
  6. Returns a structured result the renderer turns into a readout.

The scoring is deterministic. Given the same data and profile, it produces the
same result every time. The knobs live in CONFIG below so the rubric is visible
and tunable, which is what the README means by a configurable rubric.

No real company, client, or vendor appears anywhere in this engine.
"""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


# ----------------------------------------------------------------------------
# CONFIG: every scoring knob in one visible place.
# ----------------------------------------------------------------------------

CONFIG = {
    # The rubric. These four weights sum to 1.0.
    "weights": {
        "strategic_alignment": 0.35,
        "value_at_stake": 0.30,
        "time_to_value": 0.20,
        "evidence_strength": 0.15,
    },
    # How quickly and realistically each solution can be stood up, from 0 to 1.
    # Foundational, contained solutions score higher. Documented here for
    # transparency; a future version could move this into the vendor catalog.
    "feasibility": {
        "meridian-govern": 0.90,
        "meridian-analytics": 0.80,
        "meridian-content": 0.70,
        "meridian-concierge": 0.65,
        "meridian-profile": 0.60,
        "meridian-journeys": 0.50,
    },
    "feasibility_default": 0.60,
    # Industries where governance must be proven before growth scales.
    "regulated_industries": [
        "retail-banking", "insurance", "wealth-management",
        "healthcare-payer", "healthcare-provider",
    ],
    "compliance_objectives": ["risk-compliance", "safety-compliance"],
    # Readiness shaping for the roadmap sequence (not the rubric score).
    "regulated_governance_bonus": 0.15,   # prove-first: governance earns an earlier slot
    "dependency_penalty": 0.10,           # solutions that depend on a unified profile land later
    "high_dependency_solutions": ["meridian-journeys"],
    # Evidence strength is capped because catalog proof points are illustrative.
    # This encodes the no-overclaiming discipline directly into the math.
    "evidence_base": 0.30,
    "evidence_per_proof_point": 0.10,
    "evidence_per_differentiator": 0.05,
    "evidence_governance_bonus": 0.05,    # governance claims are more concrete
    "evidence_cap": 0.70,
}


# ----------------------------------------------------------------------------
# Data structures
# ----------------------------------------------------------------------------

@dataclass
class UseCase:
    solution_id: str
    solution_name: str
    primary_objective_id: str
    primary_objective_name: str
    also_supports: list = field(default_factory=list)  # other stated objectives this solution addresses
    scores: dict = field(default_factory=dict)          # per-dimension, 0 to 1
    weighted_total: float = 0.0
    readiness: float = 0.0
    phase: str = ""
    rationale: str = ""


# ----------------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------------

def load_data(data_dir: Path = DATA_DIR):
    with open(data_dir / "objective_layer.json") as f:
        objectives = json.load(f)
    with open(data_dir / "vendor_catalog.json") as f:
        catalog = json.load(f)
    with open(data_dir / "use_case_patterns.json") as f:
        patterns = json.load(f)
    return objectives, catalog, patterns


def _objective_index(objectives):
    """Map (industry_id, objective_id) -> objective name, and industry_id -> industry dict."""
    obj_names = {}
    industries = {}
    for ind in objectives["industries"]:
        industries[ind["id"]] = ind
        for o in ind["business_objectives"]:
            obj_names[(ind["id"], o["id"])] = o["name"]
    return obj_names, industries


# ----------------------------------------------------------------------------
# Scoring
# ----------------------------------------------------------------------------

def _clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def _evidence_strength(solution):
    c = CONFIG
    score = c["evidence_base"]
    score += c["evidence_per_proof_point"] * len(solution.get("proof_points", []))
    score += c["evidence_per_differentiator"] * len(solution.get("differentiators", []))
    if "guardrail" in solution:
        score += c["evidence_governance_bonus"]
    return round(_clamp(score, 0.0, c["evidence_cap"]), 3)


def score_company(profile, objectives, catalog, patterns):
    obj_names, industries = _objective_index(objectives)
    industry_id = profile["company"]["industry_id"]
    weights = CONFIG["weights"]

    # Index the company's stated objectives.
    stated = {s["objective_id"]: s for s in profile["stated_objectives"]}
    stated_ids = set(stated)

    use_cases = []
    for sol in catalog["solutions"]:
        # Which of this company's stated objectives does the solution address?
        addressed = [
            m["objective_id"] for m in sol["maps_to_objectives"]
            if m["industry_id"] == industry_id and m["objective_id"] in stated_ids
        ]
        if not addressed:
            continue

        # Primary objective: the addressed objective the company emphasizes most,
        # tie-broken by value signal.
        def rank_key(oid):
            s = stated[oid]
            return (s.get("emphasis", 0.5), s.get("value_signal", 0.5))
        primary = max(addressed, key=rank_key)
        p = stated[primary]

        # Rubric dimensions, each 0 to 1.
        alignment = round(_clamp(p.get("emphasis", 0.5)), 3)
        breadth = len(addressed)
        value = round(_clamp(p.get("value_signal", 0.5) + 0.05 * (breadth - 1)), 3)
        feasibility = CONFIG["feasibility"].get(sol["id"], CONFIG["feasibility_default"])
        evidence = _evidence_strength(sol)

        total = round(
            weights["strategic_alignment"] * alignment
            + weights["value_at_stake"] * value
            + weights["time_to_value"] * feasibility
            + weights["evidence_strength"] * evidence,
            4,
        )

        # Readiness shapes the roadmap sequence, separate from the rubric score.
        readiness = feasibility
        serves_compliance = any(o in CONFIG["compliance_objectives"] for o in addressed)
        if industry_id in CONFIG["regulated_industries"] and (serves_compliance or "guardrail" in sol):
            readiness += CONFIG["regulated_governance_bonus"]
        if sol["id"] in CONFIG["high_dependency_solutions"]:
            readiness -= CONFIG["dependency_penalty"]
        readiness = round(readiness, 3)

        also = [obj_names[(industry_id, o)] for o in addressed if o != primary]
        uc = UseCase(
            solution_id=sol["id"],
            solution_name=sol["name"],
            primary_objective_id=primary,
            primary_objective_name=obj_names[(industry_id, primary)],
            also_supports=also,
            scores={
                "strategic_alignment": alignment,
                "value_at_stake": value,
                "time_to_value": feasibility,
                "evidence_strength": evidence,
            },
            weighted_total=total,
            readiness=readiness,
            rationale=_rationale(sol, obj_names[(industry_id, primary)], also),
        )
        use_cases.append(uc)

    # Rank by rubric score (what matters most).
    ranked = sorted(use_cases, key=lambda u: u.weighted_total, reverse=True)

    # Sequence by readiness (what to do first), split into three phases.
    sequenced = sorted(use_cases, key=lambda u: u.readiness, reverse=True)
    _assign_phases(sequenced)

    # Attach the value pattern for this industry, if one exists.
    pattern = next(
        (vp for vp in patterns["value_patterns"] if industry_id in vp["applies_to_industries"]),
        None,
    )

    # Execution challenges relevant to the solutions in play.
    in_play = {u.solution_id for u in use_cases}
    challenges = [
        c for c in patterns["execution_challenges"]
        if set(c["mitigated_by_solutions"]) & in_play
    ]

    tensions = industries[industry_id]["strategic_tensions"]

    # Echo the stated objectives back, with display names, so downstream
    # renderers can show what the company told the market it cares about.
    stated_echo = [
        {**s, "objective_name": obj_names.get((industry_id, s["objective_id"]), s["objective_id"])}
        for s in profile["stated_objectives"]
    ]

    return {
        "company": profile["company"],
        "config_weights": weights,
        "stated_objectives": stated_echo,
        "ranked_use_cases": [asdict(u) for u in ranked],
        "roadmap": {
            "crawl": [asdict(u) for u in sequenced if u.phase == "crawl"],
            "walk": [asdict(u) for u in sequenced if u.phase == "walk"],
            "run": [asdict(u) for u in sequenced if u.phase == "run"],
        },
        "value_pattern": pattern,
        "execution_challenges": challenges,
        "strategic_tensions": tensions,
    }


def _assign_phases(sequenced):
    """Split readiness-sorted use cases into crawl, walk, run by thirds."""
    n = len(sequenced)
    if n == 0:
        return
    third = max(1, round(n / 3))
    for i, uc in enumerate(sequenced):
        if i < third:
            uc.phase = "crawl"
        elif i < 2 * third:
            uc.phase = "walk"
        else:
            uc.phase = "run"


def _rationale(solution, primary_name, also):
    base = f"{solution['name']} addresses {primary_name}"
    if also:
        base += f", and also supports {', '.join(also)}"
    base += "."
    return base


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run the Account Intelligence Engine on a company profile.")
    parser.add_argument("--company", required=True, help="Path to a company profile JSON.")
    parser.add_argument("--out-json", help="Optional path to write the structured result JSON.")
    parser.add_argument("--out-readout", help="Optional path to write the rendered markdown readout.")
    parser.add_argument("--out-deck", help="Optional path to write a meeting-ready .pptx deck.")
    args = parser.parse_args()

    objectives, catalog, patterns = load_data()
    with open(args.company) as f:
        profile = json.load(f)

    result = score_company(profile, objectives, catalog, patterns)

    print(f"Company: {result['company']['name']}")
    print(f"Ranked use cases: {len(result['ranked_use_cases'])}")
    for u in result["ranked_use_cases"]:
        print(f"  {u['weighted_total']:.3f}  {u['solution_name']} -> {u['primary_objective_name']}")
    print("Roadmap:")
    for phase in ("crawl", "walk", "run"):
        names = [u["solution_name"] for u in result["roadmap"][phase]]
        print(f"  {phase}: {', '.join(names)}")

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"Wrote {args.out_json}")

    if args.out_readout:
        from render_readout import render
        Path(args.out_readout).write_text(render(result))
        print(f"Wrote {args.out_readout}")

    if args.out_deck:
        from render_deck import build_deck
        build_deck(result, args.out_deck)
        print(f"Wrote {args.out_deck}")


if __name__ == "__main__":
    main()
