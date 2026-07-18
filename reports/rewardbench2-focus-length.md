# RewardBench 2 fixed v1's length bias — but the Focus subset inverted it

**Target:** RewardBench 2 (`allenai/reward-bench-2`, 1,865 items)
**Control:** content-blind length baseline + a causal per-length-stratum check
**Verdict:** aggregate is length-robust (the v1 issue is fixed) — but the `Focus` subset carries a strong *inverse* length confound
**Cost:** $0, public data only

## The control

For a best-of-N preference benchmark (one correct completion among several), a trivial null is "pick by length alone." On a subset that measures reward *quality* this should sit at chance (here 1/4 = 25%). RewardBench 2's format lets us run it directly on the gold pairs.

## Result

**Credit first:** RewardBench 2 *fixed* the v1 length degeneracy. A content-blind "pick the longest completion" baseline scores **21.3% overall — below the 24.8% chance rate.** The authors clearly corrected the aggregate.

**But the fix left an inverse confound on one subset.** On `Focus` (≈27% of the benchmark), the gold answer is on average *shorter* than the distractors, and a zero-parameter "**pick the shortest** completion" baseline scores **52.7% — 2.1× chance (z = 14.2, p ≪ 1e-6).** It holds under token count too (0.511). Math and Safety show weaker versions.

**A causal control confirms it's length, not focus-quality.** Binning Focus items by the chosen-vs-rejected length gap, the pick-shortest lift is 100% in the length-imbalanced strata but **collapses to chance (0.234 vs 0.25) in the length-balanced stratum** — when the completions are matched for length, "pick shortest" tells you nothing. So the Focus signal a length ruler exploits *is* length.

## Why it happens

The Focus distractors are generated to be off-topic / unresponsive (LLMBar-style) and empirically ramble *longer* (chosen 2,216 vs rejected 2,980 chars), so length ends up collinear with the label — inverted relative to v1's alpacaeval subsets. A reward model's Focus score is then confounded with its length preference: a brevity-biased model gets a tailwind; the more common verbosity-biased model is penalized for the wrong reason.

## Honest caveats

- Correct-is-shorter may be *partly* legitimate — a focused answer genuinely tends to be more concise, so length is a proxy, not purely spurious. The causal control shows the *measured* lift is length, but proxy-vs-artifact can't be fully separated from the data alone.
- This is not "reward models are just length-biased" — the ruler is *below* chance overall. The defect is localized to how the Focus completions were generated.

## Filed publicly

**[allenai/reward-bench#268](https://github.com/allenai/reward-bench/issues/268)** — with a self-contained reproduction.

**Fix:** report a length-controlled Focus accuracy (as AlpacaEval v2 adopted a length-controlled win-rate after its own length confound was quantified).
