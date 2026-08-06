#!/usr/bin/env python3
"""
run.py

Convenience wrapper to run the Account Intelligence Engine from the repo root,
so you do not have to change into src/ or manage relative paths.

Examples:
  python run.py --company examples/harborview_profile.json
  python run.py --company examples/harborview_profile.json --name harborview
  python run.py --company examples/harborview_profile.json --no-deck

By default it writes three files into examples/, named after the profile:
  <name>_result.json   the structured result
  <name>_readout.md    the markdown readout
  <name>_deck.pptx     the meeting-ready deck

The engine core and the readout need only the Python standard library. The deck
needs python-pptx (pip install -r requirements.txt). Use --no-deck to skip it.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT / "src"))

from engine import load_data, score_company  # noqa: E402
from render_readout import render            # noqa: E402


def main():
    p = argparse.ArgumentParser(
        description="Run the Account Intelligence Engine on a company profile."
    )
    p.add_argument("--company", required=True,
                   help="Path to a company profile JSON (e.g. examples/harborview_profile.json).")
    p.add_argument("--name",
                   help="Base name for the output files. Defaults to the profile file name.")
    p.add_argument("--outdir", default="examples",
                   help="Directory for output files (default: examples).")
    p.add_argument("--no-deck", action="store_true", help="Skip the .pptx deck output.")
    p.add_argument("--no-readout", action="store_true", help="Skip the markdown readout output.")
    p.add_argument("--quiet", action="store_true", help="Do not print the ranked summary.")
    args = p.parse_args()

    company_path = Path(args.company)
    if not company_path.exists():
        sys.exit(f"Profile not found: {company_path}")

    base = args.name or company_path.stem.replace("_profile", "")
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    objectives, catalog, patterns = load_data()
    profile = json.loads(company_path.read_text())
    result = score_company(profile, objectives, catalog, patterns)

    outputs = []
    result_path = outdir / f"{base}_result.json"
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    outputs.append(result_path)

    if not args.no_readout:
        readout_path = outdir / f"{base}_readout.md"
        readout_path.write_text(render(result))
        outputs.append(readout_path)

    if not args.no_deck:
        try:
            from render_deck import build_deck  # lazy: only needs python-pptx here
        except ImportError:
            sys.exit(
                "The deck output needs python-pptx. Install it with "
                "`pip install -r requirements.txt`, or re-run with --no-deck."
            )
        deck_path = outdir / f"{base}_deck.pptx"
        build_deck(result, str(deck_path))
        outputs.append(deck_path)

    if not args.quiet:
        print(f"Company: {result['company']['name']}")
        print(f"Ranked use cases: {len(result['ranked_use_cases'])}")
        for u in result["ranked_use_cases"]:
            print(f"  {u['weighted_total']:.3f}  {u['solution_name']} -> {u['primary_objective_name']}")
        print("Roadmap:")
        for phase in ("crawl", "walk", "run"):
            names = [u["solution_name"] for u in result["roadmap"][phase]]
            print(f"  {phase}: {', '.join(names)}")

    print("\nWrote:")
    for o in outputs:
        print(f"  {o}")


if __name__ == "__main__":
    main()
