# 04: Claude Opus 5.5 Controls (Documented Behavior)

All statements below come from Anthropic's platform docs as of October 2026 unless marked otherwise. Links: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) · [Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost) · [Prompting Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) · [Prompting Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) · [Best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) · [Task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets).

## 1. Effort: the primary control

- Set via `output_config.effort`: `low` | `medium` | `high` | `xhigh` | `max`.
- **Opus 5.5 defaults to `medium`.** Opus 5 and earlier default to `high`, so a request that omits effort runs one level lower on 5.5.
- It affects **all** output tokens: thinking, text, tool calls. "Lower effort also means fewer and terser tool calls."
- It is a behavioral signal, not a budget. "At lower effort levels, Claude still thinks on sufficiently difficult problems."
- Calibration: "Claude Opus 5.5 at `medium` matches or exceeds Claude Opus 5 at `high` on coding and knowledge-work evaluations, and on several coding evaluations `low` comes close to it at much lower cost."
- Anthropic's advice: "To get less thinking, lower the effort level first. Lowering effort reduces thinking, and with it cost and latency, more reliably than prompt instructions do."
- Reserve `xhigh` and `max` for measured gains. On Opus 4.7, Anthropic noted `max` "can lead to overthinking" on structured-output or less intelligence-sensitive tasks.
- Opus 5.5 "tends to think more per turn than Claude Opus 5" at a given level, especially at `xhigh` and `max`. **Re-sweep effort instead of carrying old settings over.**

| Effort | Tool-use behavior (docs) |
|---|---|
| Lower | Combines operations into fewer calls, goes straight to action without preamble, terse confirmations |
| Higher | More calls, explains the plan first, detailed summaries, more code comments |

**Caveat on visible length:** on Opus 5, effort "does not reliably shorten responses, so prompt for length instead." Treat effort as the *thinking* lever and prompting as the *visible output* lever.

### Per-message effort (beta, keeps the cache)

Header `mid-conversation-output-config-2026-07-01`. Insert `{"role":"system","content":[],"output_config":{"effort":"low"}}` before the next user turn. Use it to drop to `low` for routine follow-ups and raise effort for planning steps without invalidating the prompt cache. A top-level effort change does invalidate it.

## 2. Thinking on Opus 5.5

- **Always on and adaptive.** Sending `thinking: {"type":"disabled"}` returns a 400 error. `budget_tokens` returns a 400 error on 4.7 and later.
- The model decides per request. Simple questions may get no thinking block at all.
- Thinking per request "tends to decrease as a conversation grows longer."
- `display`: `omitted` (default, empty text), `summarized`, or `updates` (beta). **Billing is identical in every mode.**
- Kept thinking blocks from earlier turns are billed as input on later turns.

## 3. Hard and soft caps

| Control | Type | Scope | Notes |
|---|---|---|---|
| `max_tokens` | Hard | Per request (thinking plus text) | Truncates with `stop_reason: "max_tokens"`. Size it generously at high effort. Anthropic used 128K for agentic coding on Opus 5.5 |
| `task_budget` (beta `task-budgets-2026-03-13`) | Soft | A whole agentic turn across requests | The model sees a countdown and paces itself. Minimum 20K. **Too small a budget causes refusal-like behavior, aggressive scoping-down, or early stops.** Start from the p99 of measured usage. Set it once, because mutating it breaks the cache |
| Time budget line (`elapsed 340s / 1200s`) | Soft | Multi-agent harness | Opus 5.5 "pays close attention" to elapsed time. Teams finished sooner at comparable quality. A tighter budget mostly increases parallelism rather than cutting work |

## 4. Prompt-level steering (documented phrases)

All snippets below are **(Anthropic docs, verbatim)**.

**Think less often (system prompt):**
```text
Extended thinking adds latency and should only be used when it
will meaningfully improve answer quality, typically for problems
that require multistep reasoning. When in doubt, respond directly.
```

**Per message:** append `"Answer directly without deliberating."` to discourage thinking, or `"Please think hard before responding."` to encourage it.

**Stop re-thinking settled answers in chat (Opus 5.5):**
```text
Once you have answered something, treat that answer as done. On later turns, focus your thinking on what the user is asking now, and don't go back over an earlier answer unless the user asks about it or points out a problem with it.
```
Anthropic reports this cut follow-up thinking without hurting quality. It is *not* recommended for long analyses or agentic tasks where later steps can reveal earlier mistakes.

**Remove "think carefully" lines from chat prompts (Opus 5.5):** removing them "made replies start sooner, with no clear decline in the quality of the reply."

**Commit to an approach (anti-circular):**
```text
When you're deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning. If you're weighing two approaches, pick one and see it
through. You can always course-correct later if the chosen approach fails.
```

**Concise responses (Opus 5):**
```text
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```
In long system prompts, add a short reminder near the end: `<tone_preference>Keep outputs reasonably concise.</tone_preference>`

**Written deliverables:**
```text
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

**Agent narration:**
```text
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

**Subagent damping:**
```text
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```
Hard caps in Claude Code and the Agent SDK: `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, `max_budget_usd`.

**Correction narration:**
```text
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

**Scope control:**
```text
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

**Overengineering (Opus 4.5/4.6 era, still useful):** "Avoid over-engineering. Only make changes that are directly requested or clearly necessary..." See the [best practices page](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) for the full block.

## 5. Things to remove from older prompts

| Remove | Why (docs) |
|---|---|
| "Double-check your answer," "re-verify before responding," "include a final verification step," "use a subagent to verify" | Opus 5 already self-verifies. These cause over-verification, which "adds cost without improving results" |
| "Think step by step" or asking for reasoning in the response | Can trigger `reasoning_extraction` refusals on Opus 5 and 5.5. Use summarized thinking blocks instead |
| "CRITICAL: You MUST use this tool when..." / "If in doubt, use [tool]" | Causes overtriggering on Opus 4.5 and later |
| Rules telling the model not to think | Ineffective on 5.5 and increase tag leakage on Opus 5 |
| Prefills | Return 400 on 4.6 and later |

## 6. How to shape *how* Claude thinks (the legitimate route)

You cannot dictate the format of thinking blocks, and asking for reasoning in the response risks refusals. The documented levers:

1. **Effort** sets depth and frequency.
2. **Worked examples:** "Multishot examples work with thinking. Worked examples in your prompt shape how Claude approaches similar problems in its own thinking blocks. Present each example as a problem, the method to apply, and the expected answer." Concise worked examples are the sanctioned way to get Chain-of-Draft-style compactness into thinking. The effect on thinking length is not separately measured in Anthropic's docs, so test it.
3. **Decision policies** such as commit-to-an-approach, treat-settled-answers-as-done, and stop criteria. These govern *what* the reasoning does without dictating its text.
4. **Interleaved-thinking guidance:** "After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding." Use it when quality after tool use matters more than tokens.
5. **Clear success criteria and stop conditions** (OpenAI's guide makes the same point: "Get enough context fast... stop as soon as you can act").

## 7. Cross-vendor agreement

| Principle | Anthropic | OpenAI | Google |
|---|---|---|---|
| A built-in effort or budget knob is the primary control | `effort` | `reasoning.effort` (minimal through xhigh) | `thinkingLevel` / `thinkingBudget` (dynamic by default) |
| Don't prompt reasoning models with "think step by step" | Rely on thinking and lower effort instead | "Avoid chain-of-thought prompts" | Dynamic thinking by default |
| Control output length separately from reasoning | Prompt for length (effort doesn't reliably shorten text) | `text.verbosity` parameter plus natural-language overrides | n/a |
| Simple, direct, non-contradictory prompts | "Right altitude," dial back aggressive language | "Keep prompts simple and direct." Contradictions waste reasoning tokens | n/a |
| Explicit exploration and stop criteria for agents | Effort-scaling rules in prompts, subagent caps | `<context_gathering>` with early-stop criteria and tool-call budgets | n/a |
