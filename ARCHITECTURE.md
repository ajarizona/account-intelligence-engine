# Architecture

This engine is built as three data layers and one scoring layer, kept deliberately separate so each piece can change without the others breaking.

## The objective layer

`data/objective_layer.json`, built by `src/build_objective_layer.py`, is the vendor-agnostic foundation. It covers nine industries (retail banking, insurance, wealth management, healthcare provider, healthcare payer, retail, media and entertainment, B2B SaaS, and travel and hospitality). For each industry it carries the business objectives that matter, the KPIs leaders actually track against each one, and the strategic tensions between objectives, for example how aggressive lending growth in retail banking pulls against credit quality. This layer contains no vendor, product, or client data. It is the thing every other layer plugs into.

## The vendor catalog layer

`data/vendor_catalog.json`, built by `src/build_vendor_catalog.py`, describes a single vendor's solutions: what each one does, its capabilities, proof points, and differentiators. The vendor here, Meridian Experience Cloud, is fictional. Each solution maps to the objective layer through shared IDs (an industry ID paired with an objective ID), not by matching display names. That is what lets the scoring layer connect a solution to a stated objective reliably, and what lets this layer be swapped for a different vendor's catalog without touching the objective layer or the engine.

## The patterns layer

`data/use_case_patterns.json`, built by `src/build_use_case_patterns.py`, holds two kinds of reusable content. Value patterns are repeatable ways to frame the value of a class of company, for example an agentic approach for a regulated bank, and each one maps to a set of solution IDs and objective IDs so the engine can attach a pattern to a scored result instead of writing the narrative by hand each time. Execution challenges are the recurring problems any team hits delivering a data-driven use case (data quality, content production at scale, system dependencies, measurement, governance), and each one lists the solution IDs that mitigate it. Folding these into the output is what keeps a readout honest about what delivery actually takes, not just what the upside looks like.

## The scoring engine

`src/engine.py` reads a company profile (the objectives a company has stated in its own filings, each with an emphasis and a value signal) and matches vendor solutions to those stated objectives through the shared IDs described above. Every match becomes a candidate use case, scored on a weighted rubric:

- Strategic alignment, 0.35: how directly the use case maps to a stated objective
- Value at stake, 0.30: the size of the outcome, read against the objective's value signal
- Time to value and feasibility, 0.20: how quickly and realistically the solution can be delivered
- Evidence strength, 0.15: how well the claim is backed by the vendor's proof points

Every score keeps its per-dimension breakdown in the result, so the ranking is auditable rather than a black box. Evidence strength is deliberately capped, because catalog proof points are labeled illustrative, not verified, and the scoring should not let an unverified claim carry as much weight as one with real backing.

Scoring produces a rank (by weighted score) and, separately, a readiness figure that sequences the same use cases into a crawl, walk, run roadmap. Readiness is not the same as rank: in a regulated industry, a governance-related solution gets a readiness bonus so it lands early even if a growth-oriented solution scores higher on the rubric, because the roadmap proves governance before it scales growth. `src/render_readout.py` then turns the structured result into a markdown readout in a consistent voice.

All scoring knobs (the rubric weights, feasibility ratings, the regulated-industry list, the readiness bonuses and penalties, and the evidence cap) live in one `CONFIG` block at the top of `engine.py`, so the rubric is visible and can be tuned per vendor or per campaign without hunting through the code.

## Data flow

A company profile goes in (`examples/harborview_profile.json`, the Harborview Financial Group example). `engine.py` scores it against the objective layer, the vendor catalog, and the patterns layer, and produces a structured result (`examples/harborview_engine_result.json`): ranked use cases, the crawl/walk/run roadmap, the attached value pattern, the relevant execution challenges, and the industry's strategic tensions. `render_readout.py` turns that same structured result into a readable readout (`examples/harborview_generated_readout.md`). Both outputs come from the same scored data, so the internal plan and the client-facing narrative never drift apart.
