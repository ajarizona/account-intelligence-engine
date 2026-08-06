# Quickstart

How to run the Account Intelligence Engine and point it at your own company.

## Install

From the repo root:

```
pip install -r requirements.txt
```

The engine core and the markdown readout need only the Python standard library.
python-pptx is the one external dependency, and it is needed only for the .pptx
deck output. If you do not want the deck, you can skip the install and run with
`--no-deck`.

## Run the worked example

```
python run.py --company examples/harborview_profile.json
```

This scores the example profile and writes three files into `examples/`:

- `harborview_result.json`  the structured result, every score with its breakdown
- `harborview_readout.md`   the readout in prose
- `harborview_deck.pptx`    the meeting-ready deck

It also prints the ranked use cases and the crawl, walk, run roadmap to the
terminal.

## Command reference

```
python run.py --company PATH [options]

--company PATH     Path to a company profile JSON. Required.
--name NAME        Base name for the output files. Defaults to the profile
                   file name with "_profile" removed.
--outdir DIR       Directory for output files. Default: examples.
--no-deck          Skip the .pptx deck (no python-pptx needed).
--no-readout       Skip the markdown readout.
--quiet            Do not print the ranked summary.
```

Running directly, without the wrapper, also works from inside `src/`:

```
cd src
python engine.py --company ../examples/harborview_profile.json \
  --out-readout ../examples/out.md \
  --out-deck ../examples/out.pptx \
  --out-json ../examples/out.json
```

The wrapper is just the friendlier front door.

## Run it on your own company

1. Copy the example profile:

   ```
   cp examples/harborview_profile.json examples/acme_profile.json
   ```

2. Edit the `company` block: the `name`, the `industry_id` (must be one of the
   IDs listed below), and a short `profile` description.

3. Rewrite `stated_objectives` to reflect what the company has actually said in
   its public filings. Each entry has:

   - `objective_id`  must be a valid ID for the chosen industry (see below)
   - `emphasis`      0 to 1, how central this objective is to the company
   - `value_signal`  0 to 1, how large the payoff would be
   - `evidence`      a short note on where in the filings you saw it

   This is the analyst's judgment step. The engine scores what you give it; it
   does not invent the inputs.

4. Run it:

   ```
   python run.py --company examples/acme_profile.json
   ```

## How the rubric works

Each use case is scored on four dimensions, then combined with these weights:

- Strategic alignment 0.35, from the `emphasis` you set on the matched objective
- Value at stake 0.30, from the `value_signal`, with a small boost when one
  solution addresses several of the company's objectives
- Time to value and feasibility 0.20, from a per-solution readiness map
- Evidence strength 0.15, from the vendor's proof points, capped because those
  proof points are illustrative

All weights and knobs live in the `CONFIG` block at the top of `src/engine.py`.

## Reading the output

- The ranked list is what matters most, by score.
- The roadmap is what to do first, sequenced by readiness into crawl, walk, run.
  These can differ on purpose: the highest-value work is not always first to do.
- If you list an objective and no use case comes back for it, no vendor solution
  maps to that objective in the catalog. That is the engine reporting an honest
  partial fit, not an error. Fewer matches means the vendor is a partial fit for
  that company.

## Valid industry and objective IDs

Use exactly these IDs in a profile. Objective IDs are only valid within their
own industry.

**retail-banking** (Retail Banking): profitability, acquisition, retention,
deposit-funding, lending-credit, cross-sell, operational-efficiency,
risk-compliance, customer-experience

**insurance** (Insurance): underwriting-profitability, premium-growth,
retention-persistency, claims, distribution, investment-capital, risk-compliance,
customer-experience

**wealth-management** (Wealth Management): aum-growth, revenue-profitability,
client-acquisition, retention-depth, advisor-productivity, investment-performance,
risk-compliance, client-experience

**healthcare-provider** (Healthcare Provider): clinical-quality, access-volume,
financial-sustainability, patient-experience, operational-efficiency, workforce,
value-based, safety-compliance

**healthcare-payer** (Healthcare Payer): medical-cost, membership,
financial-performance, quality-stars, member-experience, network, care-management,
risk-compliance

**retail** (Retail): revenue-comps, gross-margin, acquisition-traffic,
retention-loyalty, conversion-basket, inventory-supply, omnichannel,
operational-efficiency, customer-experience

**media-entertainment** (Media & Entertainment): audience-growth, engagement,
retention, monetization, content-roi, advertising, profitability, brand-experience

**b2b-saas** (B2B SaaS): recurring-revenue, acquisition, retention-expansion,
customer-success, unit-economics, plg, profitability, market-expansion

**travel-hospitality** (Travel & Hospitality): revenue-yield, demand-bookings,
loyalty, customer-experience, operational-efficiency, ancillary-revenue,
distribution, capacity-utilization
