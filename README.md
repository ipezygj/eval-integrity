# Eval Integrity

**Independent auditing of the measurement behind AI eval numbers** — not "is the model good,"
but "is this benchmark/leaderboard number honestly measured, or a measurement artifact?"

AI systems are ranked and funded on eval numbers — "94% accuracy," "beats GPT on our
benchmark," "our judge scores us #1." A large share of eval claims fail basic measurement
controls that have nothing to do with the model: length/verbosity confounds, LLM-judge biases,
degenerate ground truth, contamination, underpowered samples. From the outside — and often
from the inside — an inflated number and a real one look identical. This project tells them
apart, and does so with controls whose verdicts are **derived structurally**, not asserted.

![eval-integrity CLI producing a red/yellow/green scorecard](docs/assets/eval_scan_demo.gif)

Every report here is a **real audit of a public dataset**, recomputed from raw data, free to
share. They double as worked examples of the method described in [`OFFERING.md`](OFFERING.md).

## Sample reports

| Report | Target | Finding | Discipline it demonstrates |
|---|---|---|---|
| [MT-Bench GPT-4 judge](reports/mt-bench-gpt4-judge.md) | LMSYS MT-Bench pairwise judge | **JUDGE-BIASED** — longer answer wins 68.0%, GPT own-family wins 71.5% | correlational judge-bias battery |
| [AlpacaEval win-rate](reports/alpacaeval-winrate.md) | AlpacaEval GPT-4-Turbo auto-annotator | **JUDGE-BIASED (verbosity)** — a *causal* control (same model, length only) moves win-rate 13.0%→24.2% | causal confirmation **+ refusing to certify two biases the data can't support** |
| [RewardBench length degeneracy](reports/rewardbench-length-degeneracy.md) | RewardBench v1 gold pairs | two subsets are length-degenerate — a 0-parameter "pick the longer answer" baseline scores **100%** | gold-label degeneracy on a live leaderboard |
| [RewardBench 2 Focus](reports/rewardbench2-focus-length.md) | RewardBench 2 gold pairs | v2 fixed the aggregate, but `Focus` inverted it — "pick the *shortest*" scores **52.7%** (2.1× chance); a causal control confirms it's length | causal length-confound isolation |
| [Leaderboard significance tiers](reports/leaderboard-significance-tiers.md) | BigCodeBench · EvalPlus · Open LLM Leaderboard | small-N leaderboards can't rank their tops — **55 of 199 models tied with #1 on BigCodeBench-Hard**; a clean sample-size gradient (large-N is separable) | statistical power / two-proportion significance |

Several findings are filed as public issues on the benchmarks' own trackers:
**[allenai/reward-bench#267](https://github.com/allenai/reward-bench/issues/267)** (v1 length),
**[#268](https://github.com/allenai/reward-bench/issues/268)** (v2 Focus), and
**[bigcode-project/bigcodebench#121](https://github.com/bigcode-project/bigcodebench/issues/121)**
(leaderboard significance). Each is fully reproducible — e.g.
[`reproduce/reproduce_rewardbench_length.py`](reproduce/reproduce_rewardbench_length.py)
downloads the public data and prints the tables (pure stdlib, deterministic, no model inference).

## What the audit checks

Two adversarial control batteries, each control being something that *must* behave a certain way
if the number is real:

- **Measurement-integrity** (any detection/classification metric): blind baseline, promiscuous
  baseline, permutation test, base rate, metric panel (MCC as the honest number), surface-area
  confound, ground-truth hygiene, ablation coherence.
- **LLM-judge bias** (when scoring uses an LLM judge): position, verbosity, self-preference,
  blind control, degeneracy — each gated behind a significance test so a small noisy eval can't
  manufacture a "bias."
- **Statistical power & ranking significance** (any leaderboard / A-vs-B claim): minimum
  detectable effect for the sample size, paired significance on the same items, and a
  two-proportion tier check that flags when a ranking's top is inside the noise (see the
  leaderboard-significance report).

Verdicts (`TRUSTWORTHY` / `SUSPECT` / `ARTIFACT`, or `JUDGE-BIASED`) are computed from the probe
severities. A structurally-gameable *metric choice* only caps a claim at SUSPECT; branding a
number an ARTIFACT requires *discriminating* evidence (an ablation flip, a failed permutation
test, a collapsed MCC, a blind leak, broken ground truth, or a significant judge bias). The
auditor is built to refuse both blessing a number it can't defend and condemning one on a
technicality — see the AlpacaEval report, which withdraws two biases the generic battery flags.

## The service

[`OFFERING.md`](OFFERING.md) describes an independent Eval Integrity Audit — for a startup that
wants its fundraise numbers to survive scrutiny, or a VC doing diligence on a target's model
claims. A [`REPORT_TEMPLATE.md`](REPORT_TEMPLATE.md) shows the deliverable shape.

## Scope boundaries

These reports attest to the **integrity of the measurement** on the public data as downloaded —
not that any model is good, safe, or fit for purpose, and not to how the dataset owners produced
their files. Correlational findings are labeled as such; causal claims are backed by a control.
Contact / engagement details are in [`OFFERING.md`](OFFERING.md).
