# Leaderboards report noise as ranking: a significance-tier audit

**Targets:** BigCodeBench, EvalPlus (HumanEval+/MBPP+), Open LLM Leaderboard v2
**Control:** two-proportion significance test on published pass@1 / accuracy scores, at each benchmark's task count
**Verdict:** NOISY-RANKING on the small-N benchmarks; separable on the large-N ones — a clean sample-size gradient
**Cost:** $0, public data only, no model inference

## The control

A leaderboard prints a strict order. Whether that order is *real* depends on how many items the benchmark has. For each pair of models scored on the same benchmark, a two-proportion test asks whether their score gap is larger than sampling noise at that task count `N`. Models whose gap to #1 is not significant (p ≥ 0.05) are statistically **tied** with the leader. Think of a poll: "Party A leads by 1 point" on 150 respondents is inside the margin of error.

## Result — the sample-size gradient

Running the check across code and reasoning leaderboards, the "can it rank the top?" answer tracks `N` exactly: the minimum detectable gap shrinks as √N grows, and the top flips from *tied* to *separable* right where the arithmetic says it should.

| Benchmark | N (tasks) | #1 | models statistically tied with #1 |
|---|---:|---|---|
| **BigCodeBench-Hard** (complete) | 148 | Gemini-Exp-1206 (40.5%) | **55 of 199** — a quarter of the board |
| **BigCodeBench-Hard** (instruct) | 148 | o3-mini (33.1%) | **62 of 173** |
| HumanEval+ | 164 | O1 Preview (89.0%) | **11 frontier models** — O1, GPT-4o, Claude 3.5, DeepSeek-V3, Qwen2.5-Coder … |
| MBPP+ | 378 | O1 Preview (80.2%) | ~10 |
| Open LLM · IFEval | 541 / 834 | Llama-3.3-70B (90.0%) | clear #1, then **#2–#15 one tier** |
| Open LLM · MUSR | 756 | calme-3.2 (60.2%) | top-15 all one tier |
| BigCodeBench-Full | 1,140 | Gemini-Exp-1206 (62.4%) | ~12 |
| Open LLM · MATH Lvl 5 | 1,324 | AceMath-72B (71.5%) | clear #1, then a tier |
| Open LLM · BBH | ~6,511 | — | #1 separable |
| Open LLM · MMLU-PRO | 12,032 | calme-3.2 (73.0%) | separable at the top |

**BigCodeBench-Hard is the headline:** only 148 tasks, and accuracies near 40% (the region of maximum binomial variance), push the minimum detectable gap to ~16 points — so roughly a quarter of the leaderboard is statistically indistinguishable from #1. On HumanEval+, eleven of the most-discussed frontier models are tied: you cannot say from n=164 which of O1, GPT-4o, and Claude 3.5 is the "best coder."

## Why this is measurement resolution, not a takedown

The **same control** calls the large-N benchmarks *separable* — MMLU-PRO (12,032 items) distinguishes a ~1-point gap; BBH resolves its top. The difference is sample size, not method: the check isn't crying wolf, and the large benchmarks prove it. Small, curated benchmarks (BigCodeBench-Hard, HumanEval+) are valuable *precisely because* they're hard and hand-checked — the price of that curation is that they can't finely *rank* near-matched models.

## Honest caveats

- Each item is treated as one Bernoulli trial (per-item, greedy-decoding scoring), so the two-proportion bound applies directly.
- The "tied with #1" counts use a pairwise two-proportion test (p ≥ 0.05), the rigorous measure — not a looser "within-MDE" band.
- IFEval's score averages prompt-level (n=541) and instruction-level (n=834) accuracy; the tie among #2–#15 is tested at the **larger** N=834 (the hardest test for a "tied" claim) and still holds.
- Task counts confirmed via Hugging Face dataset info: HumanEval+ 164, MBPP+ 378, IFEval 541/834, MUSR 756, BigCodeBench Hard 148 / Full 1,140, MMLU-PRO 12,032.

## Filed publicly

The BigCodeBench finding is filed on the benchmark's own tracker: **[bigcode-project/bigcodebench#121](https://github.com/bigcode-project/bigcodebench/issues/121)**, with an embedded reproduction that recomputes the 55/199 tied count from the public scores.

## Reproduce ($0)

```python
import json, urllib.request, math
d = json.load(urllib.request.urlopen("https://bigcode-bench.github.io/results-hard.json"))
rows = sorted(([k, v["pass@1"]["complete"]] for k, v in d.items()
               if v.get("pass@1", {}).get("complete") is not None), key=lambda r: -r[1])
n, top = 148, rows[0][1]
def two_prop_p(p1, p2, n):
    p = (p1 + p2) / 2 / 100
    se = math.sqrt(p * (1 - p) * 2 / n)
    return math.erfc(abs((p1 - p2) / 100) / se / math.sqrt(2)) if se else 1.0
tied = sum(1 for _, s in rows if two_prop_p(top, s, n) >= 0.05)
print(f"#1 = {rows[0][0]} @ {top}%;  {tied}/{len(rows)} models not significantly different (p>=0.05)")
# -> Gemini-Exp-1206 @ 40.5%;  55/199 models not significantly different (p>=0.05)
```

**Takeaway:** report a significance band or tier grouping alongside a strict rank, at least for small-N benchmarks — otherwise a within-noise pass@1 difference reads as a real ordering.
