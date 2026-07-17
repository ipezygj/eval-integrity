# Eval Integrity Audit

*Independent verification of the model-performance numbers in a fundraise.*

---

## The problem

AI startups raise money on metrics — "94% accuracy," "beats GPT on our benchmark,"
"our judge scores us #1." VCs cannot independently verify these numbers, and founders
cannot easily prove they are honest. The gap matters because a large share of reported
eval claims fail basic measurement controls that have nothing to do with the model being
bad — they are artifacts of how the number was produced:

- **Contamination / leakage** — test items (or their answers) leaked into training or
  prompt context, so the score measures memorization, not capability.
- **Surface-area inflation** — a headline like "recall 0.50" that a "flag everything"
  baseline would also hit; the metric rewards how much the model outputs, not whether it
  is correct.
- **Underpowered samples** — a number computed on so few examples that it is
  statistically indistinguishable from chance.
- **LLM-judge bias** — when an LLM grades the outputs, the "win" can track answer
  *position*, answer *length*, or the judge's preference for its own model family, rather
  than answer quality.
- **Broken ground truth** — duplicate rows, degenerate labels, or a label set that is
  itself noise.

None of these require bad faith. Most eval regressions are one of a small, recurring set
of measurement pathologies. The trouble is that from the outside — and often from the
inside — an inflated number and a real one look identical. This service tells them apart.

We do not take a position on whether such failures are common across the industry; we
report only on the specific claims placed under audit.

---

## What the audit checks

We run two adversarial control batteries against the eval as it was actually computed —
the model's predictions, the ground-truth labels, and, where applicable, the judge's
verdicts. Every check is a *control*: something that must behave a certain way if the
number is real.

**Measurement-integrity battery** (for any detection/classification metric):

| Control | What it proves |
|---|---|
| Blind baseline | An all-negative / label-shuffled predictor must sit at the metric floor. A blind model that scores above floor means leakage or a degenerate setup. |
| Promiscuous baseline | A "flag everything" predictor must not score high on the headline. If it does, the metric rewards surface area, not correctness. |
| Permutation test | Shuffle the labels many times to build a null distribution. A real score must sit outside that band; inside it = not distinguishable from chance. |
| Base-rate baseline | How much of the headline is explained by class imbalance alone. |
| Metric panel | Precision / recall / F1 / MCC / accuracy side by side. A high recall shipping with near-zero precision or MCC is the surface-area trap exposed. |
| Surface-area confound | Correlates positive-prediction *volume* against hits per group. High correlation = the score tracks how much you flag. |
| Ground-truth hygiene | Duplicate rows, degenerate labels, perfect leakage (predictions == labels), class balance. |
| Ablation coherence | If a gain is attributed to a specific cause, removing that cause must move the metric beyond permutation noise. If the metric stays flat, the claimed cause is not the cause. |

**LLM-judge bias battery** (when scoring uses an LLM judge):

| Control | What it proves |
|---|---|
| Position | Swap A/B order — does the winner flip? A quality judge is order-invariant. |
| Verbosity | Does the longer answer win more than half the time regardless of content? |
| Self-preference | Does the judge favor answers from its own model family (a measurable conflict of interest)? |
| Blind control | A judge shown the answers with the verdict-relevant content stripped must fall to chance. If the blind verdict still predicts the real one, the score is recoverable without reading the answers. |
| Degeneracy | All-ties or one-sided verdicts — a judge that never actually discriminates. |

Each judge bias is gated behind a significance test, so a small, noisy eval cannot
manufacture a "bias" any more than it can manufacture a win.

---

## The deliverable

A signed **Eval Integrity Report** containing, for every claim under audit:

- The claimed metric and value, and the value we recomputed from the raw data.
- A probe table: each control, its result, and its severity.
- A **per-metric verdict** — one of **TRUSTWORTHY**, **SUSPECT**, or **ARTIFACT**
  (for judge claims, **JUDGE-BIASED**) — with the reasoning that produced it.
- An overall engagement verdict.
- A **reproduction appendix**: the exact inputs, tool versions, and commands so the
  client, and any investor they show it to, can re-run the audit and get the same result.

The report is a verifiable artifact. The startup can hand it to investors as evidence that
its numbers survive scrutiny; the investor can reproduce it rather than take it on trust.
Runs are deterministic (fixed seed), so re-execution reproduces every figure exactly.

---

## Engagement model and indicative pricing

*All figures below are indicative and scoped per engagement; final fees depend on the
number of claims, data readiness, and whether judge auditing is in scope.*

| Tier | Scope | Indicative fee |
|---|---|---|
| **Single Headline Claim** | One metric (e.g. the one number on the deck). Full control battery, per-metric verdict, reproduction appendix. Fixed fee. | ~$3,500 |
| **Full Eval Suite** | Up to ~10 claims across the model's benchmark suite, including LLM-judge bias auditing where scoring is judge-based. | ~$12,000–$20,000 |
| **Pre-Fundraise Retainer** | Ongoing engagement for a team preparing to raise: audit numbers as they are produced, re-audit on data-room updates, and a diligence-desk line for the lead investor's questions. | ~$5,000–$8,000 / month |
| **VC Diligence Engagement** | Commissioned by the investor rather than the startup: audit a target company's headline claims during diligence. Priced per target, typically at the Single-Claim or Full-Suite level. | from ~$4,000 |

Data-readiness note: fees assume the client can provide raw predictions and labels (and,
for judge audits, per-comparison verdicts). We provide the input schema up front; assembling
that data is the client's responsibility and is not billed by us.

---

## Why independent, and why this auditor

The value of an audit is that it can return an unwelcome answer. This one is built to.

- **Verdicts are derived from the controls, not asserted.** The engine computes the
  verdict from the probe results structurally; no prose, and no auditor's opinion, can
  overturn what the controls show. A number is called trustworthy only when its controls
  actually pin.
- **Structural vs. discriminating discipline.** The tooling distinguishes a metric that is
  *inherently* gameable (a metric-choice problem, true of any model) from *discriminating*
  evidence that *this specific run* is inflated. A structural weakness caps a claim at
  SUSPECT and generates an advisory; it never on its own brands a number an ARTIFACT.
  Conversely, an ablation flip, a failed permutation test, a collapsed MCC, a blind leak,
  broken ground truth, or a significant judge bias *does*. The auditor refuses both to
  bless a number it cannot defend and to condemn one on a technicality.
- **Independence.** As an outside party with no stake in the round, the auditor has no
  incentive to round up. The founder gets a credential they could not self-issue; the
  investor gets a check they did not have to run themselves.

---

## Scope boundaries — what this is NOT

- It does **not** certify that the model is good, safe, or fit for any purpose. It
  certifies only that the reported numbers were honestly measured.
- It does **not** assess whether the benchmark is the *right* benchmark for the business,
  nor whether the metric is the *right* metric — only whether the reported figure on the
  chosen metric survives its controls.
- It is **not** a security, legal, or financial audit, and makes no representation about
  the company beyond the specific claims listed in the engagement scope.
- A **TRUSTWORTHY** verdict means the number survived the controls we ran on the data we
  were given; it is not a guarantee of future performance or of behavior on data outside
  the audited set.
- The audit is only as good as the raw data supplied. If a client provides fabricated
  predictions or labels, the report attests to the integrity of the *measurement*, not the
  provenance of the data — a limitation stated on the face of every report.
