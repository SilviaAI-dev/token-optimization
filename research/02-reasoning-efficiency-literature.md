# 02: Reasoning Efficiency, What the Literature Shows

Organized by how much access you need. **A** = prompt only (usable with Claude today). **B** = inference-time control of decoding or sampling (needs open weights, or a sampling harness you control). **C** = training (needs weights). For Claude users only category A applies directly. B and C explain *why* A works and show where the frontier is heading.

## 1. Length vs. accuracy: the core findings

| Finding | Source (venue) | Key numbers |
|---|---|---|
| Accuracy is an inverted U in CoT length. The optimal length rises with difficulty and falls with model capability | Wu et al., *When More is Less* (ICLR 2026) | Theory plus controlled experiments. RL drives models toward shorter CoT as accuracy improves ("simplicity bias") |
| Longer reasoning can lower accuracy (inverse scaling) | Gema et al., *Inverse Scaling in Test-Time Compute* (TMLR 2025; Anthropic Fellows) | Five failure modes. Claude models in particular grow "increasingly distracted by irrelevant information." Every model tested loses track of constraints in long deduction |
| Accuracy declines as chains grow, even controlling for difficulty. Stronger models are not longer | Ballon et al. (*Scientific Reports*) | o3-mini (m) beats o1-mini without longer chains. o3-mini (h) gains marginally by spending far more tokens, including on problems (m) already solves |
| Wrong answers are longer | Su et al. 2025 (preprint); Wang et al. (NeurIPS 2025) | Shortest sample already correct on >80% of questions (R1-Preview on GSM8K and MATH). Wrong answers use 225% more tokens |
| Shorter chains for the same question are more accurate | Hassid et al. 2025 (Meta FAIR, preprint) | Up to 34.5% more accurate than the longest sampled chain. Fine-tuning on short chains beat training on long ones |
| CoT mainly helps math and symbolic tasks | Sprague et al., *To CoT or not to CoT* (ICLR 2025) | Meta-analysis of 100+ papers plus 20 datasets × 14 models. On MMLU, direct answers ≈ CoT unless the problem has an "=" sign. Recommends using CoT selectively |
| Skipping the thinking phase can win at matched budgets | Ma et al., *Reasoning Models Can Be Effective Without Thinking* (preprint) | At 700 tokens on ACM23: 51.3 vs 28.9. Uses 2.0–5.1× fewer tokens and matches pass@k as k grows |

**Implication:** the target is *calibrated* reasoning, not minimal reasoning. Wasted tokens sit mostly on easy and medium problems, and in the tail after the answer is found.

## 2. Category A: prompt-only methods

| Method | Source | Result | Caveat |
|---|---|---|---|
| **Concise CoT** ("be concise") | Renze & Guven 2024 (preprint) | −48.7% length, negligible impact overall (GPT-3.5/4, multiple choice) | **−27.7% on math** for GPT-3.5 |
| **Chain of Draft** ("≤5 words per step") | Xu et al. 2025 (Zoom; preprint) | Claude 3.5 Sonnet, few-shot: GSM8K 95.8→91.4% with 190→40 tokens. Sports 93.2→97.3% with 189→14 tokens | **Zero-shot Claude 3.5 Sonnet GSM8K: 90.4→65.5%.** Needs hand-written few-shot examples, and small models lose 8–27 points. Authors: "CoD is not a replacement for CoT" |
| **Sketch-of-Thought** (routes among three compressed styles) | Aytes et al. (EMNLP 2025) | Up to 84% fewer tokens across 18 datasets with minimal loss. Accuracy *improved* on some math and multi-hop tasks | Uses a trained router to pick the style |
| **Token-budget prompting** (TALE-EP) | Han et al. (Findings of ACL 2025) | About 67% fewer tokens with <3% accuracy loss | The budget value "plays a crucial role." A badly chosen budget backfires |
| **Compression instructions in general** | Lee et al., *Token Complexity* (preprint) | A single tradeoff curve holds across "be concise," "≤10 words," "no punctuation," and similar | Each question has a threshold token count. Below it accuracy collapses. Prompt methods sit "far from" the theoretical optimum, so **adaptive** length is the open opportunity |
| **Plan first, then fill in in parallel** (Skeleton-of-Thought) | Ning et al. (ICLR 2024) | Latency speed-up across 12 LLMs, with quality gains on some question types | A latency win, not a token win. Not suited to step-dependent reasoning |
| **Plan all tool calls up front** (ReWOO) | Xu et al. 2023 (preprint) | 5× token efficiency and +4% accuracy on HotpotQA vs. interleaved ReAct | Brittle when a later step depends on an earlier result |

**Note on reasoning models.** These studies mostly used *visible* CoT on non-reasoning models (GPT-4o, Claude 3.5 Sonnet). On Opus 5.5 the reasoning sits in adaptive thinking blocks. Anthropic warns that prompts asking the model to write its reasoning out "may be declined." So port the *principle* of each method (concise steps, a budget, a plan first), not the literal "write a draft per step" output format. See [04](04-claude-controls.md) and [05](05-risks-and-limits.md).

## 3. Category B: decoding and sampling interventions

| Method | Source | Result |
|---|---|---|
| **NoWait** (suppress "Wait" and "Hmm") | Wang et al. (Findings of EMNLP 2025) | −27–51% CoT length across five model series, no meaningful loss |
| **Thought-switch penalty** (TIP) | Wang et al. (NeurIPS 2025) | Fewer switches and *higher* accuracy (e.g., MATH500-Hard 83.1→83.7) |
| **Dynamic early exit** (DEER: stop when a trial answer is confident) | Yang et al. (ICLR 2026) | −19–80% length with +0.3–5.0% accuracy on R1-distills. **Independent replication on Qwen3 is weaker:** AIME24 61.1→45.6 (NEAT, 2026 preprint) |
| **ES-CoT** (stop when step answers converge) | Mao et al. 2025 (preprint) | −16% tokens at comparable accuracy |
| **Budget forcing** (cut off, or append "Wait" to extend) | Muennighoff et al., *s1* (EMNLP 2025) | Extending thinking raised AIME24 from 50% to 57%. The same knob works in both directions |
| **Early-stopping self-consistency** | Li et al. (ICLR 2024) | Samples cut by 34–84% at comparable accuracy (e.g., GSM8K −80%) |
| **Adaptive-consistency** | Aggarwal et al. (EMNLP 2023) | Up to 7.9× fewer samples, <0.1% accuracy drop |
| **short-m@k** (sample k in parallel, vote over the first m to finish) | Hassid et al. 2025 | Up to 40% fewer thinking tokens than majority voting with equal or better accuracy. Up to 33% less wall time |

**Can you apply these to Claude?** Partly, through the harness:
- If you sample several times for reliability, use early-stopping or adaptive consistency rather than a fixed N.
- short-m@k works through the API: send k parallel requests, take the first m that finish, cancel the rest, and vote.
- Token-level suppression (NoWait, TIP) is not available through the API. The prompt-level stand-ins are the "commit to an approach" instruction and removing verification prompts ([06](06-playbook.md)).

## 4. Category C: training-time methods (context only)

| Method | Source | Result |
|---|---|---|
| Length-controlled RL (LCPO / L1) | Aggarwal & Welleck (COLM 2025) | Precise length control from the prompt. A 1.5B model beats GPT-4o at equal reasoning length |
| Self-training on the model's own short chains | Munkhbat et al. (Findings of ACL 2025) | −30% output tokens at equal accuracy across five model families |
| Training to stop at the first correct solution | Chen et al. (ICML 2025) | About −45% tokens with accuracy preserved |
| Two-phase RL for concision | Fatemi et al. 2025 (preprint) | Length reduced while accuracy held or improved. Argues verbosity is an RL artifact |
| Learning *when* to think (AdaptThink) | Zhang et al. (EMNLP 2025) | −53% length *and* +2.4% accuracy (1.5B). Skips thinking more on easy sets, keeps it on AIME |
| Accuracy-aware length reward (AALC) | Li et al. 2025 (preprint) | Over 50% shorter at equal accuracy. **Notes reduced interpretability:** models drop narrative and explanatory context |

**Takeaway for Claude users:** AdaptThink's result (shorter *and* more accurate by deciding when to think) is the same design idea as Anthropic's adaptive thinking plus `effort`. Users get the benefit by configuring effort correctly and not fighting the adaptive mechanism with blanket "think carefully" instructions ([04](04-claude-controls.md)).

## 5. Surveys for further reading

- Sui et al., *Stop Overthinking: A Survey on Efficient Reasoning for LLMs* (TMLR 2025). Taxonomy: model-based, reasoning-output-based, and input-prompt-based methods.
- Wang et al., *Harnessing the Reasoning Economy* (2025 preprint). System 1 vs. System 2 framing, with an emphasis on dynamic compute allocation over uniform compression.
