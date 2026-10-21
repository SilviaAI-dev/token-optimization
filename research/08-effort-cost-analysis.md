# 08: Opus 5.5 Effort Levels: Cost, Tokens, Code Quality, and Hallucination

Question: how much do Opus 5.5's effort levels (`low`, `medium`, `high`, `xhigh`, `max`) cost in tokens and dollars, what quality does each buy, and does higher effort cause more hallucination?

Data was collected 2026-10-21. The raw numbers are in [`data/`](data/). Every derived figure below comes from [`analysis/effort_cost.py`](analysis/effort_cost.py) (`python3 research/analysis/effort_cost.py`).

## Bottom line

1. **Effort is the biggest lever on output tokens.** On Artificial Analysis's independent benchmark suite, `max` uses **13x the output tokens** of `low` and **6.8x** those of `medium`, but scores only **+16** and **+7** index points higher. The token cost is not linear in quality. Past `high`, each extra point costs several times more than the one before.
2. **For code, the efficiency knee is `medium` to `high`.** On Anthropic's SWE-bench Pro subset, going from `medium` to `high` costs **$3.20 per extra solved task**. Going from `high` to `xhigh` costs **$32.14 per extra solved task**, ten times as much, for 1.4 more tasks per 100.
3. **Escalating effort only on failures beats running everything at high.** Running at `low` and re-running only the failures at `high` solved about 97% of tasks at about $0.17 per task. Running every task at `high` solved 95.3% at $0.29. That is **better quality for 41% less money**, and it is the cleanest evidence in this folder that blanket high effort is wasteful.
4. **Effort is not the only big lever.** Anthropic says caching "is usually the largest lever in our measurements": the same SWE-bench Pro run cost **3.3x** more without it. Effort is the main lever on *output and thinking* tokens. Caching is the main lever on *input* cost. Both matter.
5. **"Higher effort causes more hallucination" is not established for Claude.** It holds for some models on factual question-answering: GPT-5 mini, o3-mini, gpt-oss-20b, and Gemini 2.5 Flash hallucinate more with longer reasoning. The mechanism is that the model attempts more answers instead of abstaining. But the one Claude model tested (Sonnet 4) showed **no consistent trend**, and Opus 5.5 at `max` ranks **#1** on Artificial Analysis's hallucination-penalizing knowledge benchmark. The documented risk for Claude at high effort is different: *scope creep* and *overthinking*, not invented facts.

## 1. Pricing basis

| Item | Opus 5.5 list price |
|---|---|
| Input | $4 / M tokens |
| Output (including all thinking tokens) | $20 / M tokens |
| Cache write (5 min / 1 h) | $5 / $8 per M |
| Cache read | $0.20 / M (0.05x input) |
| Batch API | 50% off ($2 / $10) |

Source: [What's new in Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5). Thinking is always on and billed as output, so effort changes the bill mainly through the output rate. Output costs 5x input per token.

## 2. Code quality: SWE-bench Pro subset (Anthropic, primary)

Source: [Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence). This is Anthropic's internal subset, so it does not match the public leaderboard. Scores pool two runs, except `xhigh`, which is a single run. `max` was not reported.

| Effort | Solved | Cost/task | Cost/solved | Extra solves vs. previous level (per 100 tasks) | Extra cost (per 100 tasks) | Marginal $ per extra solve |
|---|---|---|---|---|---|---|
| low | 87.4% | $0.11 | $0.126 | n/a | n/a | n/a |
| medium (default) | 92.8% | $0.21 | $0.226 | +5.4 | +$10 | $1.85 |
| high | 95.3% | $0.29 | $0.304 | +2.5 | +$8 | $3.20 |
| xhigh | 96.7% | $0.74 | $0.765 | +1.4 | +$45 | **$32.14** |

**Escalation policies (same source):**

| Policy | Solved | Cost/task |
|---|---|---|
| Everything at `high` | 95.3% | $0.29 |
| `medium`, re-run failures at `high` | ~97% | ~$0.24 |
| `low`, re-run failures at `high` | ~97% | **~$0.17** |

Anthropic notes that "most of the small lift comes from the second attempt, not from the higher effort itself." The cheapest effective setup is to start low, check the result against tests, and escalate only the failures. That requires a verifier (a test suite), which coding tasks usually have.

**Other code results from Anthropic's launch post ([Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)):**
- FrontierCode v1.1: **54.6% at the default (`medium`)** vs. **54.4% at `max`**. Max effort bought nothing measurable.
- CursorBench 4.0: 52.5% at `medium` vs. 57.8% at `max` (+5.3 points). A third-party write-up puts `medium` at about $3 per task and `max` at about $4. That cost figure is not confirmed in the primary source.
- Terminal-Bench 4.0: at its default effort, Opus 5.5 "beats Opus 5 at max effort for about a fifth of the cost."
- **Headline launch numbers are measured at `max`** ("Unless otherwise noted, all Claude Opus 5.5 results use adaptive thinking at max effort"). If you set effort to match the benchmark tables, you pay `max`-level token costs for gains that are often a few points.

**A larger output cap is not always better (same Anthropic docs, internal repository-task benchmark, default effort):** `max_tokens` 64K solved 75.6% at $5.38 per solved task, and 128K solved 68.9% at $5.94. No attempts were truncated at either cap. Both rows are single runs, so treat the gap as noise-prone. It still shows that extra room did not buy quality.

**What "code quality" means here:** every benchmark above measures whether the code *passes the tests*. None measures maintainability, minimal diff size, or style. Anthropic's effort docs describe a qualitative difference: higher effort brings "more comprehensive code comments" and "detailed summaries of changes." At lower effort, Opus 4.7 "scopes its work to what was asked rather than doing more than requested." No public benchmark scores these differences per effort level.

## 3. Tokens and cost across all five levels: Artificial Analysis (independent)

Artificial Analysis runs its own suite of evaluations (the Intelligence Index, which includes coding and agentic tasks such as Terminal-Bench 4.0, SciCode, and FrontierCode 1.1). These are the only independent per-effort numbers found, and the only ones that cover `max`. Pages: [low](https://artificialanalysis.ai/models/claude-opus-5-5-low) · [medium](https://artificialanalysis.ai/models/claude-opus-5-5-medium) · [high](https://artificialanalysis.ai/models/claude-opus-5-5-high) · [xhigh](https://artificialanalysis.ai/models/claude-opus-5-5-xhigh) · [max](https://artificialanalysis.ai/models/claude-opus-5-5).

| Effort | Index | Output tokens (M, whole suite) | Tokens vs. low | Cost/task | Cost vs. low | Index gain vs. previous | Token growth vs. previous | Index points per extra $/task |
|---|---|---|---|---|---|---|---|---|
| low | 42 | 20 | 1.0x | $0.55 | 1.0x | n/a | n/a | n/a |
| medium | 51 | 38 | 1.9x | $1.34 | 2.4x | +9 | +90% | 11.4 |
| high | 54 | 53 | 2.6x | $1.82 | 3.3x | +3 | +39% | 6.2 |
| xhigh | 56 | 100 | 5.0x | $3.46 | 6.3x | +2 | +89% | 1.2 |
| max | 58 | 260 | **13.0x** | $5.98 | **10.9x** | +2 | **+160%** | **0.8** |

How to read it:
- `low`→`medium` is the best spend on the curve: +9 points for +$0.79 per task.
- From `high` to `max`, the model spends **207M more output tokens** (4.9x) and **3.3x the cost per task** for **+4 points**.
- Output speed stays at about 78–95 tokens per second at every level, so extra tokens translate almost directly into extra wall-clock time.
- Artificial Analysis says every effort level sits on the cost/intelligence Pareto frontier. No level is strictly dominated. The question is whether a few extra points are worth 2–5x the spend for your task.
- **Caveats:** "with fallback" means requests blocked by safety classifiers are retried on a fallback model. The index mixes knowledge, reasoning, and coding. Artificial Analysis's per-task cost includes input tokens.

## 4. Where low effort *does* cost quality

Effort sensitivity depends on the task type. From [Anthropic's measurements](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence), comparing `low` to `medium`:

| Task | Time saved at `low` | Score lost at `low` |
|---|---|---|
| SWE-bench Pro (coding) | n/a | −5.4 points |
| HLE (hard knowledge and reasoning) | 30% | −3.4 points |
| DRACO (research) | 84% | **−13.3 points** |
| Internal physics | 47% | **−14.0 points** |

Coding with a test-based verifier tolerates low effort best, because failures can be retried cheaply. Open-ended research and multi-step quantitative reasoning lose the most. This matches the compression-floor finding in [05](05-risks-and-limits.md#1-the-compression-floor-token-complexity): hard problems need their tokens.

## 5. Does higher effort cause more hallucination?

### Evidence that it can

| Source | Finding |
|---|---|
| Zhao, Hooi & Ng, *Test-Time Scaling in Reasoning Models Is Not Effective for Knowledge-Intensive Tasks Yet* ([arXiv:2509.06861](https://arxiv.org/abs/2509.06861), COLM 2026). 14 models; SimpleQA, FACTS Parametric, FRAMES | More reasoning "often increases hallucinations." SimpleQA hallucination rose ~15% for GPT-5 mini (300→3,300 reasoning tokens), and 9%, 12%, and 25% for GPT-5, o3-mini, and gpt-oss-20b. Gemini 2.5 Flash rose >5% on all benchmarks. **Mechanism:** longer reasoning makes the model *attempt* questions it would otherwise skip. 95% of gpt-oss-20b's new hallucinations came from previously unattempted questions. The authors also report a confirmation-bias pattern: extended reasoning reinforces early wrong beliefs and adds fabricated detail |
| OpenAI o3/o4-mini system card (Apr 2025, Table 4) | PersonQA hallucination: o3 **0.33** vs. o1 **0.16**. SimpleQA: o3 0.51 vs. o1 0.44. OpenAI: "o3 tends to make more claims overall, leading to more accurate claims as well as more inaccurate/hallucinated claims." *This compares models, not effort levels* |
| Gema et al., *Inverse Scaling in Test-Time Compute* (TMLR 2025) | With longer reasoning, Claude models grow "increasingly distracted by irrelevant information." That is a reasoning error rather than invented facts, but the same direction |

### Evidence that it doesn't, or that it depends

| Source | Finding |
|---|---|
| Zhao et al. (same paper) | **Claude Sonnet 4: no consistent trend** in hallucination or accuracy, despite thinking length nearly tripling. Grok-3 mini and R1-Distill-Qwen-14B hallucinated *less* with more reasoning, mostly because they abstained more. 4 of 14 models went up, 2 went down, and 8 showed no consistent trend |
| Yao et al., *Are Reasoning Models More Prone to Hallucination?* ([arXiv:2505.23646](https://arxiv.org/abs/2505.23646)) | It depends on post-training. A full pipeline (cold-start SFT + verifiable-reward RL) generally *reduces* hallucination. Distillation-only or RL without SFT increases it |
| Kalai et al. (OpenAI), *Why Language Models Hallucinate* (2025) | Hallucination is driven by training and evaluation incentives that reward guessing over abstaining, not by reasoning length as such |
| [Artificial Analysis AA-Omniscience](https://artificialanalysis.ai/evaluations/omniscience) | Opus 5.5 at **`max`** scores **highest of all models** (index 46, 66% accuracy) on a knowledge benchmark that penalizes wrong answers relative to abstaining. Per-effort values for the other levels were not published |
| [Anthropic launch post](https://www.anthropic.com/claude-opus-5-5) | On grader-checked research reports where "every figure and quote" was checked against sources, 16 of 18 Opus 5.5 reports passed *across effort settings*. Fable 5.1 and Opus 5 passed none. The page does not break this down by effort level |

### Verdict

- **For factual Q&A on some models, yes.** More reasoning → more attempted answers → more confident wrong answers. The cause is answer-willingness, not the thinking itself.
- **For Claude, not shown.** The only Claude model in the per-effort study showed no trend. Opus 5.5 at `max` is the top independent performer on a hallucination-penalizing benchmark. No source measured Opus 5.5's hallucination rate at each effort level, which is a real gap.
- **The documented high-effort risks for Claude are elsewhere:**
  - *Scope creep:* more tool calls, more comments, more summaries, and changes beyond the request ([Effort docs](https://platform.claude.com/docs/en/build-with-claude/effort); Opus 5's tendency to "expand the scope of a task").
  - *Overthinking:* Anthropic says `max` "can lead to overthinking" on structured-output or less intelligence-sensitive tasks (Opus 4.7 guidance).
  - *Distraction:* Claude models in particular were increasingly distracted by irrelevant content as reasoning grew (Gema et al.).
- **Practical defense against hallucination at any effort:** give the model permission to abstain and reward it. Kalai et al. argue that incentivizing guessing is the root cause. Ground answers in retrieved sources, and verify claims against those sources with a grader, as in Anthropic's report test.

## 6. Recommended effort policy for Opus 5.5 (synthesized from the data above)

| Workload | Start at | Escalate when | Evidence |
|---|---|---|---|
| Coding with tests | `low` or `medium` | Tests fail → retry at `high` | Escalation policy: ~97% at $0.17 vs. 95.3% at $0.29 |
| Coding without a verifier | `medium` | Task is hard or long-horizon → `high` | `medium`→`high` costs $3.20 per extra solve. `xhigh` costs $32 |
| Research, synthesis, quantitative reasoning | `medium` | Measured gain → `high` | `low` loses 13–14 points here |
| Classification, extraction, chat, subagents | `low` | Quality check fails | Effort docs; fewer, terser tool calls |
| Frontier problems | `xhigh` / `max` | Only where your evals show a gain | Under 1.2 index points per extra $/task above `high` |

Combine with caching (3.3x cost difference) and the playbook in [06](06-playbook.md).

## Limitations

- Anthropic's numbers are vendor-measured on an internal subset. Artificial Analysis is independent, but it publishes one run per configuration without confidence intervals on these pages.
- The two sources measure different things: SWE-bench pass rate vs. a mixed index. Their cost figures are not comparable with each other.
- No source reports per-effort *token counts* for SWE-bench Pro, or per-effort hallucination rates for Opus 5.5.
- `xhigh` on SWE-bench Pro is a single run, and launch-post comparisons carry ±2.6-point standard errors (Terminal-Bench 4.0).
