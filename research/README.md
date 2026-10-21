# Token Optimization for Claude: Research

Research into cutting token use in large reasoning models (Claude Opus 5.5 is the main target) while keeping or improving output quality. Compiled 2026-10-21.

## How to read this folder

| File | What it covers |
|---|---|
| [01-where-tokens-go.md](01-where-tokens-go.md) | How Opus 5.5 spends tokens, and the kinds of waste that research has documented |
| [02-reasoning-efficiency-literature.md](02-reasoning-efficiency-literature.md) | Academic evidence on overthinking, concise reasoning, and early stopping, plus what training-time fixes show |
| [03-context-and-input-efficiency.md](03-context-and-input-efficiency.md) | Input-side waste: long-context degradation, prompt compression, caching, tool loading, compaction |
| [04-claude-controls.md](04-claude-controls.md) | Controls Anthropic documents for Opus 5.5 (effort, adaptive thinking, task budgets, steering phrases), with their exact behavior |
| [05-risks-and-limits.md](05-risks-and-limits.md) | Where compression hurts quality, and what it costs in safety and monitorability |
| [06-playbook.md](06-playbook.md) | Prioritized recommendations that map each of your goals to evidence-backed tactics, with prompt snippets |
| [07-measurement.md](07-measurement.md) | How to measure whether an optimization actually worked |
| [08-effort-cost-analysis.md](08-effort-cost-analysis.md) | Opus 5.5 cost, token, and code-quality data at every effort level, plus the evidence on effort and hallucination ([data](data/), [script](analysis/effort_cost.py)) |
| [sources.md](sources.md) | Full bibliography with venue, peer-review status, and the discrepancies found while cross-checking |

## Bottom line

1. **More thinking is not reliably better.** Accuracy follows an inverted U against reasoning length. Peer-reviewed results show this in several ways: an ICLR 2026 paper on CoT length, a TMLR 2025 Anthropic-affiliated paper finding inverse scaling in test-time compute, and a *Scientific Reports* analysis of o1/o3-mini. Past the peak, extra tokens add cost and lower accuracy. Wrong answers are on average longer than right ones (the NeurIPS 2025 underthinking paper and the Hassid et al. and Su et al. preprints).
2. **Most reasoning waste comes from three patterns:** (a) more solution rounds after a correct answer is already found, where over 92% of first rounds were correct (ICML 2025); (b) frequent switching between half-explored approaches, the "circular" pattern, where wrong answers used 225% more tokens and switched thoughts 418% more often (NeurIPS 2025); (c) reflexive "Wait / Hmm" self-checks, whose removal cut 27–51% of tokens with no meaningful loss (EMNLP 2025 Findings).
3. **On Opus 5.5, `effort` is the first lever, not prompting.** Anthropic's docs say lowering effort reduces thinking "more reliably than prompt instructions do." Opus 5.5 defaults to `medium`, which Anthropic reports matches or beats Opus 5 at `high`. Thinking is always on and cannot be disabled.
4. **Prompting still matters for the visible output and the agent loop.** Documented wins include: removing legacy "double-check / verify" instructions, which cause over-verification; a "commit to an approach" instruction; a "treat earlier answers as settled" instruction for chat; explicit length calibration for written deliverables; and caps on subagent spawning.
5. **Input tokens are usually the larger bill in agentic work.** Prompt caching (reads cost 0.05x on Opus 5.5), deferred tool loading (85% fewer tool-definition tokens, with higher accuracy), code-execution filtering (150K→2K tokens in Anthropic's example), context editing and compaction, and shorter CLAUDE.md files all cut tokens without touching reasoning quality. Shorter, focused context also *raises* accuracy (TACL 2024, ACL 2024, ICML 2025, Chroma).
6. **Compression has a floor.** Each problem has a minimum token count it needs, and accuracy collapses below it. Aggressive prompts such as Chain of Draft lost up to 25 points zero-shot on Claude 3.5 Sonnet, and concise CoT lost 27.7% on math with GPT-3.5. The goal is *adaptive* length: short on easy problems, full depth on hard ones. A uniform squeeze misses that.
7. **Do not try to force a format on the thinking itself.** On Opus 5.5, prompts that push the model to reproduce its reasoning in the response can be declined (`reasoning_extraction` refusal category). Shape thinking through effort, worked examples (which Anthropic says carry over into thinking), and decision-policy instructions such as "commit to an approach." Prescribing a thinking template does not work this way.

## Evidence standards used

- Every quantitative claim names its source. Peer-reviewed venues (ICLR, ICML, NeurIPS, ACL/EMNLP, TACL, TMLR, COLM, *Nature*, *Scientific Reports*) are marked as such. Preprints and vendor docs are labeled.
- Where two sources disagree, or a paper's own numbers conflict, the discrepancy is recorded in [sources.md](sources.md#cross-check-notes).
- Claims about Opus 5.5 come from Anthropic's own platform documentation, current as of October 2026. Results measured on older models (Claude 3.5 Sonnet, GPT-4o, R1-distills) are labeled with the model, because behavior does not carry over between models automatically.
- Snippets marked **(Anthropic docs, verbatim)** are quoted from official documentation. Snippets marked **(synthesized)** are this research's own wording, built from the cited evidence, and need validation on your workload.
