# RewardBench's per-category #1 rankings are inside the noise

**Target:** RewardBench v1 per-category leaderboard (`allenai/reward-bench-results`)
**Control:** paired McNemar significance test on the displayed #1-vs-#2 gap, per category
**Verdict:** the *aggregate* ranking is well-powered and sound — but none of the four per-category #1 slots is distinguishable from #2 on its own sample
**Cost:** $0, public data only

## The control

A leaderboard that shows a strict order is making a claim: #1 is measurably ahead of #2. That claim is testable. Because every model is scored on the **same** items, the honest test of a #1-vs-#2 gap is the **paired** McNemar test on the discordant items — the cases where exactly one of the two models is right. (An unpaired two-proportion test is *conservative* here: the two models' per-item errors are strongly correlated, so ignoring the pairing inflates the standard error. McNemar is strictly more powerful, so a tie under McNemar is a real tie, not a weak-test artifact.)

## Result

**On its own sample, RewardBench cannot separate the displayed #1 from #2 in any of the four categories.**

| Category | #1 (acc) | #2 (acc) | discordant b / c | McNemar p | Rank supported? |
|---|---|---|---|---|---|
| **Chat** (n=358) | internlm2-7b-reward (0.992) | internlm2-20b-reward (0.989) | 4 / 3 | **1.000** | no — a coin flip |
| **Chat Hard** (n=456) | Skywork-Gemma-2-27B (0.899) | Skywork-Llama-3.1-8B (0.884) | 30 / 23 | 0.410 | no |
| **Safety** (n=740) | Skywork-Gemma-2-27B (0.930) | Skywork-Llama-3.1-8B (0.927) | 29 / 27 | 0.894 | no |
| **Reasoning** (n=1431) | Skywork-Gemma-2-27B (0.973) | URM-LLaMa-3.1-8B (0.964) | 39 / 26 | 0.137 | no |

## This is specific, not blanket skepticism

The point of the control is that it *passes* where the data supports the ranking. The **aggregate** RewardBench ranking has the sample size to discriminate: the overall #1 (Skywork-Gemma-2-27B) beats #2 at **p = 0.048** and #3 at **p = 0.008**, and the overall top-10 spans **7 distinct statistical tiers** with only three adjacent ties. The ~2,985-item headline metric separates most models fine. It is only the **per-category** sub-rankings — measured on 358–1,431 near-ceiling items — that their smaller samples cannot support. So this is not "RewardBench is a bad benchmark"; the headline is sound, and the per-category point-ranks are simply presented with more precision than their samples carry.

## The pattern partially recurs on RewardBench 2

Repeating the paired test on **RewardBench 2** (`allenai/reward-bench-2-results`) over the verified top models: **4 of the 6 category #1 slots are tied with #2** (Focus p=0.50, Math p=1.00, Safety p=1.00, Ties p=0.50), while two are real — the #1 genuinely leads on Factuality (p=0.016) and Precise IF (p<0.001). The newer benchmark *narrows* the problem but does not remove it.

## Honest caveats

- This is about the **presentation of a point ranking without uncertainty**, not a data bug and not a claim that any model is bad. Consumers who read "#1 on Safety" as "measurably the best reward model for safety" are reading signal that isn't in the data.
- The RewardBench 2 check was verified over the strong top candidates rather than all 188 models; the category leaders are near-ceiling, so the true top-2 are very likely captured, but a full sweep could shift a borderline pair.

## Fix

For the per-category columns, publish confidence intervals or a significance-grouped ordering (tiers/letters) rather than a strict integer rank — so "#1 on Safety" isn't read as a measurable lead when #1-vs-#2 is a coin flip.

## Filed publicly

**[allenai/reward-bench#269](https://github.com/allenai/reward-bench/issues/269)** — with a self-contained, pure-stdlib reproduction ([`reproduce/reproduce_rewardbench_category_ties.py`](../reproduce/reproduce_rewardbench_category_ties.py)) that downloads the public per-example results, aligns the two models item-by-item within each category, runs paired McNemar, and prints every figure above. Deterministic, no model inference.
