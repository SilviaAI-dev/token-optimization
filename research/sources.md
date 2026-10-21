# Sources

Status key: **PR** = peer-reviewed venue · **WS** = peer-reviewed workshop · **Pre** = preprint · **Doc** = official vendor documentation · **Eng** = vendor engineering or research blog · **Ind** = industry technical report.

Accessed 2026-10-21.

## Reasoning length and efficiency

| # | Source | Status | Used for |
|---|---|---|---|
| 1 | Chen et al., *Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs*. [arXiv:2412.21187](https://arxiv.org/abs/2412.21187) · [ICML 2025](https://icml.cc/virtual/2025/poster/45540) | PR | Overthinking, efficiency metrics, >92% first-round correct, ~45% reduction |
| 2 | Wang et al., *Thoughts Are All Over the Place: On the Underthinking of o1-Like LLMs*. [arXiv:2501.18585](https://arxiv.org/abs/2501.18585) · [NeurIPS 2025](https://neurips.cc/virtual/2025/poster/117581) | PR | Thought switching (225% / 418%), TIP decoding penalty |
| 3 | Wu et al., *When More is Less: Understanding Chain-of-Thought Length in LLMs*. [arXiv:2502.07266](https://arxiv.org/abs/2502.07266) · [ICLR 2026](https://iclr.cc/virtual/2026/poster/10011380) | PR | Inverted U, optimal length scaling, simplicity bias |
| 4 | Gema et al., *Inverse Scaling in Test-Time Compute*. [arXiv:2507.14417](https://arxiv.org/abs/2507.14417) · [TMLR 2025](https://mlanthology.org/tmlr/2025/gema2025tmlr-inverse) · [Anthropic blog](https://alignment.anthropic.com/2025/inverse-scaling) | PR | Longer reasoning lowers accuracy, Claude distraction, safety behavior shifts |
| 5 | Ballon et al., *The relationship between reasoning and performance in LLMs: o3 (mini) thinks harder, not longer*. *Scientific Reports* ([Consensus link](https://consensus.app/papers/details/d10b82e215385dbd85e0bdbbaa3a98d5/)) | PR | Accuracy declines with chain length even controlling for difficulty |
| 6 | Sprague et al., *To CoT or not to CoT?* [arXiv:2409.12183](https://arxiv.org/abs/2409.12183) · [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ead542f13a38179d1b55b88610f959a1-Abstract-Conference.html) | PR | CoT helps mainly math and symbolic tasks; apply it selectively |
| 7 | Su et al., *Between Underthinking and Overthinking*. [arXiv:2505.00127](https://arxiv.org/abs/2505.00127) | Pre | Overthinks easy, underthinks hard; wrong answers longer |
| 8 | Hassid et al., *Don't Overthink it. Preferring Shorter Thinking Chains*. [arXiv:2505.17813](https://arxiv.org/abs/2505.17813) | Pre | Shorter chains up to 34.5% more accurate; short-m@k |
| 9 | Ma et al., *Reasoning Models Can Be Effective Without Thinking*. [arXiv:2504.09858](https://arxiv.org/abs/2504.09858) | Pre | NoThinking wins at matched budgets |
| 10 | Lee, Che & Peng, *How Well do LLMs Compress Their Own Chain-of-Thought? A Token Complexity Approach*. [arXiv:2503.01141](https://arxiv.org/abs/2503.01141) | Pre | Compression floor; prompts far from optimal |
| 11 | Renze & Guven, *The Benefits of a Concise Chain of Thought*. [arXiv:2401.05618](https://arxiv.org/abs/2401.05618) | Pre | −48.7% length; −27.7% on math (GPT-3.5) |
| 12 | Xu et al., *Chain of Draft: Thinking Faster by Writing Less*. [arXiv:2502.18600](https://arxiv.org/abs/2502.18600) | Pre | CoD results and zero-shot and small-model failures |
| 13 | Aytes, Baek & Hwang, *Sketch-of-Thought*. [arXiv:2503.05179](https://arxiv.org/abs/2503.05179) · [EMNLP 2025](https://preview.aclanthology.org/setup/2025.emnlp-main.1236) | PR | Up to 84% fewer tokens with routed sketch styles |
| 14 | Han et al., *Token-Budget-Aware LLM Reasoning* (TALE). [arXiv:2412.18547](https://arxiv.org/abs/2412.18547) · [Findings of ACL 2025](https://preview.aclanthology.org/new-sigs/2025.findings-acl.1274/) | PR | Budget-in-prompt: ~67% fewer tokens, <3% loss |
| 15 | Ning et al., *Skeleton-of-Thought*. [ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/03d7e13f0092405804f3a381ade8f3f0-Abstract-Conference.html) | PR | Outline-then-parallel latency gains |
| 16 | Xu et al., *ReWOO*. [arXiv:2305.18323](https://arxiv.org/abs/2305.18323) | Pre | Plan-first tool use: 5× token efficiency on HotpotQA |
| 17 | Wang et al., *Wait, We Don't Need to "Wait"!* (NoWait). [arXiv:2506.08343](https://arxiv.org/abs/2506.08343) · Findings of EMNLP 2025 | PR | −27–51% CoT by suppressing reflection tokens |
| 18 | Yang et al., *Dynamic Early Exit in Reasoning Models* (DEER). [arXiv:2504.15895](https://arxiv.org/abs/2504.15895) · [ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/8df90a1440ce782d1f5607b7a38f2531-Abstract-Conference.html) | PR | Confidence-based early exit |
| 19 | NEAT: Neuron-Based Early Exit for LRMs. [arXiv:2602.02010](https://arxiv.org/abs/2602.02010) | Pre | Independent check showing DEER degrades on Qwen3 |
| 20 | Mao et al., *Early Stopping Chain-of-thoughts in LLMs* (ES-CoT). Via [Consensus](https://consensus.app/papers/details/80b032728ab852288dd3d734d39a86cb/) | Pre | −16% tokens via answer convergence |
| 21 | Muennighoff et al., *s1: Simple test-time scaling*. [arXiv:2501.19393](https://arxiv.org/abs/2501.19393) · [EMNLP 2025](https://preview.aclanthology.org/credits/2025.emnlp-main.1025) | PR | Budget forcing in both directions |
| 22 | Li et al., *Escape Sky-high Cost: Early-stopping Self-Consistency*. [ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/3fe2a777282299ecb4f9e7ebb531f0ab-Abstract-Conference.html) | PR | 34–84% fewer samples |
| 23 | Aggarwal et al., *Let's Sample Step by Step: Adaptive-Consistency*. [EMNLP 2023](https://preview.aclanthology.org/setup/2023.emnlp-main.761) | PR | Up to 7.9× fewer samples |
| 24 | Aggarwal & Welleck, *L1: Controlling How Long A Reasoning Model Thinks With RL*. [arXiv:2503.04697](https://arxiv.org/abs/2503.04697) · COLM 2025 | PR | Length-controlled RL |
| 25 | Munkhbat et al., *Self-Training Elicits Concise Reasoning*. [arXiv:2502.20122](https://arxiv.org/abs/2502.20122) · [Findings of ACL 2025](https://preview.aclanthology.org/credits/2025.findings-acl.1289) | PR | −30% tokens with self-generated short chains |
| 26 | Fatemi et al., *Concise Reasoning via Reinforcement Learning*. [arXiv:2504.05185](https://arxiv.org/abs/2504.05185) | Pre | Verbosity as an RL artifact |
| 27 | Zhang et al., *AdaptThink: Reasoning Models Can Learn When to Think*. [arXiv:2505.13417](https://arxiv.org/abs/2505.13417) · [EMNLP 2025](https://preview.aclanthology.org/setup/2025.emnlp-main.184) | PR | −53% length and +2.4% accuracy by choosing when to think |
| 28 | Li et al., *AALC: Adaptive Accuracy-Length Control*. Via [Consensus](https://consensus.app/papers/details/2c2a2f56560359a5b6bb59efdb620647/) | Pre | Interpretability cost of compression |
| 29 | Guo et al. (DeepSeek-AI), *DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning*. *Nature* 2025, [doi:10.1038/s41586-025-09422-z](https://www.nature.com/nature-index/article/10.1038/s41586-025-09422-z) | PR | RL-driven length growth and emergent reflection |
| 30 | Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*. [ICLR 2024](https://iclr.cc/virtual/2024/poster/18956) | PR | Intrinsic self-correction is weak |
| 31 | Sui et al., *Stop Overthinking: A Survey on Efficient Reasoning for LLMs*. [arXiv:2503.16419](https://arxiv.org/abs/2503.16419) · [TMLR 2025](https://mlanthology.org/tmlr/2025/sui2025tmlr-stop/) | PR | Taxonomy |
| 32 | Wang et al., *Harnessing the Reasoning Economy*. [arXiv:2503.24377](https://arxiv.org/abs/2503.24377) | Pre | Dynamic allocation framing |

## Output verbosity and evaluation

| # | Source | Status | Used for |
|---|---|---|---|
| 33 | Zhang, Das & Zhang, *Verbosity ≠ Veracity: Demystify Verbosity Compensation Behavior of LLMs*. [arXiv:2411.07858](https://arxiv.org/abs/2411.07858) · [UncertaiNLP 2025](https://preview.aclanthology.org/setup/2025.uncertainlp-main.14) | WS | Verbosity signals uncertainty; −27.6 points on Qasper |
| 34 | Dubois et al., *Length-Controlled AlpacaEval*. [arXiv:2404.04475](https://arxiv.org/abs/2404.04475) | Pre (COLM 2024 listing not verified) | LLM-judge length bias |
| 35 | Tam et al., *Let Me Speak Freely? Format Restrictions and LLM Performance*. [arXiv:2408.02442](https://arxiv.org/abs/2408.02442) · EMNLP 2024 Industry | PR | Strict formats degrade reasoning |

## Context and input

| # | Source | Status | Used for |
|---|---|---|---|
| 36 | Levy, Jacoby & Goldberg, *Same Task, More Tokens*. [ACL 2024](https://aclanthology.org/2024.acl-long.818) | PR | Degradation well below context limits |
| 37 | Liu et al., *Lost in the Middle*. [TACL 2024](https://aclanthology.org/2024.tacl-1.9.pdf) | PR | Position effects |
| 38 | Modarressi et al., *NoLiMa*. [ICML 2025](https://proceedings.mlr.press/v267/modarressi25a.html) | PR | Non-literal long-context retrieval collapse |
| 39 | Chroma, *Context Rot*. [trychroma.com/research/context-rot](https://www.trychroma.com/research/context-rot) | Ind | 18-model degradation; focused vs. full input |
| 40 | Jiang et al., *LLMLingua*. EMNLP 2023 · [project](https://www.microsoft.com/en-us/research/project/llmlingua/) | PR | 20× compression |
| 41 | Jiang et al., *LongLLMLingua*. [ACL 2024](https://aclanthology.org/2024.acl-long.91) | PR | Long-context compression |
| 42 | Pan et al., *LLMLingua-2*. [Findings of ACL 2024](https://preview.aclanthology.org/new-sigs/2024.findings-acl.57.bib) | PR | Fast task-agnostic compression |

## Faithfulness and monitorability

| # | Source | Status | Used for |
|---|---|---|---|
| 43 | Chen et al. (Anthropic), *Reasoning Models Don't Always Say What They Think*. [Anthropic](https://www.anthropic.com/research/reasoning-models-dont-say-think) · [arXiv:2505.05410](https://arxiv.org/abs/2505.05410) | Eng / Pre | CoT faithfulness 25% / 39% |
| 44 | Korbak et al., *Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety*. [arXiv:2507.11473](https://arxiv.org/abs/2507.11473) | Pre (position paper) | Monitorability caution |

## Vendor documentation and engineering posts

| # | Source | Status |
|---|---|---|
| 45 | Anthropic, [Effort](https://platform.claude.com/docs/en/build-with-claude/effort) | Doc |
| 46 | Anthropic, [Steering thinking (cost, pricing, steering)](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost) | Doc |
| 47 | Anthropic, [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Doc |
| 48 | Anthropic, [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) | Doc |
| 49 | Anthropic, [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) | Doc |
| 50 | Anthropic, [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | Doc |
| 51 | Anthropic, [Task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets) | Doc |
| 52 | Anthropic, [Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing) | Doc |
| 53 | Anthropic, [Claude Code: Manage costs effectively](https://code.claude.com/docs/en/costs) | Doc |
| 54 | Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (Sep 2025) | Eng |
| 55 | Anthropic, [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) (Nov 2025) | Eng |
| 56 | Anthropic, [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) (Nov 2025) | Eng |
| 57 | Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (Jun 2025) | Eng |
| 58 | Anthropic, [The "think" tool](https://www.anthropic.com/engineering/claude-think-tool) (Mar 2025; Dec 2025 note recommends extended thinking instead) | Eng |
| 59 | OpenAI, [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices) | Doc |
| 60 | OpenAI, [GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) | Doc |
| 61 | Google, [Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking) | Doc |

## Effort cost analysis and hallucination (file 08)

| # | Source | Status | Used for |
|---|---|---|---|
| 62 | Anthropic, [What's new in Claude Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5) | Doc | Pricing ($4/$20, cache $0.20), always-on thinking |
| 63 | Anthropic, [Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence) | Doc (vendor-measured) | Per-effort SWE-bench Pro subset, escalation policies, caching 3.3x, low-vs-medium deltas, max_tokens experiment |
| 64 | Anthropic, [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5) | Eng (vendor-measured) | Headline benchmarks at max; FrontierCode and CursorBench at medium; grader-checked reports |
| 65 | Artificial Analysis, Opus 5.5 model pages ([low](https://artificialanalysis.ai/models/claude-opus-5-5-low), [medium](https://artificialanalysis.ai/models/claude-opus-5-5-medium), [high](https://artificialanalysis.ai/models/claude-opus-5-5-high), [xhigh](https://artificialanalysis.ai/models/claude-opus-5-5-xhigh), [max](https://artificialanalysis.ai/models/claude-opus-5-5)) | Ind (independent) | Per-effort index, output tokens, cost per task, speed |
| 66 | Artificial Analysis, [AA-Omniscience](https://artificialanalysis.ai/evaluations/omniscience) | Ind | Opus 5.5 max ranks #1 on the hallucination-penalizing knowledge index |
| 67 | Zhao, Hooi & Ng, *Test-Time Scaling in Reasoning Models Is Not Effective for Knowledge-Intensive Tasks Yet*. [arXiv:2509.06861](https://arxiv.org/abs/2509.06861) · COLM 2026 | PR | Per-model hallucination vs. reasoning length; abstention mechanism; Claude Sonnet 4 shows no trend |
| 68 | OpenAI, [o3 and o4-mini System Card](https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf) (Apr 2025), Table 4 | Doc | PersonQA and SimpleQA hallucination rates; "makes more claims" |
| 69 | Yao et al., *Are Reasoning Models More Prone to Hallucination?* [arXiv:2505.23646](https://arxiv.org/abs/2505.23646) | Pre | Hallucination depends on the post-training pipeline |
| 70 | Kalai, Nachum, Vempala & Zhang (OpenAI), *Why Language Models Hallucinate* (2025). [IAS abstract](https://www.ias.edu/node/310786) | Pre | Incentives to guess as the root cause |

## Agentic token consumption and skills

| # | Source | Status | Used for |
|---|---|---|---|
| 71 | Bai, Huang, Wang, Sun, Mihalcea, Brynjolfsson, Pentland & Pei, *How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks*. [arXiv:2604.22750v3](https://arxiv.org/abs/2604.22750v3) (Oct 2026) | Pre | Input and cache-read dominance; repeated file actions; non-monotonic accuracy vs. cost; 30x run variance; poor self-prediction of cost; per-model token gaps (files 01, 05, 06, 08) |
| 72 | Gao, Li, Yuanyuanyuan, Ji, Ma & Wang, *SkillReducer: Optimizing LLM Agent Skills for Token Efficiency*. [arXiv:2603.29919v1](https://arxiv.org/abs/2603.29919v1) (Mar 2026) | Pre | Skill bloat statistics; 39–75% compression with a quality gain; example-as-specification failure mode (files 01, 03, 06) |

## Cross-check notes

Discrepancies and caveats found while verifying:

- **Chen et al. (#1):** the introduction claims a 48.6% reduction on MATH500, but the results table implies about 45% for FCS+Reflection. This research uses about 45%.
- **DEER (#18):** the authors report gains on R1-distills, but independent work (#19) finds AIME24 drops from 61.1 to 45.6 on Qwen3-8B. Gains are model-dependent.
- **Sketch-of-Thought (#13):** arXiv v1 reports 76% over 15 datasets, and the EMNLP version reports up to 84% over 18. This research uses the published figure.
- **LongLLMLingua (#41):** LooGLE cost reduction is 94.0% in the ACL and arXiv versions and 94.2% on the ICLR abstract page.
- **Think tool (#58):** the post's text says 0.570 vs. 0.370 on τ-bench airline, while its table says 0.584 vs. 0.332. Anthropic now recommends extended thinking over the think tool in most cases, so it is not used in recommendations.
- **Tool Search (#56):** the post cites both ~55K tokens (58 tools, five servers) and ~77K→8.7K in its comparison. Both reflect different setups described in the post.
- **NoLiMa (#38):** the arXiv version reports 10 of 12 models below 50% at 32K; the ICML version reports 11 of 13. This research uses the ICML figures.
- **Chroma (#39):** not peer-reviewed, and the vendor has a commercial interest in retrieval. Its findings agree with the peer-reviewed #36–38.
- **Length-Controlled AlpacaEval (#34):** commonly cited as COLM 2024, but that could not be confirmed from primary sources here, so it is marked as a preprint.
- **Let Me Speak Freely (#35):** a single study. Results are directional.
- **Chain of Draft (#12):** the headline "7.6% of tokens" is a best case. Its own zero-shot Claude 3.5 Sonnet result is a 25-point accuracy drop.
- **Opus 5.5 CursorBench cost per task (#64):** third-party blogs cite about $3 (medium) and $4 (max) per task. These figures were not found in Anthropic's primary post and are marked unconfirmed in file 08. One blog's "$0.50–$1.35 per task" range for Artificial Analysis conflicts with Artificial Analysis's own pages ($0.55–$5.98) and is not used.
- **FrontierCode (#64):** medium (54.6%) scores slightly above max (54.4%), as Anthropic reported it. That is within noise, and it is cited as "no measurable gain."
- **Artificial Analysis per-effort Omniscience (#66):** only the max entry's values were visible, so per-effort hallucination rates for Opus 5.5 remain unknown.
- **Bai et al. (#71):** the abstract says runs on the same task differ by "up to 30x" in tokens, while the Figure 2(b) caption says the most expensive run averages about 2x the cheapest per model. The two figures describe the extreme and the typical case and are not reconciled in the paper. Agentic-vs-chat multipliers appear as "1000x" in the abstract and as 3500x and 1200x in the text.
- **SkillReducer (#72):** the SkillsBench token figures cover 84 of 87 tasks, with three unexplained exclusions. SkillsBench was at ceiling (86 of 87 passed with no skill), so the +2.8% gain comes from the 600-skill Gate 2 evaluation, not SkillsBench. The arXiv page also lists a v2 (Jun 2026); this research cites v1 as requested.
- **Transfer to Opus 5.5:** most academic results use open models (R1-distills, QwQ, Qwen) or older closed models. Only Anthropic's docs (#45–53) describe Opus 5.5 behavior directly. Treat academic magnitudes as directional for Claude.
