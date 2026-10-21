# 06: Playbook, Your Goals Mapped to Evidence-Backed Tactics

Ordered by expected impact and safety. Do the steps in tier order, measuring each one ([07](07-measurement.md)).

## Goal → tactic map

| Your goal | Primary tactic | Evidence | Risk |
|---|---|---|---|
| **Cut circular thinking** | Commit-to-an-approach instruction. Clear stop criteria. Contradiction-free prompts | Thought switching drives wrong, long answers (NeurIPS 2025). Anthropic's commit snippet. OpenAI: contradictions burn reasoning | Low |
| **Cut redundant thinking** | Lower `effort` first. Remove verify and double-check instructions. "Settled answers" line for chat | Over 92% of first solutions already correct (ICML 2025). Opus 5 over-verification (docs). Effort beats prompting (docs) | Low–medium (sweep effort) |
| **More concise thinking** | Right-size `effort` per task class. Per-message effort for routine turns. Concise worked examples | Inverted U (ICLR 2026). Worked examples shape thinking (docs). CoD and SoT principle | Medium on hard math and deduction. Keep high effort there |
| **Cut redundant output and phrasing** | Explicit length and format instructions. No-preamble rule. Narration cadence. Deliverable-length calibration | Effort doesn't shorten visible text on Opus 5 (docs). Verbosity tracks uncertainty (UncertaiNLP 2025) | Low |
| **Structure thinking and processes** | Structure the *process*: plans, checklists, stop criteria, scope rules, effort-scaling rules, subagent caps. Structured Outputs for the final payload only | Anthropic multi-agent effort rules. Format restrictions hurt reasoning (EMNLP 2024). `reasoning_extraction` refusals | Don't template the thinking text |
| **Enhance quality while cutting** | Shrink and focus context. Deferred tool loading. Filter tool output. Effort calibration. Remove distractors | Focused context is more accurate (TACL, ACL, ICML, Chroma). Tool Search raised accuracy. Inverse scaling (TMLR 2025) | Low |

## Tier 1: configuration (no prompt changes, highest return)

1. **Set `effort` explicitly and sweep it.** Run `low`, `medium`, and `high` on a representative eval set. Opus 5.5 defaults to `medium`. Many workloads hold quality at `low` (Anthropic: `low` "comes close" on several coding evals). Use `xhigh` and `max` only where measured.
2. **Route effort by task class.** Example (synthesized; validate on your own data):
   - `low`: classification, extraction, formatting, simple Q&A, routine confirmations, subagents doing narrow lookups
   - `medium`: most coding and knowledge work, agent loops on well-specified tasks
   - `high` or above: hard math and deduction, ambiguous design decisions, long autonomous runs where errors compound
3. **Use per-message effort** (beta) to drop routine turns to `low` without breaking the cache.
4. **Fix caching.** Stable prefix order, a breakpoint on the last stable block, constant top-level effort, 1-hour TTL for intermittent workloads. Verify the hit rate.
5. **Defer tool definitions** (Tool Search) once tools exceed 10K tokens or 10 tools. Prefer CLIs over MCP where they exist.
6. **Enable context editing and compaction** for long agent runs: tool-result clearing with `clear_at_least`, and server-side compaction.
7. **Set `max_tokens` generously and use `task_budget`** (sized from p99 usage) for agent loops, so pacing happens through the countdown and not through truncation.

## Tier 2: prompt hygiene (removals first)

Deletions before additions:

- [ ] Remove "double-check," "verify before responding," "add a verification step," "use a subagent to verify"
- [ ] Remove "think step by step," "explain your reasoning," and `<thinking>`-tag instructions
- [ ] Remove "think carefully before answering" from chat system prompts
- [ ] Remove "CRITICAL / MUST / If in doubt, use X" emphasis
- [ ] Remove contradictory rules (check for pairs of instructions that can't both hold)
- [ ] Remove duplicated instructions and boilerplate. Move workflow-specific blocks into skills or on-demand docs
- [ ] Trim CLAUDE.md to under about 200 lines

## Tier 3: additive instructions (use only what fixes an observed problem)

Use the documented snippets in [04 §4](04-claude-controls.md#4-prompt-level-steering-documented-phrases): commit-to-approach, settled answers, concise responses, deliverable length, narration cadence, subagent damping, correction narration, scope control.

Below is a **(synthesized)** compact system-prompt block that combines the documented principles. It is a starting point to A/B test, not a validated artifact. Keep only the lines that address problems you have measured.

```text
<working_style>
Choose an approach and commit to it; revisit a decision only when new information contradicts it.
Stop exploring once you have enough to act. Do not re-solve a problem you have already solved.
Verify with external checks (tests, tools, sources) when they exist; do not re-read your own work for reassurance.
Delegate to subagents only for large, independent, parallelizable work; never to double-check yourself.
</working_style>

<output_style>
Lead with the answer or outcome. No preamble, no restating the request, no closing recap unless asked.
Keep caveats to one short sentence, and only when they change what the reader should do.
Match length to the question: a sentence for simple questions, structured detail only when the task needs it.
</output_style>
```

Notes on the block:
- Line 3 deliberately keeps *external* verification. Huang et al. (ICLR 2024) show that external feedback is what makes self-correction work.
- Phrasing is positive ("lead with the answer") where possible. Anthropic: "Tell Claude what to do instead of what not to do."
- If your system prompt is long, add a one-line reminder near the end (Anthropic's `<tone_preference>` pattern).
- **Don't** add "keep thinking short." On Sonnet and Haiku 5.5, Anthropic reports prompt instructions don't reliably reduce thinking, and on Opus 5.5 effort is the more reliable lever.

## Tier 4: process structure for agents

1. **Effort-scaling rules in the prompt** (adapted from Anthropic's research system): simple lookups use one agent and 3–10 tool calls. Comparisons use 2–4 subagents. Broad research uses more. Write these rules for your own domain.
2. **Checklist or to-do state** for multi-part tasks. It doubles as the completion condition and prevents re-planning loops.
3. **Explicit stop criteria** (OpenAI's pattern): "stop as soon as you can name the exact change," "stop when the top results converge on one area."
4. **Plan-then-execute** where steps are independent (ReWOO-style batching of tool calls, parallel tool calls). Keep interleaved reasoning where later steps depend on earlier results.
5. **Filter at the source.** Hooks or code that grep logs, page results, or return only the needed rows before the model sees them.
6. **Hard caps:** subagent depth and concurrency limits, `max_budget_usd`, `max_tokens`, and a continuation limit of 2–3 automatic "continue" nudges.

## Tier 5: if you control sampling (API harness)

- When you need multiple samples for reliability, use **early-stopping or adaptive self-consistency** (34–84% fewer samples) or **short-m@k** (first m finishers vote, the rest are cancelled).
- **Route** easy requests to a smaller model or `low` effort with a cheap classifier. This is the same idea the CoD authors suggested ("a router model to decide when to use CoD or CoT").

## Claude Code–specific quick wins

From [Claude Code costs](https://code.claude.com/docs/en/costs):
- `/clear` between unrelated tasks. `/compact <focus>` with custom instructions.
- `/effort` to lower effort for routine work. `/usage` shows attribution and fix-it recommendations.
- Use Sonnet or Haiku for subagents (`model: haiku` in the subagent config).
- Use hooks to filter test and log output. Use skills instead of a bloated CLAUDE.md.
- Write specific prompts ("add validation to login in auth.ts" rather than "improve the codebase") to avoid broad scans.
- Plan mode for complex work prevents expensive rework.

## What *not* to do

- Don't apply flat word or token caps to reasoning (the token-complexity floor).
- Don't force JSON or a rigid template on reasoning. Constrain the final output only.
- Don't remove external verification (tests, compilers).
- Don't change top-level effort or tool definitions mid-conversation. Both invalidate the cache.
- Don't set a task budget below realistic needs. It triggers refusals and early stops.
- Don't judge concise variants with an un-debiased LLM judge.
