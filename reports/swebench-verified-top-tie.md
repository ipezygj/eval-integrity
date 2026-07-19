# The top of the SWE-bench Verified leaderboard is one statistical tie

**Target:** SWE-bench Verified leaderboard (`swe-bench/experiments`, 500 instances)
**Control:** paired McNemar significance test on the #1-vs-#k gap, over the same 500 instances
**Verdict:** the benchmark has power (it separates mid-board) — but the top **8** submissions are mutually indistinguishable, so the displayed rank order among the leaders isn't supported
**Cost:** $0, public data only

## The control

SWE-bench Verified scores an agent as the percentage of the same 500 fixed instances it resolves, and the leaderboard shows a strict rank order. A rank claims #1 is measurably ahead of #2. Because every submission is scored on the **same** instances, the honest test of a #1-vs-#k gap is the **paired** McNemar test on the discordant instances — the ones exactly one of the two agents solves. (Pairing matters: two strong agents both solve the easy instances, so their errors are correlated and an unpaired test overstates the noise. McNemar conditions on the disagreements only.)

## Result

**The top eight submissions are all statistically tied with #1.**

| Rank | Resolved (of 500) | vs #1 (McNemar p) |
|---|---|---|
| 1. sonar-foundation-agent (claude-opus-4-5) | 396 — 79.2% | — |
| 2. livesweagent (claude-opus-4-5) | 396 — 79.2% | 0.868 |
| 3. trae (doubao-seed-code) | 394 — 78.8% | 0.901 |
| 4. openhands (claude-opus-4-5) | 388 — 77.6% | 0.243 |
| 5. livesweagent (gemini-3-pro-preview) | 387 — 77.4% | 0.253 |
| 6. epam-ai-run (claude-4-sonnet) | 384 — 76.8% | 0.156 |
| 7. atlassian-rovo-dev | 384 — 76.8% | 0.134 |
| 8. ACoder | 382 — 76.4% | 0.115 |
| **9. warp** | **378 — 75.6%** | **0.026 ← first separation** |

Every one of ranks 2–8 is within noise of #1 (all p ≥ 0.11); #1 first becomes significant at rank 9 (p = 0.026). So a spread of **2.8 percentage points at the top — eight distinct leaderboard positions — is a single statistical tier.**

## This is specific, not blanket skepticism

The control passes where the data supports it: the benchmark **does** have the power to separate models — #1 pulls clear of the field by rank 9, and the gaps widen further down. SWE-bench Verified is a well-powered benchmark for distinguishing *dissimilar* agents. The issue is narrow and specific: the leaders are now packed into a few points near the top of a 500-item test, and 500 items cannot resolve that packing into an order. "Ranked #1 on SWE-bench Verified" and "ranked #6" are, on this evidence, the same result.

## Honest caveats

- **The tie is a lower bound on the uncertainty.** McNemar treats each submission's single run as fixed, but coding agents are stochastic — re-running the same agent moves several instances. Run-to-run variance is *additional* noise on top of what's tested here, so accounting for it would only make more ranks tie, never fewer.
- Submissions span different dates and harness versions; the comparison assumes "resolved" means the same thing across them (passed the instance's official tests), which is the benchmark's own metric.
- This is about the **presentation of a point rank without uncertainty**, not a claim that any agent is bad or that SWE-bench is a bad benchmark. It is the opposite: the benchmark is good enough that the frontier has compressed against its ceiling.

## Fix

Show a confidence interval or a significance-grouped ordering (tiers) at the top of the leaderboard, so eight teams within one McNemar tie aren't presented — and cited in launch announcements — as eight measurably-different ranks. A single "≈79% ± ~4pp, tier 1" band communicates what the data actually supports.

## Reproduce

[`reproduce/reproduce_swebench_verified_toptie.py`](../reproduce/reproduce_swebench_verified_toptie.py) — pure stdlib, deterministic, no model inference. Downloads the canonical 500 instance IDs and each public `resolved` list from `swe-bench/experiments`, builds pass/fail vectors, and runs paired McNemar. Prints the tables above and `REPRODUCED: the top 8 ... are one statistical tie; #1 first separates at rank 9.`
