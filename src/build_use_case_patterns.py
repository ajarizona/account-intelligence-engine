"""
build_use_case_patterns.py

Reusable use-case patterns for the Account Intelligence Engine.

Two kinds of pattern live here:

1. value_patterns: repeatable ways to frame value for a class of company (for
   example, an agentic approach for a regulated bank). Each maps to vendor
   solutions and to objective-layer IDs, so the engine can attach a pattern to
   a scored use case rather than reinventing the narrative each time.

2. execution_challenges: the recurring challenges any team hits when executing
   a data-driven use case, and which solutions address them. The engine folds
   these into an output so the readout is honest about what delivery takes.

All content is vendor-agnostic and synthetic. Solutions reference the fictional
Meridian catalog by ID; objectives reference the objective layer by ID. No real
company, client, or vendor appears here.

Output: data/use_case_patterns.json
"""

import json
from pathlib import Path

SCHEMA_VERSION = "1.0"

VALUE_PATTERNS = [
    {
        "id": "agentic-value-regulated-bank",
        "name": "Agentic value framing for a regulated bank",
        "applies_to_industries": ["retail-banking"],
        "thesis": (
            "An agentic approach helps a regulated bank grow without growing "
            "risk in step. The value comes from purpose-built, governed agents "
            "embedded in content, marketing, and service workflows, not from "
            "handing work to uncontrolled autonomous systems."
        ),
        "principles": [
            "Human in the loop: agents assist and recommend; people stay accountable for regulated decisions.",
            "Governed by default: data-use and consent rules are enforced at the point of action, with an audit trail.",
            "Explainable, not black box: every agent action can be traced and reviewed.",
            "Outcome-anchored: each use case ties to a KPI the bank already funds.",
        ],
        "maps_to_solutions": ["meridian-concierge", "meridian-govern", "meridian-profile", "meridian-journeys"],
        "maps_to_objectives": [
            {"industry_id": "retail-banking", "objective_id": "customer-experience"},
            {"industry_id": "retail-banking", "objective_id": "operational-efficiency"},
            {"industry_id": "retail-banking", "objective_id": "cross-sell"},
            {"industry_id": "retail-banking", "objective_id": "risk-compliance"},
        ],
    },
]

EXECUTION_CHALLENGES = [
    {
        "id": "data-quality-segmentation",
        "name": "Data quality and segmentation complexity",
        "description": (
            "Precise segmentation depends on accurate, complete data across "
            "multiple systems, and on integrating external signals cleanly. "
            "Gaps and mismatches undermine every downstream use case."
        ),
        "mitigated_by_solutions": ["meridian-profile", "meridian-govern"],
    },
    {
        "id": "content-personalization-scale",
        "name": "Content personalization at scale",
        "description": (
            "Personalized experiences demand custom content across segments and "
            "channels, which can strain creative and development capacity if "
            "production is not shortened and governed."
        ),
        "mitigated_by_solutions": ["meridian-content", "meridian-journeys"],
    },
    {
        "id": "system-dependencies",
        "name": "Technology enablement and system dependencies",
        "description": (
            "Execution spans several platforms and integrations. Activation and "
            "tracking must be coordinated across systems, which requires "
            "flexibility and delivery bandwidth."
        ),
        "mitigated_by_solutions": ["meridian-profile", "meridian-journeys", "meridian-analytics"],
    },
    {
        "id": "measurement-attribution",
        "name": "Measurement and attribution complexity",
        "description": (
            "Attributing engagement and conversion to specific tactics is hard "
            "when many things move an outcome. Honest measurement claims "
            "incremental lift against a holdout, not gross results."
        ),
        "mitigated_by_solutions": ["meridian-analytics"],
    },
    {
        "id": "governance-control",
        "name": "Governance and human-in-the-loop control",
        "description": (
            "In regulated settings, agent actions must stay inside policy, honor "
            "consent, and hand off to a human where accountability is required. "
            "Governance is a design requirement, not an afterthought."
        ),
        "mitigated_by_solutions": ["meridian-govern", "meridian-concierge"],
    },
]


def build():
    return {
        "schema_version": SCHEMA_VERSION,
        "description": (
            "Reusable value patterns and execution-challenge taxonomy for the "
            "Account Intelligence Engine. Vendor-agnostic and synthetic. "
            "Solutions reference the Meridian catalog by ID; objectives "
            "reference the objective layer by ID."
        ),
        "value_pattern_count": len(VALUE_PATTERNS),
        "execution_challenge_count": len(EXECUTION_CHALLENGES),
        "value_patterns": VALUE_PATTERNS,
        "execution_challenges": EXECUTION_CHALLENGES,
    }


def main():
    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "use_case_patterns.json"
    out_path.write_text(json.dumps(build(), indent=2, ensure_ascii=False))
    print(f"Wrote {out_path}")
    print(f"  value patterns: {len(VALUE_PATTERNS)}")
    print(f"  execution challenges: {len(EXECUTION_CHALLENGES)}")


if __name__ == "__main__":
    main()
