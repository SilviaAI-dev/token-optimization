# 03: Context and Input Efficiency

In agentic work, input tokens (the system prompt, tools, history, and tool results resent on every turn) usually exceed output tokens. This is also where cutting tokens most reliably *improves* quality.

## 1. Less context is often more accurate

| Finding | Source (venue) | Key numbers |
|---|---|---|
| Reasoning degrades with input length far below the context limit | Levy, Jacoby & Goldberg, *Same Task, More Tokens* (ACL 2024, Outstanding Paper) | Same question padded from about 250 to 3,000 tokens. Accuracy falls across GPT-4, GPT-3.5, Gemini Pro, and Mixtral |
| Information in the middle is used worst | Liu et al., *Lost in the Middle* (TACL 2024) | U-shaped curve. Accuracy is best when the relevant text is at the start or end |
| Without literal word overlap, long-context retrieval collapses | Modarressi et al., *NoLiMa* (ICML 2025) | At 32K tokens, 11 of 13 models fall below 50% of their short-context score. GPT-4o drops from 99.3% to 69.7%. CoT did not fully fix it |
| Performance gets less reliable as input grows, on all 18 models tested | Chroma, *Context Rot* (2025 industry report) | Focused ~300-token inputs beat full ~113K inputs for every family, with the gap largest for Claude (abstentions). Even one similar distractor hurts. *Note: Chroma sells retrieval infrastructure* |
| Claude in particular is distracted by irrelevant content when reasoning longer | Gema et al. (TMLR 2025) | A named failure mode for Claude models |

Anthropic's framing ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), Sep 2025): context is an "attention budget," and the goal is "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." Opus 5 docs say instruction following stays consistent across its 1M window, but that is about capacity. It does not mean irrelevant tokens are free, and the research above shows they are not.

## 2. Caching: the biggest cost lever that leaves quality untouched

From [Anthropic prompt caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching):

| Item | Value |
|---|---|
| Cache read price | **0.05x** base input on Opus 5.5 and Sonnet 5.5 (0.1x on most others, 0.025x on Fable 5.1) |
| Cache write | 1.25x (5-minute TTL) or 2x (1-hour TTL) |
| Minimum cacheable prefix | 512 tokens on Opus 5.5 |
| Prefix order | `tools` → `system` → `messages`. A change at any level invalidates it and everything after it |
| Silent invalidators | Changing tool definitions; editing the system prompt; **changing top-level `effort` or the thinking config**; toggling web search; adding or removing images; non-deterministic key order in tool-use JSON |

Practical rules:
- Put stable content first. Put the breakpoint on the last block that is identical across requests, never on a timestamp or the incoming user message.
- Keep effort constant within a cached conversation. To change it, use **per-message effort** (beta on Opus 5.5), which keeps the cache.
- Use the 1-hour TTL for workloads that come back every 5–60 minutes.
- Check hits: `cache_read_input_tokens` should dominate. Claude Code's `/usage` shows a cache hit line.

## 3. Tool loading and tool results

| Technique | Source | Token effect | Quality effect |
|---|---|---|---|
| **Tool Search Tool** (deferred tool definitions) | Anthropic, Nov 2025 | ~77K → ~8.7K context (−85%) | Opus 4: 49→74%. Opus 4.5: 79.5→88.1% on MCP evals |
| **Programmatic tool calling** (Claude writes code that calls the tools) | Anthropic, Nov 2025 | 43,588 → 27,297 average (−37%) | Knowledge retrieval 25.6→28.5%. GIA 46.5→51.2% |
| **MCP as code APIs** with filtering in a sandbox | Anthropic, Nov 2025 | 150K → 2K (−98.7%) in the Drive→Salesforce example | Needs secure sandboxing and adds operational overhead |
| **Tool use examples** | Anthropic, Nov 2025 | Small added cost | Complex parameter accuracy 72→90% |
| **Prefer CLIs over MCP** where possible | [Claude Code costs](https://code.claude.com/docs/en/costs) | CLIs add no per-tool listing to context | n/a |
| **Hooks that filter output** (e.g., grep test failures) | Claude Code costs | "tens of thousands of tokens to hundreds" | Less noise for the model |

Use Tool Search when tool definitions exceed 10K tokens or there are 10 or more tools. Skip it for small, always-used toolsets.

## 4. Managing long histories

| Mechanism | What it does | Notes |
|---|---|---|
| **Server-side compaction** (`compact_20260112`) | Summarizes history near the limit | Anthropic's recommended primary strategy. Keeps decisions and open bugs, drops redundant output |
| **Tool-result clearing** (`clear_tool_uses_20250919`) | Replaces old tool outputs with placeholders | Set `clear_at_least` so a clear is worth the cache rebuild. Use `exclude_tools` for results that must stay |
| **Thinking-block clearing** (`clear_thinking_20251015`) | Drops old thinking blocks | Newer models keep all thinking by default, and kept thinking is billed as input on later turns. Clearing breaks the cache at the clear point |
| **Memory tool / structured notes** | Persists state outside the context window | Pair with clearing: Claude is warned to save notes before results are cleared |
| **Subagents** | Run verbose work in an isolated context and return a 1–2K-token summary | Each subagent's requests still cost tokens, so use it to isolate context, not to double-check work |
| **`/clear` between unrelated tasks** (Claude Code) | Fresh context | Free. `/compact` itself is a large request |

**Opus 5.5 constraint:** keep the history append-only. Editing earlier messages, rebuilding `system` or `tools`, or summarizing old turns in place between requests invalidates later thinking blocks. Put such changes in mid-conversation system messages or server-side context management ([prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), migration section).

## 5. Prompt compression (for documents you don't control)

| Method | Venue | Result |
|---|---|---|
| LLMLingua | EMNLP 2023 | Up to 20× compression with minimal loss, using a small LM to drop low-information tokens |
| LongLLMLingua | ACL 2024 | +21.4% on NaturalQuestions at about 4× fewer tokens (GPT-3.5). −94% cost on LooGLE |
| LLMLingua-2 | Findings of ACL 2024 | Task-agnostic. 3–6× faster than LLMLingua, with 1.6–2.9× end-to-end speedup at 2–5× compression |

These suit RAG and long-document pipelines. For instructions you write yourself, editing by hand works better: delete contradictions, duplicates, and "CRITICAL/MUST" emphasis that newer Claude models over-apply.

## 6. System prompt hygiene

- Anthropic says to start minimal on the best model, then add instructions only for failures you observe. Aim for the "right altitude," between brittle if-else rules and vague platitudes.
- Use a few canonical examples, not an exhaustive list of edge cases.
- Keep CLAUDE.md under about 200 lines. Move workflow-specific instructions into skills, which load on demand ([Claude Code costs](https://code.claude.com/docs/en/costs)).
- Remove leftover aggressive language from older models. Opus 4.5 and later "may now overtrigger. The fix is to dial back any aggressive language."
- Remove contradictions. OpenAI documents that a careful instruction-follower burns reasoning tokens reconciling them.
