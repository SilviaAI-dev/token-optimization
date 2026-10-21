"""Derive cost-efficiency metrics for Claude Opus 5.5 effort levels.

Reads the CSVs in ../data and prints Markdown tables used in
08-effort-cost-analysis.md. Standard library only:

    python3 research/analysis/effort_cost.py
"""

import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def load(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))


def swebench_table(rows):
    print("| Effort | Solved | Cost/task | Cost/solved | Δ solved vs prev (per 100 tasks) | Δ cost vs prev (per 100 tasks) | Marginal $ per extra solve |")
    print("|---|---|---|---|---|---|---|")
    prev = None
    for r in rows:
        rate, cost = float(r["solve_rate"]), float(r["cost_per_task_usd"])
        cells = [r["effort"], f"{rate:.1%}", f"${cost:.2f}", f"${cost / rate:.3f}"]
        if prev:
            d_solved = (rate - prev[0]) * 100
            d_cost = (cost - prev[1]) * 100
            cells += [f"+{d_solved:.1f}", f"+${d_cost:.0f}", f"${d_cost / d_solved:.2f}"]
        else:
            cells += ["n/a", "n/a", "n/a"]
        print("| " + " | ".join(cells) + " |")
        prev = (rate, cost)


def aa_table(rows):
    base = rows[0]
    b_tok, b_cost = float(base["output_tokens_millions"]), float(base["cost_per_task_usd"])
    print("| Effort | Index | Output tokens (M) | Tokens vs low | Cost/task | Cost vs low | Δ index vs prev | Δ tokens vs prev | Index points per extra $ |")
    print("|---|---|---|---|---|---|---|---|---|")
    prev = None
    for r in rows:
        idx, tok, cost = int(r["intelligence_index"]), float(r["output_tokens_millions"]), float(r["cost_per_task_usd"])
        cells = [r["effort"], str(idx), f"{tok:.0f}", f"{tok / b_tok:.1f}x", f"${cost:.2f}", f"{cost / b_cost:.1f}x"]
        if prev:
            cells += [f"+{idx - prev[0]}", f"+{(tok - prev[1]) / prev[1]:.0%}", f"{(idx - prev[0]) / (cost - prev[2]):.1f}"]
        else:
            cells += ["n/a", "n/a", "n/a"]
        print("| " + " | ".join(cells) + " |")
        prev = (idx, tok, cost)


if __name__ == "__main__":
    print("## Anthropic SWE-bench Pro subset\n")
    swebench_table(load("opus-5-5-effort-anthropic-swebench-pro.csv"))
    print("\n## Artificial Analysis Intelligence Index\n")
    aa_table(load("opus-5-5-effort-artificial-analysis.csv"))
