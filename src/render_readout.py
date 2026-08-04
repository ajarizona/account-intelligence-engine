"""
render_readout.py

Turns an engine result (from engine.score_company) into a markdown readout.

The rendering is templated but written in a consistent register: outcome first,
collaborative, organized on the crawl, walk, run spine, no em dashes. It is the
machine-generated cousin of the hand-written example in the same folder. The
hand-written one shows the ideal; this one shows the engine producing the same
shape automatically from data.
"""


def _fmt_scores(s):
    return (
        f"alignment {s['strategic_alignment']:.2f}, "
        f"value {s['value_at_stake']:.2f}, "
        f"feasibility {s['time_to_value']:.2f}, "
        f"evidence {s['evidence_strength']:.2f}"
    )


def render(result):
    c = result["company"]
    lines = []

    lines.append("# Generated Readout: Account Intelligence Engine")
    lines.append("")
    lines.append(f"*{c['name']}, generated automatically from the company profile*")
    lines.append("")
    if c.get("fictional"):
        lines.append("> This company is fictional and the figures are synthetic. The vendor,")
        lines.append("> Meridian Experience Cloud, is also fictional. This file is produced by")
        lines.append("> `engine.py` from a company profile, to show the engine running.")
        lines.append("")

    # Company brief
    lines.append("## The company, in brief")
    lines.append("")
    lines.append(c.get("profile", ""))
    lines.append("")

    # Thesis from the value pattern
    vp = result.get("value_pattern")
    if vp:
        lines.append("## The thesis")
        lines.append("")
        lines.append(vp["thesis"])
        lines.append("")
        lines.append("What makes this fit here:")
        lines.append("")
        for pr in vp["principles"]:
            lines.append(f"- {pr}")
        lines.append("")

    # Ranked use cases
    lines.append("## Ranked use cases")
    lines.append("")
    lines.append("Scored on the rubric: strategic alignment 0.35, value at stake 0.30, time")
    lines.append("to value and feasibility 0.20, evidence strength 0.15. Every score shows")
    lines.append("its breakdown so the ranking is auditable.")
    lines.append("")
    for i, u in enumerate(result["ranked_use_cases"], 1):
        lines.append(f"**{i}. {u['solution_name']} for {u['primary_objective_name']}** "
                     f"(score {u['weighted_total']:.3f})")
        lines.append("")
        lines.append(f"{u['rationale']}")
        lines.append("")
        lines.append(f"Score breakdown: {_fmt_scores(u['scores'])}.")
        lines.append("")

    # Roadmap
    lines.append("## The roadmap: crawl, walk, run")
    lines.append("")
    lines.append("Ranked by rubric score, sequenced by readiness. The highest-value work is")
    lines.append("not always first to do. In a regulated setting we prove governance before")
    lines.append("growth scales.")
    lines.append("")
    phase_intro = {
        "crawl": "Start where the risk is lowest and the audit story is cleanest.",
        "walk": "Extend into service and personalization once the foundation holds.",
        "run": "Turn on the growth engine on a foundation the risk side already trusts.",
    }
    for phase in ("crawl", "walk", "run"):
        items = result["roadmap"][phase]
        if not items:
            continue
        lines.append(f"### {phase.capitalize()}")
        lines.append("")
        lines.append(phase_intro[phase])
        lines.append("")
        for u in items:
            supports = ""
            if u["also_supports"]:
                supports = f" It also supports {', '.join(u['also_supports'])}."
            lines.append(f"- **{u['solution_name']}**, serving {u['primary_objective_name']}.{supports}")
        lines.append("")

    # Execution challenges
    challenges = result.get("execution_challenges", [])
    if challenges:
        lines.append("## What execution actually takes")
        lines.append("")
        lines.append("A readout that only sells the upside is not honest. Here are the "
                     "challenges to expect, and what addresses each.")
        lines.append("")
        for ch in challenges:
            lines.append(f"**{ch['name']}.** {ch['description']}")
            lines.append("")

    # Strategic tensions as caution
    tensions = result.get("strategic_tensions", [])
    if tensions:
        lines.append("## Tensions to hold")
        lines.append("")
        lines.append("These are the trade-offs in this industry. We sequence the roadmap so a "
                     "use case does not win one objective while quietly damaging another.")
        lines.append("")
        for t in tensions:
            lines.append(f"- **{t['name']}.** {t['description']}")
        lines.append("")

    # Measurement discipline
    lines.append("## The measurement discipline")
    lines.append("")
    lines.append("We baseline before we deploy, claim incremental lift against a holdout "
                 "rather than gross results, and agree the scorecard with Finance up front. "
                 "That keeps every claim defensible in front of the stakeholders whose trust "
                 "the crawl phase is built to earn.")
    lines.append("")

    return "\n".join(lines)
