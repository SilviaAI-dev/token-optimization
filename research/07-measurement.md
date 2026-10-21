# 07: Measuring Whether an Optimization Worked

An optimization succeeds only if quality holds or improves *and* cost falls on your own workload. Every vendor source reviewed says the same: "Test your use case" (Anthropic), "measure before you ship" (Anthropic on steering), "test other levels against your own tasks" (OpenAI).

## Metrics

| Metric | How to get it | Why |
|---|---|---|
| Output tokens (total) | `usage.output_tokens` | Billing truth for output |
| Thinking tokens | `usage.output_tokens_details.thinking_tokens` | Separates thinking from visible text. Billed even when display is omitted |
| Visible tokens | `output_tokens − thinking_tokens` | Target for verbosity work |
| Input split | `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` | Cache hit rate = read ÷ (read + creation + input) |
| Cost in dollars | Tokens × current prices, including cache multipliers | Token cuts that break caching can *raise* cost |
| Task quality | Your grader: tests passing, exact match, rubric | The constraint you must not violate |
| Hard-tail quality | Quality on the hardest 10–20% of items | Compression losses concentrate here (token-complexity threshold) |
| Thinking trigger rate | Share of responses with a thinking block | Anthropic's suggested steering metric |
| Latency | TTFT and total | Thinking drives time to first token |
| Agent loop size | Tool calls per task, subagents spawned, turns | Over-exploration and over-delegation |
| Outcome efficiency (optional) | Share of tokens generated before the first correct answer (Chen et al., ICML 2025) | Directly measures "re-solving after solved" |

## Protocol

1. **Build an eval set** of about 50–200 items that reflects real traffic, stratified by difficulty. Include the cases you care most about.
2. **Baseline:** current prompt at the current effort. Record every metric above, with 3+ samples per item if outputs vary.
3. **Change one variable at a time:** effort level, then removals, then additions, then context changes.
4. **Grade without length bias:** rubric or test-based where possible. If you use an LLM judge, blind it to which variant is which, ask it to ignore length, or apply length control as in LC-AlpacaEval (Dubois et al.).
5. **Accept a change only if** overall quality is within your tolerance (e.g., no statistically meaningful drop), hard-tail quality doesn't drop, and cost or latency improves.
6. **Re-run on model upgrades.** Effort levels are recalibrated between models. Anthropic says to run a fresh sweep instead of carrying settings over.

## Minimal harness sketch (Python, illustrative)

Field names follow Anthropic's docs as of October 2026. Check them against your SDK version.

```python
import anthropic, statistics

client = anthropic.Anthropic()

def run(item, system, effort):
    r = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=32000,
        system=system,
        output_config={"effort": effort},
        messages=[{"role": "user", "content": item["prompt"]}],
    )
    text = "".join(b.text for b in r.content if b.type == "text")
    u = r.usage
    thinking = getattr(getattr(u, "output_tokens_details", None), "thinking_tokens", 0) or 0
    return {
        "correct": item["grade"](text),           # your grader
        "out": u.output_tokens,
        "thinking": thinking,
        "visible": u.output_tokens - thinking,
        "cache_read": u.cache_read_input_tokens or 0,
        "input": u.input_tokens,
    }

def sweep(items, system, efforts=("low", "medium", "high")):
    for e in efforts:
        rows = [run(it, system, e) for it in items]
        acc = sum(r["correct"] for r in rows) / len(rows)
        print(e, f"acc={acc:.3f}",
              f"out={statistics.mean(r['out'] for r in rows):.0f}",
              f"thinking={statistics.mean(r['thinking'] for r in rows):.0f}",
              f"visible={statistics.mean(r['visible'] for r in rows):.0f}")
```

Extensions:
- Add `difficulty` to each item and report accuracy per stratum.
- For agent loops, sum usage across every request in the turn, and count tool calls and subagents.
- To A/B prompt variants, hold effort fixed and swap `system`.

## Reading results

- **Thinking falls, quality flat:** a good cut. Keep it.
- **Visible tokens fall, quality flat, user satisfaction unknown:** check with real users. Concise is usually preferred, but some products need explanation.
- **Average flat, hard tail drops:** you've hit the compression floor. Route hard items to higher effort.
- **Tokens fall, cost rises:** you broke caching. Check for changed prefixes, effort or tool changes, or clearing without `clear_at_least`.
- **Thinking unchanged after a prompt instruction:** expected on some models (Sonnet and Haiku 5.5). Use effort instead.
