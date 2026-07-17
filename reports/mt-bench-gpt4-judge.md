# Eval Integrity Report

> **SAMPLE / SALES COLLATERAL.** This is a *real* audit of a *public* dataset, produced to
> demonstrate the Eval Integrity service. Every number below was recomputed from raw data
> downloaded from the source cited in Appendix A. No client commissioned it and no data was
> fabricated. It is free to share.

---

## 1. Engagement header

| Field | Value |
|---|---|
| Client | SAMPLE — no client (public-dataset demonstration) |
| Client contact | n/a |
| Engagement type | Single Headline Claim (LLM-as-judge) |
| Commissioned by | Eval Integrity (self-commissioned sample) |
| Report date | 2026-07-17 |
| Report version | v1.0 |
| Auditor | Eval Integrity audit tooling |
| Tooling | measurement_audit.py `6e162f69`, judge_audit.py `6e162f69` |
| Determinism | No RNG in the judge battery; every figure is a deterministic function of the input file (Appendix A). Re-running reproduces the numbers byte-for-byte. |

### Scope

**Target:** MT-Bench / "Judging LLM-as-a-Judge" (LMSYS). We audit the **pre-generated GPT-4
pairwise judgments** that ship with the benchmark — the file `gpt-4_pair.jsonl` — restricted
to the **general pairwise templates** (`pair-v2` single-turn + `pair-v2-multi-turn`),
n = 2,999 pairwise verdicts. Each verdict was rendered by GPT-4 in **both** answer orderings
(fields `g1_winner` / `g2_winner`), which is exactly the raw material a position-bias probe
needs.

**In scope:** whether the GPT-4 pairwise judge behaves as an *order-invariant, content-only*
measure of answer quality, tested for the four documented LLM-judge biases (position,
verbosity, self-preference, blind leakage) plus degeneracy.

**Out of scope:** the `pair-math-v1` reference-guided template (audited separately, see
§Reasoning), single-answer (`gpt-4_single`) grading, GPT-4's agreement rate with *human*
labels, the quality of any underlying model, and the provenance of the LMSYS file itself
(we attest to the measurement on the bytes we downloaded, not to how LMSYS produced them).

### Claims under audit

| # | Claim (as stated by the benchmark) | Metric | Claimed value | Source |
|---|---|---|---|---|
| C1 | GPT-4 acting as a pairwise judge is a reliable stand-in for human preference — its A-vs-B verdicts reflect answer *quality*, not presentation. (The paper reports ~85% GPT-4↔human agreement and uses these verdicts to rank models.) | judge win-rate / pairwise verdict validity | "reliable / order-invariant quality signal" | Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, NeurIPS 2023; data file `gpt-4_pair.jsonl` |

---

## 2. Overall verdict

**Overall: JUDGE-BIASED**

| Claim | Metric | Claimed | Recomputed | Verdict |
|---|---|---|---|---|
| C1 | pairwise verdict validity | "unbiased quality signal" | length wins 68.0%; own-family wins 71.5% | **JUDGE-BIASED** |

Summary: On its own raw data the GPT-4 pairwise judge is **not** the content-only instrument
the headline framing implies. Two presentation confounds reach overwhelming significance:
the **longer** answer wins **68.0%** of the time (p≈0) and answers from the judge's **own
model family (GPT) win 71.5%** of the time (p≈0). Order-sensitivity is real but small in
aggregate (position-1 wins 52.6%, sub-threshold; 12.9% of paired verdicts flip on swap).
The single most important finding: **verdicts co-vary with length and with author-family as
strongly as with anything the judge could have read**, so a win on this leaderboard is not
cleanly attributable to answer quality without controls the eval does not apply.

---

## 3. Per-claim findings

### Claim C1 — GPT-4 pairwise judge as an unbiased quality signal (LLM-judge)

| Field | Value |
|---|---|
| Claim as stated | "GPT-4's pairwise A/B verdicts are a reliable, order-invariant measure of answer quality." |
| Metric | judge win-rate / pairwise verdict validity |
| Claimed value | "unbiased quality signal" (paper: ~85% agreement with humans) |
| Recomputed value | verbosity: longer wins 68.0%; self-preference: GPT-family wins 71.5%; position-1 wins 52.6% (flip 12.9%) |
| Number of judgments (n) | 2,999 general pairwise verdicts (each rendered in both orderings → 5,821 non-tie decisions; verbosity tested on 2,600 length-resolved pairs; self-preference on 2,820 mixed-family pairs) |
| Judge family | gpt (GPT-4, template `pair-v2`) |
| **Verdict** | **JUDGE-BIASED** |

#### Probe table

> One row per probe from `judge_audit.py --json`. Each bias is gated behind a two-sided
> binomial significance test vs 0.5.

| Probe | Result / key figures | Severity |
|---|---|---|
| degeneracy | discriminates: A=886, B=2028, tie=85 (n=2999) | OK |
| position_bias | position-1 wins **52.6%** (n_dec=5821, z=3.91, p=0.0001), flip_rate=**0.129** over 2877 swap pairs | OK |
| verbosity_bias | the **longer answer wins 68.0%** (n=2600, z=18.3, p≈0.000) | **CRITICAL** |
| self_preference | judge family **gpt picks its own family 71.5%** (n=2820, z=22.8, p≈0.000) | **CRITICAL** |
| blind_control | no `blind_winner` field in the public file → not run | INFO |

#### Reasoning

The verdict is derived mechanically from the probe severities: two **discriminating**
CRITICALs (verbosity, self-preference) → JUDGE-BIASED. Walking the evidence:

- **Verbosity (CRITICAL, the driver).** Of 2,600 verdicts where the two answers differ in
  length, the longer one wins 68.0% of the time — 18 standard deviations off the 0.5 an
  order/length-blind judge would produce. Winning answers average 1,079 characters vs 953
  for losers (1.13×). This is the "LLM judges reward length" effect the MT-Bench authors
  themselves flag; here it is quantified on their own file. It does not prove length *causes*
  the win (longer answers can also be better), but it proves the headline "quality signal"
  is entangled with a presentation variable the eval never controls — so a raw pairwise
  win-rate cannot be read as a clean quality measurement.

- **Self-preference (CRITICAL).** Among 2,820 pairs pitting a GPT-family answer
  (GPT-4 or GPT-3.5-turbo) against a non-GPT answer, the GPT side wins 71.5% (z=22.8).
  Narrowing to **GPT-4's own answers**, GPT-4-as-judge picks GPT-4-as-author in **82 of 94**
  head-to-heads (**87.2%**). We checked the obvious confound: in these GPT-vs-non-GPT pairs
  the GPT side is the *longer* answer only 51.8% of the time — i.e. length is balanced, so
  the self-preference is **not** merely the verbosity effect wearing a mask. A model grading
  a leaderboard that contains its own outputs is a measurable conflict of interest, and it is
  measurably firing here.

- **Position (OK, but not clean).** Aggregate position-1 win-rate is 52.6%. That is
  statistically distinguishable from 0.5 (p=0.0001) but the *effect size* is small — below
  the auditor's 55% escalation threshold — so the probe correctly declines to call it a
  CRITICAL. The honest read: order matters a little, and 12.9% of paired verdicts literally
  **flip when the two answers swap seats** (87.1% consistency), matching the order-sensitivity
  the paper reports. Aggregate position bias is muted here mainly because answer *strength*
  dominates seat position and the two orderings partially cancel; the flip-rate is the
  cleaner order signal and it is non-zero.

- **Blind control (INFO).** The public file carries no content-stripped verdict, so the
  strongest single control — "does a judge that cannot see the answers still reproduce the
  verdict?" — could not be run. We recommend generating one before treating any future
  version of this judge as trustworthy.

**Bottom line for a buyer of this eval:** the GPT-4 pairwise number is usable as a *rough*
ranking signal but must not be quoted as an unconfounded measure of quality. Any comparison
that (a) pits answers of different length or (b) includes GPT-family models against non-GPT
models inherits a bias worth double-digit win-rate points. Fixes: length-normalise or
length-match pairs, use a disinterested (non-GPT) judge or an ensemble, always run both
orderings and report the flip-rate, and add a blind control.

> **Cross-check (out of scope, informational):** the same battery on the `pair-math-v1`
> reference-guided subset (n=1,800) also returns **JUDGE-BIASED** — verbosity 64.0% and
> self-preference 87.5% — so the biases are not an artifact of the general template alone.

---

## Appendix A — Reproduction

**Tooling**
- `judge_audit.py` — git `6e162f6915724711ec964d7bf8a5ea431a066273` (2026-07-17)
- `measurement_audit.py` — git `6e162f6915724711ec964d7bf8a5ea431a066273` (shared verdict/derive_verdict)
- Python 3.14.6; pure standard library (no third-party ML deps).
- Determinism: the judge battery contains no RNG; output is a pure function of the input JSON.

**Data source (real)**
- Judgments: `https://huggingface.co/spaces/lmsys/mt-bench/resolve/main/data/mt_bench/model_judgment/gpt-4_pair.jsonl` (4,800 rows; downloaded 2026-07-17).
- Model answers (for lengths): `https://huggingface.co/spaces/lmsys/mt-bench/resolve/main/data/mt_bench/model_answer/<model>.jsonl` for all 31 MT-Bench models.
- Download manifest: `fastchat/llm_judge/download_mt_bench_pregenerated.py` in `github.com/lm-sys/FastChat`.

**Field mapping (raw → auditor schema)** — content **A = `model_1`**, content **B = `model_2`**:
- `winner` ← `g1_winner` (game 1: `model_1` sits in position 1): `model_1`→`A`, `model_2`→`B`, `tie`→`tie`, `error`→dropped.
- `winner_swapped` ← `g2_winner` (game 2: positions swapped, still named by *content/model*): same map. An order-invariant judge yields `winner == winner_swapped`.
- `len_a`/`len_b` ← character length of the judged turn's answer for `model_1`/`model_2`, indexed by (model, question_id, turn) from the model_answer files. 300/2,999 pairs had a missing answer/turn and were excluded from the verbosity probe only.
- `family_a`/`family_b` ← `gpt` for {gpt-4, gpt-3.5-turbo}, `claude` for {claude-v1, claude-instant-v1}, else the model id. `judge_family = "gpt"` (GPT-4 is the judge).
- Scope filter: `judge[1] ∈ {pair-v2, pair-v2-multi-turn}`.

**Inputs** (kept in the audit scratch dir, not committed to the repo; hashes fix the exact bytes audited)
| File | Description | SHA-256 |
|---|---|---|
| `gpt-4_pair.jsonl` | raw LMSYS pairwise judgments (4,800 rows) | `d662c0b7d1d297f0494fcb4cc09fe8f054fa22d75deb4754a483a921984bc585` |
| `judge_general.json` | derived auditor input (2,999 general pairwise verdicts) | `37593ae93c503961875e463cfc33558caeef9ae7b9237808d33488b92101b4d2` |
| `judge_audit.py` | auditor | `68eaa5cb5aba11d41a63c7c5617e6b6377cd44b3f97bd0d87d8b77eb9bb4d42d` |
| `measurement_audit.py` | shared verdict engine | `cab8eb013ca337c559dcef31a367eaef5272717add9048c37b2906f0e0c610b2` |

**Commands**
```bash
# 1. fetch raw judgments + model answers (source URLs above)
# 2. build judge_general.json via the field mapping in this appendix
# 3. audit:
python judge_audit.py judge_general.json          # human-readable
python judge_audit.py judge_general.json --json    # machine-readable (probe table above)
```

**Expected result:** `VERDICT: JUDGE-BIASED` — verbosity_bias CRITICAL (longer wins 68.0%,
p≈0.000) and self_preference CRITICAL (GPT own-family wins 71.5%, p≈0.000). Exit code 1.

> Exit codes: `judge_audit.py` exits non-zero on JUDGE-BIASED — so re-execution drops into CI.

---

## Appendix B — Limitations

- This report attests to the **integrity of the measurement** on the LMSYS file as downloaded,
  not to how LMSYS generated it. Fabricated inputs are outside its assurance.
- The verbosity and self-preference probes measure **correlation**, not proven causation:
  longer / GPT-family answers may also be genuinely better. The finding is that the eval
  reports a raw pairwise win-rate **without controlling for these confounds**, so the number
  cannot be read as a clean quality signal — not that quality plays no role.
- The blind control could not be run (no content-stripped verdict in the public file); the
  strongest single leakage test is therefore absent.
- Verdicts describe this data set only; they are not a prediction of a differently-configured
  judge's behavior.
- Out-of-scope items (§1) were not examined and carry no assurance.

---

## Sign-off

| | |
|---|---|
| Auditor | Eval Integrity audit tooling |
| Signature | __________________________ |
| Date | 2026-07-17 |
| Report ID | mtbench-gpt4-pair-v2 / judge_general.json@37593ae9 |

*This Eval Integrity Report certifies that the listed numbers were honestly measured under
the controls described. It does not certify that the judge, or any model it ranks, is good,
safe, or fit for any purpose.*
