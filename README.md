# Account Intelligence Engine

This repository documents the design of a system built inside client engagements. The implementation shown here is an abstracted, vendor-agnostic reference version, and no client names, deal metrics, or proprietary vendor material appear in it.

*From a company's public record to a scored, client-ready use-case library, in an afternoon instead of a week.*

## The problem this solves

Every solution engineer knows the drill before a first meeting with a target account. You read the 10-K. You pull the last few earnings transcripts. You skim the press releases. Then you try to connect what the business is actually worried about to what your product can do for them, and you turn all of that into something a customer will sit still for: an account plan, a point of view, a deck. Done well, it takes the better part of a week. Done under time pressure, it gets skipped, and you walk into the room with generic talking points.

What I built here is an engine that does the reading and the first pass of the thinking, so the SE spends their time on judgment and the conversation instead of on assembly.

## What it does

Point it at a company's public documents (10-Ks, earnings call transcripts, press releases) and a vendor's solution catalog. It reads the filings for the business objectives and pressures that matter, matches them against what the vendor can credibly deliver, scores every candidate use case, and produces three client-ready artifacts from the top of that list.

The output is not a summary of the 10-K. It is a ranked set of use cases, each one tied to a business objective the company has actually stated, with the evidence attached.

## How it works

Three layers, deliberately separated so the engine is reusable rather than a one-off build:

**A shared, cross-industry KPI and business-objective layer.** This is the foundation. It started in financial services and now spans nine industries: retail banking, insurance, wealth management, healthcare provider, healthcare payer, retail, media and entertainment, B2B SaaS, and travel and hospitality. For each one it carries the business objectives that matter, the KPIs leaders actually track, and, just as important, the strategic tensions between them. It knows that in retail banking, aggressive lending growth pulls against credit quality, and that in a health plan, cutting the medical loss ratio too hard damages the very Star ratings that drive revenue. That last part is what makes it more than a lookup table: the engine will not lead with a use case that wins one KPI while quietly damaging another, because the trade-off is encoded in the foundation.

**A vendor catalog layer.** This is where a specific vendor's solutions, proof points, and differentiators plug in. Swap this layer and the same engine works for a different vendor.

**A scoring and generation layer.** This reads the target company's documents, maps stated objectives to vendor capabilities, scores each candidate use case against a weighted rubric, and generates the artifacts from the top of the ranked list.

## The scoring rubric

Not every use case that could work is worth leading with. The rubric weights four things:

- **Strategic alignment (0.35):** how directly the use case maps to an objective the company has stated in its own filings
- **Value at stake (0.30):** the size of the outcome if it works, read against the KPIs that industry actually funds
- **Time to value and feasibility (0.20):** how quickly and realistically it can be delivered
- **Evidence strength (0.15):** how well we can back the claim with the vendor's proof points

Strategic alignment carries the most weight on purpose. A use case that solves a problem the company has told the market it cares about earns the first conversation. Everything else supports that.

## What comes out

Three artifacts, all generated from the same scored library so the story stays consistent from the internal plan to the customer-facing deck:

- A **Word account plan** for the account team
- A **Word execution playbook** for the delivery motion
- A **PowerPoint deck** for the client conversation

## How it fits a real account motion

This is where the engine earns its keep. I designed it around a crawl, walk, run motion, because that is how accounts actually grow.

**Crawl:** start with one account and one vendor. Prove the top three use cases are real, grounded in the company's own words, and worth a meeting.

**Walk:** expand the library across the account's business units, and bring more of the vendor's catalog into play as trust builds.

**Run:** run the same engine across a book of accounts, so the whole team walks into every first meeting with a grounded point of view instead of a generic pitch.

## Validation

I validated the engine on a test run using the public filings of a top-tier US retail bank. The point of the test was not to claim a business result I cannot verify from outside the account. It was to confirm the engine could take real, messy, public documents and produce a use-case library that a working SE would recognize as accurate and worth taking into a room. It did.

## A note on what is and is not here

This is an abstracted, vendor-agnostic version of work originally built inside live sales engagements. Client names, deal metrics, and any confidential proof points have been removed. What remains is the design: the architecture, the cross-industry objective layer, the rubric, and the generation pipeline. Nothing in this repository overstates a compliance certification or a customer outcome, which is a discipline that matters more in regulated industries than anywhere else.

## Running the engine

Everything runs from the repo root.

Install the one dependency, which is needed only for the .pptx deck:

```
pip install -r requirements.txt
```

Run the engine on the worked example:

```
python run.py --company examples/harborview_profile.json
```

That reads the company profile, scores the use cases, and writes three files into `examples/`: a structured result (`.json`), a readout (`.md`), and a meeting-ready deck (`.pptx`). Add `--no-deck` to skip the deck if you have not installed python-pptx.

To run it on a different company, copy `examples/harborview_profile.json`, edit the company block and the stated objectives to match what that company has said in its public filings, and point `run.py` at the new file. The profile format and the valid industry and objective IDs are documented in `QUICKSTART.md`.

## Adapting this for your own use

The layered design has two deliberate swap points, the company profile and the vendor catalog, so the engine can run on real work without touching the scoring code. The examples shipped here are fictional on purpose; the pattern below is how you would point it at something real.

**Bring your own vendor catalog.** The bundled catalog is a fictional vendor, Meridian. To run against a real vendor, build a catalog in the same schema as `data/vendor_catalog.json`: each solution, its capabilities and public proof points, mapped to the objective IDs it addresses. Then pass it in:

```
python run.py --company examples/acme_profile.json --catalog path/to/your_catalog.json
```

A richer, real catalog usually produces better coverage than the demo one, since the demo maps only a few solutions per industry.

**Build profiles from real filings.** The engine scores structured objectives, not raw documents, on purpose: that is what keeps the scoring deterministic and auditable. So a 10-K is the source you distill a profile from, not something the engine reads directly. You can do that distillation by hand, or hand the filing to an assistant and ask it to draft a profile in the documented schema, but a human confirms the emphasis and value reads before scoring. The document informs the profile; a person signs off on the judgment.

**Keep real work private.** Real client and vendor material does not belong in a public repo. The included `.gitignore` already excludes a `/private/` folder, so the intended pattern is to keep real profiles and catalogs in `private/` where git never sees them, and run the same engine against them locally. The public repo stays fictional; your live work stays out of it.

**What this is and is not.** This is a reference implementation, not a finished product. The scoring is transparent rather than magic, and the quality of the output depends on the quality of the catalog and the honesty of the profile inputs. It is meant to be read, understood, and extended.

## Tech notes

- Written in Python. The engine core and the readout need only the standard library.
- The .pptx deck is generated with python-pptx, the one external dependency.
- The cross-industry KPI and objective layer is maintained as structured JSON, kept separate from any single vendor.
- The scoring rubric is configurable in a single CONFIG block, so the weights can be tuned per vendor or per campaign.
