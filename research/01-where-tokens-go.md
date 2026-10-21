# 01: Where the Tokens Go

## The four token streams in an Opus 5.5 request

| Stream | Billed as | What drives it | Main levers |
|---|---|---|---|
| **Thinking** | Output tokens, billed in full even when the visible thinking is summarized or omitted | Effort level, problem difficulty, prompt wording, conversation length | `effort`, `max_tokens`, task budgets, steering phrases |
| **Visible output** | Output tokens | Model verbosity defaults, prompt style, preambles and recaps, narration during agent loops | Length instructions, format instructions, effort (partly) |
| **Fresh input** | Input tokens | System prompt, tool definitions, documents, tool results | Caching, deferred tool loading, filtering, compaction |
| **Re-read input** | Cache reads (0.05x on Opus 5.5) or full input on a miss | Every turn of an agent loop resends the whole history | Cache hygiene, context editing, `/clear`, subagents |

Key facts from Anthropic's docs ([Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)):

- Thinking is billed in full. "The billed output token count does **not** match the visible token count in the response." Read `usage.output_tokens_details.thinking_tokens` to see the reasoning share.
- On Opus 5.5, thinking is always on and adaptive. The model decides per request whether to think and how much, guided by `effort`.
- In a tool loop, "the first request after new user input typically carries most of the reasoning." Follow-ups that only process tool results can skip thinking.
- Agentic work multiplies everything. Anthropic measured agents at about 4x the tokens of chat, and multi-agent systems at about 15x ([multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)). Claude Code agent teams in plan mode use about 7x the tokens of a standard session ([Claude Code costs](https://code.claude.com/docs/en/costs)).

## A taxonomy of waste, with the evidence for each

### 1. Overthinking: solving an already-solved problem again

- **Evidence:** Chen et al. (ICML 2025) found that o1-style models produce 2–4 solution rounds in most cases (76–80% of instances for QwQ-32B), while "in more than 92% of cases, the initial round of solutions produces the correct answer." They define *outcome efficiency*: tokens generated after the first correct answer count as waste.
- **Scale:** Training models to stop at the first correct solution plus one reflection cut about 45% of tokens on MATH500 with accuracy essentially unchanged (93.0→92.8).
- **Trigger:** Overthinking is worst on easy problems. Su et al. (2025 preprint) show models "overthink simple problems... and underthink harder ones."

### 2. Circular thinking, or underthinking: abandoning paths too early

This is what most people mean by "circular" reasoning. The model hops between approaches without finishing any of them, then comes back.

- **Evidence:** Wang et al. (NeurIPS 2025): on incorrect answers, o1-style models used **225% more tokens** than on correct answers, driven by **418% more frequent thought switching**.
- **Fix that improved accuracy:** A decoding penalty on thought-switch tokens (TIP) *raised* accuracy (e.g., GPQA Diamond 57.6→59.1) while cutting switches from 21.1 to 7.3.
- **Prompt-level analogue (Anthropic docs):** "choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning."

### 3. Reflexive self-verification

- **Evidence:** NoWait (Findings of EMNLP 2025) suppressed "Wait" and "Hmm" tokens at inference time and cut CoT length by 27–51% across five R1-style model series and ten benchmarks, with no meaningful loss in utility.
- **Intrinsic self-correction rarely helps:** Huang et al. (ICLR 2024) found that without external feedback, models "struggle to improve" their reasoning answers and sometimes get worse after self-correction.
- **Opus-specific:** Anthropic's docs say Opus 5 "verifies its own work without being told to," and that explicit verification instructions "cause over-verification... removing them reduces wasted tokens with no loss in quality."

### 4. Verbose output: padding, hedging, preambles, recaps

- **Verbosity often signals uncertainty, not care:** Zhang et al. (UncertaiNLP 2025) found "verbosity compensation" (restating the question, hedging, long enumerations) in all 14 LLMs tested. GPT-4 did it 50.4% of the time. Verbose answers scored up to 27.6 points worse, and the gap did not shrink as models got more capable.
- **Evaluators reward length:** Dubois et al. showed that LLM judges prefer longer outputs, and that controlling for length raised AlpacaEval's correlation with human Chatbot Arena rankings from 0.94 to 0.98. A system tuned against an un-debiased LLM judge will drift toward verbosity.
- **Opus 5 specifically:** "default user-facing responses run longer than prior Opus models'," and "effort controls how much the model thinks rather than how much it says." Written files are also longer, and narration during agent loops is heavier.

### 5. Over-exploration and over-delegation in agents

- Anthropic's early multi-agent system "spawned 50 subagents for simple queries." The fix was explicit effort-scaling rules in the prompt (simple fact-finding: one agent, 3–10 tool calls).
- Anthropic's docs say Opus 5 "delegates to subagents more readily than prior models... it multiplies cost and time when applied to small tasks."
- Legacy "if in doubt, use [tool]" prompts cause overtriggering on newer models.

### 6. Context bloat

- Tool definitions alone can consume about 55K tokens (five MCP servers, 58 tools) before the conversation starts ([advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)).
- Raw intermediate results pass through the model. One 2-hour transcript copied between tools costs about 50K extra tokens ([code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)).
- Bloat also costs accuracy, not just money (see [03](03-context-and-input-efficiency.md)). Chroma found focused ~300-token inputs beat full ~113K-token inputs for every model family tested.
- Skills are often padded. Of 55,315 public agent skills, 26.4% have no routing description, and over 60% of skill-body content is background, examples, or templates rather than actionable rules (Gao et al., *SkillReducer*, 2026 preprint).

### 6b. Agentic coding: input re-reads and repeated file actions dominate

Bai et al. (*How Do AI Agents Spend Your Money?*, 2026 preprint) analyzed OpenHands trajectories from eight models on SWE-bench Verified, four runs per problem:
- Agentic coding uses about **1000x** more tokens than code reasoning or code chat. **Input tokens drive the cost, even with caching.** For Sonnet 4.5, cache reads are the largest token *and* dollar category in every phase, despite output costing about 80x more per token.
- Exploring the code and writing the fix make up about two-thirds of agent rounds (30.4% and 33.5%). Input-heavy rounds come from tool results such as file views and test output.
- **Expensive runs are redundant runs.** Higher-cost runs show sharply more repeated views and edits of the same file. For Qwen3-Coder, Sonnet 4, and Kimi-K2, about 50% of file actions repeat on a file already touched.
- Runs on the same task can differ by up to 30x in total tokens, and expert difficulty ratings barely predict cost (Kendall τ = 0.32).
- Model choice matters: Sonnet 4.5 and Kimi-K2 averaged over 1.5M more tokens per task than GPT-5 on the same tasks, including tasks every model solved.

### 7. Contradictory or vague instructions

- OpenAI's GPT-5 guide says the model "expends reasoning tokens searching for a way to reconcile the contradictions." One user found that removing the contradictions "drastically streamlined and improved" performance. The mechanism (careful instruction-followers burning reasoning tokens on conflicts) plausibly applies to Claude, which Anthropic describes as following system prompts closely. That transfer is an inference: no source tested it on Claude.

## Why the waste exists

- **RL training pushes toward length.** Fatemi et al. (2025 preprint) argue that PPO/GRPO losses on *incorrect* answers drive policies toward verbosity, so lengthening is "an optimization artifact" rather than a sign of better reasoning. DeepSeek-R1 (*Nature* 2025) documents response length growing steadily during RL, along with emergent reflection behavior.
- **Models misjudge difficulty.** The optimal reasoning length grows with task difficulty and *shrinks* with model capability (Wu et al., ICLR 2026). Models do not calibrate well on their own (Su et al.).
- **Better models already use fewer tokens.** Ballon et al. (*Scientific Reports*) found that o3-mini beat o1-mini "without requiring longer reasoning chains," and that accuracy declines as chains grow, even after controlling for difficulty. Anthropic reports that Opus 5.5 "tends to finish the same task with fewer tokens" than Opus 5. Part of the problem is getting solved at the model level. The rest is configuration and prompting.
