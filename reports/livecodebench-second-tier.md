# LiveCodeBench's #1 is real — but ranks 2–6 are one statistical tie

**Target:** LiveCodeBench code-generation leaderboard (`livecodebench.github.io`, 28 models × 1,055 problems)
**Control:** paired t-test on per-problem pass@1 differences (matches the leaderboard's own mean-pass@1 metric)
**Verdict:** the top rank is genuinely separated (the benchmark has the power) — but five different models below it are presented as ranks 2–6 while sitting in a single statistical tier
**Cost:** $0, public data only

## Why this one is a positive control

The point of a significance control is that it must *pass where the data supports the ranking* — otherwise it's just leaderboard nihilism. LiveCodeBench is the counter-example that proves the method isn't that. It publishes a dense per-problem grid (28 models scored on the same 1,055 problems), and 1,055 items is enough sample size to resolve a real top gap. So here the control **certifies** the #1:

- **#1 O4-Mini (High) — 87.30 mean pass@1 — genuinely leads.** #1 vs #2 gap is +2.56 points, paired t **p = 0.010**. This is a real separation, not a coin flip. (Contrast: on SWE-bench Verified, n=500 could not separate its top 8 at all — see [that report](swebench-verified-top-tie.md). Same method, opposite and correct verdict, because the sample sizes differ.)

## The finding: a five-way tie for second

Immediately below the real #1, five distinct leaderboard positions are one statistical group:

| Rank | Model | mean pass@1 | vs #2 (paired t p) |
|---|---|---|---|
| 1 | O4-Mini (High) | 87.30 | *(tier 1 — separated, p=0.010)* |
| 2 | O3 (High) | 84.74 | — |
| 3 | O4-Mini (Medium) | 84.45 | 0.778 |
| 4 | DeepSeek-R1-0528 | 84.36 | 0.674 |
| 5 | Gemini-2.5-Pro-06-05 | 84.27 | 0.647 |
| 6 | Gemini-2.5-Pro-05-06 | 82.75 | 0.050 |
| **7** | OpenReasoning-Nemotron-32B | 80.96 | **<0.001 (tier 3)** |

Ranks 2–6 — O3, O4-Mini (Medium), DeepSeek-R1, and both Gemini-2.5-Pro snapshots — are mutually indistinguishable (all #2-vs-#k p ≥ 0.05). The whole top 10 collapses to just **three statistical tiers**: {#1}, {#2–#6}, {#7–#10}. So "ranked 2nd" and "ranked 6th" on LiveCodeBench code-gen are, on this evidence, the same result — five labs separated on the board by differences their shared 1,055-problem sample cannot establish.

## Honest caveats

- The paired t-test is on per-problem pass@1 (each problem's mean over the sampled generations), which is exactly what the leaderboard averages — so this tests the displayed metric directly, not a proxy.
- The analysis uses the full published problem grid, not a per-model date-contamination window; date-windowing changes absolute scores but the same-problems paired comparison between two models remains valid on whatever set both were scored on.
- This is about the **presentation of adjacent ranks without uncertainty**, not a claim that any model is weak. The #1 result is explicitly credited as real.

## Fix

Group the leaderboard into significance tiers (or show a CI on mean pass@1). "Tier 1: O4-Mini High; Tier 2: O3 / O4-Mini Med / DeepSeek-R1 / Gemini-2.5-Pro (×2)" tells the reader what the 1,055-problem sample actually supports — and, unlike a strict 1–2–3–4–5–6 order, it doesn't invite five teams to each claim a distinct rank.

## Reproduce

[`reproduce/reproduce_livecodebench_second_tier.py`](../reproduce/reproduce_livecodebench_second_tier.py) — pure stdlib, deterministic, no model inference. Downloads the public per-problem grid, builds the 28×1,055 matrix, ranks by mean pass@1, and runs the paired t-test tier structure. Prints the tables above and `REPRODUCED: #1 is a real lead (p=0.010); ranks 2-6 are one statistical tie (5 models).`
