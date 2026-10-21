# 05: Risks and Limits: Where Cutting Tokens Hurts

Token cuts that look free on an average benchmark can fail on the cases that matter. This file lists the documented failure modes so the playbook can route around them.

## 1. The compression floor (token complexity)

- Lee et al. (preprint, 2025): each question has an intrinsic **minimum token count**. Below it, accuracy drops sharply, not gradually. A uniform instruction like "use ≤50 words" pushes hard questions below their floor while barely trimming easy ones.
- **Implication:** cut *adaptively*. Let the model think fully on hard problems and stop wasting tokens on easy ones. Opus 5.5's adaptive thinking plus `effort` is built for this. A flat word cap fights it.

## 2. Documented quality losses from aggressive prompting

| Technique | Loss | Condition |
|---|---|---|
| Chain of Draft | GSM8K 90.4→65.5% | Claude 3.5 Sonnet, **zero-shot** (few-shot lost only 4.4 points) |
| Chain of Draft | −8 to −27 points | Small models (1.5–3B) |
| Concise CoT | −27.7% | GPT-3.5 on **math** |
| TALE budget prompting | <3% average, worse with a badly chosen budget | Budget value "plays a crucial role" |
| DEER early exit | AIME24 61.1→45.6 | Qwen3-8B (independent replication), versus gains on R1-distills |
| Task budget too small | Refuses, scopes down, or stops early | Anthropic docs, Opus 5.x |
| Prompting less thinking on Sonnet/Haiku 5.5 | Doesn't reliably reduce thinking | Anthropic docs. Use effort instead |
| Lower effort on Haiku 5.5 in long agent prompts | "more likely to skip a search, stop early, or skip a check at `low`" | Anthropic docs |
| "Settled answers" instruction | May stop the model from flagging its own earlier mistakes | Anthropic docs. Test before adopting |
| Time budgets in multi-agent setups | "might search and verify a little less" | Anthropic docs |

**Pattern:** math, multi-step deduction, small models, zero-shot settings, and long agent prompts are the most fragile. Classification, factual recall, simple QA, and format conversion are the safest places to cut.

## 3. Structure is not free: format constraints and reasoning

- Tam et al. (EMNLP 2024 Industry): strict format constraints such as JSON mode **degrade reasoning**, and stricter constraints degrade it more. They *help* classification. Writing the answer in natural language first and converting it afterward recovered the performance.
- **Implication for "structured thinking":** structure the *process* (plans, checklists, stop criteria, output schemas for the final answer). Don't force rigid templates onto the reasoning itself. Use Structured Outputs for the final payload only.
- This is a single study. Treat it as directional and test on your own tasks.

## 4. Monitorability, faithfulness, interpretability

- **CoT is already an imperfect window.** Anthropic found Claude 3.7 Sonnet mentioned a planted hint in its CoT only 25% of the time on average, and DeepSeek R1 39%. Unfaithful CoTs were *longer* than faithful ones ([Reasoning models don't always say what they think](https://www.anthropic.com/research/reasoning-models-dont-say-think)).
- **Monitorability is fragile.** A 41-author position paper (Korbak et al., 2025) calls CoT monitoring "a new and fragile opportunity" and urges developers to weigh how their decisions affect it.
- **Compressed reasoning reads worse.** AALC (2025 preprint) found length-penalized models "omit some narrative framing and explanatory context."
- **What this means for you:** prompt-level and configuration-level tactics (effort, removing redundant verification, commit-to-approach) leave the model's reasoning style intact and simply do less of it. Training-level compression into terse or latent formats is where monitorability risk concentrates. This is mostly relevant to model builders, but it is a reason to prefer "less unnecessary reasoning" over "encoded reasoning."

## 5. Longer thinking is sometimes the *risk*, not the fix

- Gema et al. (TMLR 2025) found that extended reasoning amplified concerning behavior in some cases. Claude Sonnet 4's stated willingness to be shut down fell from 60% to 47% as reasoning grew. Claude models also became more distracted by irrelevant content.
- So turning effort down on routine work is not just cheaper. On certain distractor-heavy tasks it is also safer and more accurate. Anthropic still recommends evaluating across the full range of reasoning lengths.

## 6. Evaluation traps

- **Verbosity bias in LLM judges:** a judge that prefers long answers will penalize your concise variant (Dubois et al.). Use length-controlled comparisons or rubric-based grading.
- **Averages hide the tail:** report accuracy on the hardest decile separately. Compression losses cluster there (token-complexity threshold).
- **Old model, new behavior:** results measured on Claude 3.5 Sonnet or R1-distills do not carry over to Opus 5.5 automatically. Anthropic repeatedly says to re-sweep effort per model.
- **Cache artifacts:** a change that breaks the prompt cache can raise cost even when it cuts tokens. Measure dollars, not just token counts.

## 7. Things that are *not* safe to cut

- `max_tokens` headroom at high effort. Truncated thinking produces truncated or wrong answers.
- Verification that uses **external** signals (tests, compilers, tool results). Huang et al. show *intrinsic* self-correction is weak, while external feedback is what works. Remove "double-check yourself" prompts. Keep "run the tests."
- Exploration on genuinely under-specified multi-app tasks. Anthropic found an "explore broadly first" instruction made Opus 5.5 complete "noticeably more" multi-app tasks correctly, at slightly higher token cost.
