# Eval Integrity Report

> **SAMPLE / SALES COLLATERAL.** A real audit of a public leaderboard, produced to demonstrate the
> Eval Integrity service. Every number was recomputed from public data (Appendix A). No client
> commissioned it and no data was fabricated. Free to share.
>
> Fourth in the sample set, and the first about **statistical power** rather than a judge/label
> pathology: is a leaderboard *ranking* even distinguishable from noise on the sample it was
> measured on?

---

## 1. Engagement header

| Field | Value |
|---|---|
| Engagement type | Single Headline Claim (statistical power) |
| Target | **Open LLM Leaderboard v2** — the GPQA sub-score ranking |
| Report date | 2026-07-18 |
| Tooling | `power_audit.py` (reproduce/power_audit.py) |
| Determinism | No RNG; every figure is a pure function of the two published accuracies + the sample size. |

### Claim under audit

| # | Claim (as implied by the leaderboard) | Metric | Values | Source |
|---|---|---|---|---|
| C1 | The top-ranked model outranks the second on GPQA — its higher GPQA score reflects genuinely stronger graduate-level reasoning. | GPQA accuracy | rank 1 = **47.06%**, rank 2 = **46.90%** (a **+0.16pp** lead that sets the top rank) | `open-llm-leaderboard/contents` (HF), field `GPQA Raw`, all 4,576 rows |

---

## 2. Overall verdict

**Overall: UNDERPOWERED**

The gap that determines the top ranking (**+0.16pp**) is **not statistically
distinguishable from noise** at any plausible GPQA sample size (p = 0.94 at n = 1,192). The ranking is real on the page;
its *statistical basis* is not.

---

## 3. Finding

### Claim C1 — the #1 GPQA ranking

GPQA is a small benchmark (the Diamond subset is **198** questions; the full leaderboard task, even
combining Main/Diamond/Extended subsets, is on the order of ~1,200). At those sizes, a couple of
percentage points is inside the sampling noise. The table below audits a **3.69pp** gap as a
two-proportion comparison across every plausible GPQA `n`. That gap is not the top-rank gap — see the
correction note at the end — but it is retained here because it is the *harder* case: the real
top-rank gap is 0.16pp and fails to separate by a wider margin at every `n` in the table.

| GPQA n | observed diff | p-value | MDE at this n | verdict |
|---:|---:|---:|---:|---|
| 198 (Diamond) | +3.54pp | **0.48** | 13.9pp | UNDERPOWERED |
| 448 (Main) | +3.79pp | **0.25** | 9.3pp | UNDERPOWERED |
| 546 (Extended) | +3.66pp | **0.22** | 8.4pp | UNDERPOWERED |
| ~1,192 (all subsets) | +3.69pp | **0.07** | 5.7pp | UNDERPOWERED |

At **no** plausible GPQA size does the gap reach significance (p ranges 0.07–0.48; the 95% CI on
the difference includes 0 throughout). To reliably detect a real 3.5pp gap at 80% power you would
need **~2,820 questions per model** — an order of magnitude more than GPQA provides. The benchmark's
**minimum detectable effect** at n=198 is ~14pp: *any* GPQA gap smaller than ~14 points between two
models on the Diamond subset is, by construction, within the noise.

**Reading it.** This does not say the leading model is *not* better — it says the GPQA score
*cannot tell you whether it is*. The whole top of the GPQA ranking is compressed: over the full
leaderboard the top ten models span **3.6pp** (47.06% down to 43.46%), a spread far inside the
benchmark's own MDE. Ranking those models by
fractions of a GPQA point, or citing "we lead GPQA by 3 points," reports a number the sample size
cannot support.

**The fix** (what a defensible leaderboard would do): publish a confidence interval or standard
error on each GPQA score, and refuse to imply a ranking between models whose intervals overlap — or
report GPQA only in aggregate with enough other benchmarks that the *composite* is powered.

---

## Appendix A — Reproduction

**Data (public):** `open-llm-leaderboard/contents` on Hugging Face (via datasets-server `/rows`),
field **`GPQA Raw`** (raw accuracy), **all 4,576 rows** (re-pulled 2026-09-18; the dataset's
`lastModified` is 2025-03-20, so nothing drifted). Top two by GPQA Raw:
rank 1 `Steelskull/L3.3-MS-Nevoria-70b` = 0.4706, rank 2 `Steelskull/L3.3-Nevoria-R1-70b` = 0.4690.

**Correction, 2026-09-18.** The original version of this report named
`Daemontatox/Llama3.3-70B-CogniLink` (0.4455) as the GPQA leader and audited its 3.69pp lead over
`EVA-UNIT-01/EVA-Qwen2.5-72B-v0.2`. That model ranks **seventh**: six models score above it, and the
numbers quoted as "the top ~12" were the first rows of the dataset in its native order rather than the
top of the ranking. The pull covered roughly a tenth of the leaderboard and was never sorted against
the whole. The report's conclusion is unchanged and in fact stronger — the true top gap is 0.16pp,
p = 0.94 — but every model name and number under it was wrong, and one of them presented a named
author's model as the leaderboard's best on GPQA when it is not.

**Method:** successes = round(accuracy × n) per arm; two-proportion z-test (pooled) + 95% CI on the
difference (unpooled); MDE at n and required-N for the claimed gain at α=0.05 / 80% power. Pure
stdlib, deterministic.

```bash
# for each n in {198, 448, 546, 1192}:
python power_audit.py claim.json          # claim.json: arm_a/arm_b successes+n, claimed_gain=0.037
# -> VERDICT: UNDERPOWERED at every n; p in [0.07, 0.48]; required ~2820/arm
```

**Expected result:** UNDERPOWERED at all four n; exit code 1.

## Appendix B — Limitations

- Successes are derived from published accuracy × n (integer-rounded); the exact per-model graded
  counts would sharpen the figures slightly but cannot move a p=0.22–0.48 result across 0.05.
- The exact `n` of the leaderboard's GPQA task is subset-dependent; the finding is reported across
  the full plausible range precisely so it does not depend on pinning one value.
- This audits whether the GPQA *ranking* is statistically supported, not the models' actual
  capability, and not the other leaderboard sub-scores (some of which, e.g. MMLU-Pro at ~12k items,
  are far better powered).

---

*This Eval Integrity Report certifies that the listed numbers were honestly measured under the
controls described. Its finding is bounded and specific: the top GPQA ranking gap is inside the
benchmark's own sampling noise at every plausible sample size.*
