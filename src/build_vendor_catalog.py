"""
build_vendor_catalog.py

Builds the vendor catalog layer for the Account Intelligence Engine.

This vendor is entirely fictional. "Meridian Experience Cloud" does not exist.
Its solutions, capabilities, and proof points are invented to demonstrate how a
real vendor catalog would plug into the engine. Swap this file for a different
catalog and the same engine works for a different vendor.

Every solution maps to objectives by referencing the stable IDs in
data/objective_layer.json (industry_id + objective_id), so the scoring layer can
match a company's stated objectives to vendor capabilities without string
matching on display names.

Design guardrails, kept on purpose:
- Proof points are illustrative and labeled as such. A proof point without a
  verifiable source is a wish, not evidence.
- No solution claims to "make a customer compliant." Governance tooling supports
  obligations; it does not discharge them. This mirrors the discipline required
  in regulated industries.

Output: data/vendor_catalog.json
"""

import json
from pathlib import Path

SCHEMA_VERSION = "1.0"

VENDOR = {
    "id": "meridian",
    "name": "Meridian Experience Cloud",
    "fictional": True,
    "category": "Customer data and experience platform",
    "positioning": (
        "A single foundation for customer data, journey orchestration, "
        "analytics, content, governance, and conversational experience. "
        "Meridian is fictional and exists only to demonstrate the engine."
    ),
}

# Each solution maps to a set of {industry_id, objective_id} pairs drawn from
# data/objective_layer.json. Mappings are representative, not exhaustive.
SOLUTIONS = [
    {
        "id": "meridian-profile",
        "name": "Meridian Profile",
        "category": "Customer data platform",
        "what_it_does": "Unifies customer data into a real-time, single profile that every channel can act on, with a federated option that queries the customer's own warehouse rather than copying data out of it.",
        "capabilities": ["Real-time profile unification", "Identity resolution across web, app, email, and call center", "Federated queries against the customer's data warehouse", "Audience building and activation"],
        "maps_to_objectives": [
            {"industry_id": "retail-banking", "objective_id": "cross-sell"},
            {"industry_id": "retail-banking", "objective_id": "retention"},
            {"industry_id": "retail-banking", "objective_id": "acquisition"},
            {"industry_id": "wealth-management", "objective_id": "retention-depth"},
            {"industry_id": "insurance", "objective_id": "retention-persistency"},
            {"industry_id": "retail", "objective_id": "retention-loyalty"},
            {"industry_id": "media-entertainment", "objective_id": "engagement"},
            {"industry_id": "travel-hospitality", "objective_id": "loyalty"},
        ],
        "proof_points": ["Illustrative: unified profiles across five channels in a single activation layer"],
        "differentiators": ["Federated option keeps regulated data in place", "Real-time rather than batch profile updates"],
    },
    {
        "id": "meridian-journeys",
        "name": "Meridian Journeys",
        "category": "Journey orchestration",
        "what_it_does": "Designs and triggers personalized journeys across channels in real time, from onboarding to retention, based on live customer behavior.",
        "capabilities": ["Real-time triggered journeys", "Known-visitor personalization at the edge", "Onboarding and lifecycle campaigns", "Next-best-action delivery"],
        "maps_to_objectives": [
            {"industry_id": "retail-banking", "objective_id": "acquisition"},
            {"industry_id": "retail-banking", "objective_id": "retention"},
            {"industry_id": "b2b-saas", "objective_id": "customer-success"},
            {"industry_id": "b2b-saas", "objective_id": "retention-expansion"},
            {"industry_id": "retail", "objective_id": "conversion-basket"},
            {"industry_id": "healthcare-payer", "objective_id": "member-experience"},
            {"industry_id": "travel-hospitality", "objective_id": "demand-bookings"},
        ],
        "proof_points": ["Illustrative: onboarding journey lifted completed sign-ups versus a static flow in an internal test"],
        "differentiators": ["Journeys triggered on live behavior, not overnight segments"],
    },
    {
        "id": "meridian-analytics",
        "name": "Meridian Analytics",
        "category": "Cross-channel analytics",
        "what_it_does": "Analyzes the full customer journey across channels on one data set, so teams can follow a single customer from web to app to call center in one analysis.",
        "capabilities": ["Cross-channel journey analysis", "Unified data set across touchpoints", "Holdout and incrementality testing", "Attribution and funnel analysis"],
        "maps_to_objectives": [
            {"industry_id": "retail-banking", "objective_id": "customer-experience"},
            {"industry_id": "retail", "objective_id": "conversion-basket"},
            {"industry_id": "media-entertainment", "objective_id": "content-roi"},
            {"industry_id": "b2b-saas", "objective_id": "plg"},
            {"industry_id": "travel-hospitality", "objective_id": "customer-experience"},
            {"industry_id": "wealth-management", "objective_id": "client-experience"},
        ],
        "proof_points": ["Illustrative: single cross-channel view replacing three disconnected reporting tools"],
        "differentiators": ["Built-in holdouts make incremental lift measurable rather than assumed"],
    },
    {
        "id": "meridian-content",
        "name": "Meridian Content Studio",
        "category": "Content management and generative AI",
        "what_it_does": "Speeds compliant content and campaign production with commercially safe generative AI, shared review workflows, and reusable brand-governed assets.",
        "capabilities": ["Commercially safe generative AI for content", "Review and approval workflows", "Reusable brand-governed asset library", "Campaign asset production at scale"],
        "maps_to_objectives": [
            {"industry_id": "retail-banking", "objective_id": "operational-efficiency"},
            {"industry_id": "retail", "objective_id": "acquisition-traffic"},
            {"industry_id": "media-entertainment", "objective_id": "content-roi"},
            {"industry_id": "insurance", "objective_id": "distribution"},
            {"industry_id": "travel-hospitality", "objective_id": "demand-bookings"},
        ],
        "proof_points": ["Illustrative: shorter brief-to-launch time on campaign content in an internal benchmark"],
        "differentiators": ["Generative AI trained for commercial safety", "Compliance review built into the production path"],
    },
    {
        "id": "meridian-govern",
        "name": "Meridian Govern",
        "category": "Consent and data governance",
        "what_it_does": "Enforces data-use and consent rules at the field level across every activation, with an audit trail, so teams can honor obligations consistently across channels.",
        "capabilities": ["Field-level data-use enforcement", "Consent policy management", "Audit trail across activations", "Customer-managed encryption keys"],
        "maps_to_objectives": [
            {"industry_id": "retail-banking", "objective_id": "risk-compliance"},
            {"industry_id": "insurance", "objective_id": "risk-compliance"},
            {"industry_id": "wealth-management", "objective_id": "risk-compliance"},
            {"industry_id": "healthcare-payer", "objective_id": "risk-compliance"},
            {"industry_id": "healthcare-provider", "objective_id": "safety-compliance"},
        ],
        "proof_points": ["Illustrative: field-level consent enforcement applied consistently across activation channels"],
        "differentiators": ["Enforcement at the point of activation, not just at collection"],
        "guardrail": "Supports data-use and consent obligations. Does not by itself make an organization compliant; regulated advice stays human-accountable.",
    },
    {
        "id": "meridian-concierge",
        "name": "Meridian Concierge",
        "category": "Conversational AI",
        "what_it_does": "Delivers brand-governed conversational experiences that handle high-volume self-service while staying inside defined guardrails.",
        "capabilities": ["Brand-governed conversational agents", "Guardrailed responses within policy", "Self-service deflection for common tasks", "Handoff to human when needed"],
        "maps_to_objectives": [
            {"industry_id": "retail-banking", "objective_id": "customer-experience"},
            {"industry_id": "healthcare-payer", "objective_id": "member-experience"},
            {"industry_id": "healthcare-provider", "objective_id": "patient-experience"},
            {"industry_id": "travel-hospitality", "objective_id": "customer-experience"},
            {"industry_id": "b2b-saas", "objective_id": "customer-success"},
        ],
        "proof_points": ["Illustrative: common self-service tasks handled within guardrails, with human handoff on exceptions"],
        "differentiators": ["Guardrails and brand governance applied to every response"],
        "guardrail": "Conversational guidance in regulated contexts stays inside policy and hands off to a human where accountability is required.",
    },
]


def build():
    return {
        "schema_version": SCHEMA_VERSION,
        "description": (
            "Fictional vendor catalog for the Account Intelligence Engine. "
            "Meridian Experience Cloud does not exist. Solutions map to the "
            "objective layer by industry_id and objective_id so the scoring "
            "layer can match stated objectives to vendor capabilities. Proof "
            "points are illustrative."
        ),
        "vendor": VENDOR,
        "solution_count": len(SOLUTIONS),
        "solutions": SOLUTIONS,
    }


def main():
    out_dir = Path(__file__).parent.parent / "data"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "vendor_catalog.json"
    out_path.write_text(json.dumps(build(), indent=2, ensure_ascii=False))
    mappings = sum(len(s["maps_to_objectives"]) for s in SOLUTIONS)
    print(f"Wrote {out_path}")
    print(f"  vendor: {VENDOR['name']} (fictional)")
    print(f"  solutions: {len(SOLUTIONS)}")
    print(f"  objective mappings: {mappings}")


if __name__ == "__main__":
    main()
