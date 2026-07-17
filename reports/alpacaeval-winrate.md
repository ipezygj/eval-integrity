# Eval Integrity Report

> **SAMPLE / SALES COLLATERAL.** This is a *real* audit of a *public* dataset, produced to
> demonstrate the Eval Integrity service. Every number below was recomputed from raw data
> downloaded from the source cited in Appendix A. No client commissioned it and no data was
> fabricated. It is free to share.
>
> This is a **companion** to the MT-Bench sample report. Where the MT-Bench audit demonstrates
> the *correlational* judge-bias battery, this one demonstrates two further disciplines: (1) a
> **causal, controlled** confirmation of the one finding that survives — and (2) the auditor
> **refusing to certify two biases the raw battery flags** because they are not defensible on
> this data. An integrity product's value is precisely what it declines to claim.

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
| Tooling | judge_audit.py `6e162f69`, measurement_audit.py `6e162f69` (shared verdict engine) |
| Determinism | No RNG in the judge battery; every figure is a deterministic function of the input files (Appendix A). Re-running reproduces the numbers exactly. |

### Scope

**Target:** **AlpacaEval** (Dubois et al., Stanford) — the automatic LLM-judged instruction-
following leaderboard. We audit its headline instrument: the **win-rate** produced by the
`weighted_alpaca_eval_gpt4_turbo` auto-annotator, in which **GPT-4-Turbo judges** each model's
answer against a fixed **GPT-4-1106-preview reference answer** and the leaderboard reports the
fraction of comparisons the model "wins."

We audit two slices of the *published* annotation files:

- **Pooled slice** — 4,830 pairwise verdicts across six leaderboard entries spanning three
  model families (Llama, Mistral/Mixtral, Qwen), to run the standard judge-bias battery.
- **Controlled slice** — the project's own **`_concise` / `_verbose`** ablation of one base
  model (`Mixtral-8x7B-Instruct-v0.1`), in which the *same model* is prompted to answer the
  *same questions* more or less verbosely. This holds model quality fixed and moves only
  answer length — a genuine causal control on the verbosity question.

**In scope:** whether the AlpacaEval auto-annotator win-rate is a *content-only* measure of
answer quality, or whether it co-varies with presentation (answer length, author family).

**Out of scope:** AlpacaEval's own **length-controlled (LC) win-rate** (a *fix* the project
shipped in v2.0 — see §Reasoning; we audit the *raw* win-rate the confound motivated), the
correlation with human preference, the quality of any model, and the provenance of the
annotation files (we attest to the measurement on the bytes we downloaded).

### Claims under audit

| # | Claim (as implied by leaderboard use) | Metric | Claimed value | Source |
|---|---|---|---|---|
| C1 | The AlpacaEval GPT-4-Turbo auto-annotator win-rate ranks models by answer *quality* — a higher win-rate means better instruction-following. | judge win-rate / pairwise verdict validity | "quality signal / faithful ranking" | Dubois et al., *AlpacaEval* / *Length-Controlled AlpacaEval*; `tatsu-lab/alpaca_eval` annotation files |

---

## 2. Overall verdict

**Overall: JUDGE-BIASED** — on a single, *causally confirmed* confound: **verbosity.**

| Claim | Metric | Claimed | Recomputed | Verdict |
|---|---|---|---|---|
| C1 | pairwise verdict validity | "quality signal" | making one model's answers longer, nothing else changed, raises its win-rate from **13.0% → 24.2%** | **JUDGE-BIASED (verbosity)** |

Summary: The AlpacaEval auto-annotator win-rate is materially confounded by **answer length**.
The decisive evidence is not a correlation — it is the project's own controlled ablation:
taking **one fixed model** and only changing how verbose its answers are moves its win-rate
against the identical reference from **13.0% (concise) → 16.8% (neutral) → 24.2% (verbose)**,
a **+11.1-point** swing (z = 5.7, p ≈ 1e-8) attributable to **length alone**. That is a clean
causal demonstration that the raw win-rate rewards padding, independent of quality.

**Two biases the raw battery also flags, we decline to certify** (this is the finding as much
as the verbosity one):

- **Position bias — NOT TESTABLE here, discarded.** The battery reports "position-1 wins
  79.6%," but AlpacaEval's annotator **randomizes answer order internally** and de-randomizes
  the recorded `preference` back to semantic (reference vs model). "A" in our encoding is the
  *reference*, not a *prompt seat*, and no swapped-order verdict is published — so the 79.6% is
  **not** order sensitivity and must not be read as such. We drop it.
- **Self-preference — CONFOUNDED, downgraded to advisory.** The battery reports "GPT family
  wins 79.6%," but the GPT-family answer here **is** the reference `gpt4_1106_preview`, a
  genuinely strong model these 7B–70B open models mostly lose to on merit. Without a
  family-swapped design we cannot separate a same-family preference from real quality, so we do
  **not** certify a conflict of interest. (Note: this 79.6% is the *same statistic* as the
  bogus "position" number — one confound wearing two labels.)

The honest one-line read: **AlpacaEval's raw auto-win-rate cannot be quoted as a clean quality
measure — it pays for length** — and that is exactly why the project itself introduced a
length-controlled win-rate. The other two "biases" the generic battery surfaces are artifacts
of this dataset's shape and are withdrawn.

---

## 3. Per-claim findings

### Claim C1 — AlpacaEval auto-annotator win-rate as a quality signal (LLM-judge)

| Field | Value |
|---|---|
| Claim as stated | "A higher AlpacaEval GPT-4-Turbo win-rate means better answer quality." |
| Metric | judge win-rate / pairwise verdict validity |
| Recomputed value | verbosity **causal**: 13.0% → 24.2% win-rate by length alone (same model); verbosity correlational (pooled): longer wins 73.3% |
| Number of judgments (n) | pooled 4,830 verdicts (6 models); controlled slice 805 (concise) + 803 (neutral) + 803 (verbose) verdicts, same base model |
| Judge family | gpt (GPT-4-Turbo annotator; GPT-4-1106-preview reference) |
| **Verdict** | **JUDGE-BIASED (verbosity, causally confirmed)** |

#### Probe table — pooled battery (`judge_audit.py --json`)

> Raw output of the standard battery over the 6-model pooled slice. The **Adjudication**
> column is the auditor's disposition; see Reasoning for why two raw CRITICALs are withdrawn.

| Probe | Result / key figures | Raw severity | Adjudication |
|---|---|---|---|
| degeneracy | discriminates: A(ref)=3835, B(model)=982, tie=13 (n=4830) | OK | — |
| verbosity_bias | longer answer wins **73.3%** (n=4811, z=32.3, p≈0) | **CRITICAL** | **UPHELD**, and *upgraded* to causal (controlled slice below) |
| position_bias | "position-1 wins 79.6%" (n=4817, z=41.1); **swap_pairs=0, flip test skipped** | CRITICAL | **DISCARDED** — order is randomized inside the annotator; "A" is the reference, not a seat; untestable here |
| self_preference | "gpt own-family wins 79.6%" (n=4817, z=41.1) | CRITICAL | **DOWNGRADED → advisory** — the GPT answer is the strong reference; confounded with quality; same statistic as position |
| blind_control | no `blind_winner` in public files → not run | INFO | recommend for any future engagement |

#### Controlled slice — the causal confirmation (same base model, length varied)

> `Mixtral-8x7B-Instruct-v0.1`, three published variants, each judged against the identical
> `gpt4_1106_preview` reference on the same 805 prompts. Only answer verbosity differs.

| Variant | Mean answer length | Win-rate vs reference | Δ vs concise |
|---|---|---|---|
| `_concise` | 910 chars | **13.0%** | — |
| (neutral) | 1,466 chars | 16.8% | +3.8 pts |
| `_verbose` | 2,083 chars | **24.2%** | **+11.1 pts** |

Concise → verbose: **z = 5.7, p ≈ 1.0e-8** (two-proportion test). Model, weights, questions,
and reference are identical across the three columns; **length is the only manipulated
variable.** The win-rate nearly doubles.

#### Reasoning

The verdict rests on the **controlled** slice, not the pooled correlation — and this is the
methodological point of the report.

- **Why the pooled correlation is not enough (honesty check).** Pooled, the longer answer wins
  73.3% — but in this data the reference `gpt4_1106_preview` is **both longer** (mean 2,049 vs
  1,621 chars; longer in 73.1% of pairs) **and stronger**, so "longer wins" is entangled with
  "the better model wins." Worse, *within a single model's* natural outputs the length↔win
  correlation is actually **slightly negative** (Pearson −0.09 on the neutral Mixtral) — because
  naturally-longer answers tend to be responses to harder prompts. A responsible auditor cannot
  call verbosity a bias from the pooled number alone.

- **Why the controlled slice settles it.** The `_concise`/`_verbose` ablation removes the
  quality confound by construction: same model, same questions, same reference — only length
  moves. The win-rate rises monotonically with length and the concise→verbose gap is +11.1
  points at p≈1e-8. **This is length *causing* wins, not length *correlating* with a better
  model.** It is the single cleanest control available on this dataset, and it fires.

- **External corroboration.** This is not a novel accusation — it is the documented reason the
  AlpacaEval authors shipped a **length-controlled win-rate** in v2.0, built specifically to
  neutralize the verbosity gameability we measure here. Our report quantifies, on the raw files,
  the confound their fix targets. (Their LC metric is out of scope — we audit the *raw*
  win-rate, which is still widely quoted.)

- **Why we discard position bias.** The battery's position probe, with no swapped-order verdict
  to compare, degenerates into "does one side win more often" and labels the imbalance
  "position." On AlpacaEval that reading is simply wrong: the annotator randomizes the physical
  order and reports a de-randomized `preference`, so our "A" is the *reference answer*, not
  *prompt position 1*. The 79.6% is real, but it is not order sensitivity. Certifying it would
  be the exact over-claim this service exists to prevent. **Discarded.**

- **Why we downgrade self-preference.** Same 79.6% statistic, relabeled: every "A" is the
  GPT-family reference, which is a top-tier model these open models mostly lose to fairly.
  Distinguishing a same-family *preference* from a genuine *quality* gap needs a design where
  family and quality are decoupled (e.g. swap in a non-GPT judge, or a GPT-family answer known
  to be weaker). This data has neither. We record self-preference as an **advisory / untested
  risk**, not a certified bias.

**Bottom line for a buyer of this eval:** treat the raw AlpacaEval GPT-4-Turbo win-rate as
**length-inflatable** — a model can move double-digit win-rate points by padding, with no
quality change. Use the length-controlled variant, or length-match/normalize before quoting the
raw number. Do **not** infer from these files that the judge has a position bias or a GPT
self-preference; those require controls the published data does not contain.

---

## Appendix A — Reproduction

**Tooling**
- `judge_audit.py` — git `6e162f6915724711ec964d7bf8a5ea431a066273` (2026-07-17)
- `measurement_audit.py` — git `6e162f6915724711ec964d7bf8a5ea431a066273` (shared `derive_verdict`)
- Python 3.14.6; pure standard library (no third-party ML deps).
- Determinism: the judge battery and the win-rate/length computations contain no RNG; output is
  a pure function of the input JSON.

**Data source (real)** — `tatsu-lab/alpaca_eval`, GitHub `main`, path
`results/<model>/weighted_alpaca_eval_gpt4_turbo/annotations.json`
(`https://raw.githubusercontent.com/tatsu-lab/alpaca_eval/main/results/<model>/weighted_alpaca_eval_gpt4_turbo/annotations.json`),
downloaded 2026-07-17.

Pooled models: `Meta-Llama-3-8B-Instruct`, `Meta-Llama-3-70B-Instruct`,
`Mistral-7B-Instruct-v0.2`, `Mixtral-8x22B-Instruct-v0.1`, `Mixtral-8x7B-Instruct-v0.1`,
`Infinity-Instruct-3M-0625-Qwen2-7B`.
Controlled slice: `Mixtral-8x7B-Instruct-v0.1{,_concise,_verbose}`.

**Field mapping (raw → auditor schema)** — in every AlpacaEval annotation, `output_1`/
`generator_1` is the **reference** (`gpt4_1106_preview`) and `output_2`/`generator_2` is the
**model under test**; `preference` is a weighted score in [1,2] (→1 favors the reference, →2
favors the model):
- `winner` ← `A` if `preference < 1.5` (reference wins), `B` if `> 1.5` (model wins), else `tie`.
- `len_a`/`len_b` ← character length of `output_1`/`output_2`.
- `family_a` ← `gpt` (reference is `gpt4_1106_preview`); `family_b` ← family of `generator_2`
  (`llama`/`mistral`/`qwen`). `judge_family = "gpt"` (GPT-4-Turbo annotator).
- Controlled slice win-rate = fraction of decided verdicts with `preference > 1.5`; mean length
  = mean `len(output_2)`.

**Inputs** (raw annotation files kept in the audit scratch dir, not committed; the derived
auditor input is hashed to fix the exact bytes audited)

| File | Description | SHA-256 |
|---|---|---|
| `alpacaeval_judge.json` | derived pooled auditor input (4,830 verdicts, 6 models) | `05825e055000ffa73215bb4d9fcfeaa544d9a8f0446e847c20ca8c7927ff4188` |
| `judge_audit.py` | auditor | `68eaa5cb5aba11d41a63c7c5617e6b6377cd44b3f97bd0d87d8b77eb9bb4d42d` |
| `measurement_audit.py` | shared verdict engine | `cab8eb013ca337c559dcef31a367eaef5272717add9048c37b2906f0e0c610b2` |

**Commands**
```bash
# 1. fetch results/<model>/weighted_alpaca_eval_gpt4_turbo/annotations.json for the models above
# 2. build alpacaeval_judge.json via the field mapping in this appendix (pooled slice)
# 3. audit the pooled battery:
python judge_audit.py alpacaeval_judge.json          # human-readable
python judge_audit.py alpacaeval_judge.json --json    # machine-readable (probe table above)
# 4. controlled slice: win-rate = mean(preference>1.5), mean length = mean len(output_2),
#    over the _concise / neutral / _verbose annotation files (numbers in §3).
```

**Expected result (pooled):** `VERDICT: JUDGE-BIASED`, exit code 1 — verbosity_bias CRITICAL
(longer wins 73.3%). The report's *adjudicated* verdict keeps verbosity (causally confirmed by
the controlled slice) and withdraws the position/self-preference flags per §Reasoning.

---

## Appendix B — Limitations

- This report attests to the **integrity of the measurement** on the AlpacaEval annotation
  files as downloaded, not to how the project generated them. Fabricated inputs are outside its
  assurance.
- The **pooled** verbosity/self-preference/position numbers are correlations on confounded data
  and are explicitly **not** the basis of the verdict; the verdict rests on the **controlled**
  `_concise`/`_verbose` ablation, where length is manipulated and quality is held fixed.
- Length is measured in **characters** as a verbosity proxy; token-based length gives the same
  qualitative result but is not recomputed here.
- We audit the **raw** auto-annotator win-rate. AlpacaEval's **length-controlled** win-rate is a
  mitigation of exactly this confound and is **out of scope** — a model's LC number may be sound
  where its raw number is length-inflated.
- The self-preference and position questions are recorded as **untested** on this data, not as
  cleared; a family-swapped judge and published swapped-order verdicts would be needed to test
  them.
- Verdicts describe these files only; they are not a prediction of a differently-configured
  annotator's behavior.

---

## Sign-off

| | |
|---|---|
| Auditor | Eval Integrity audit tooling |
| Signature | __________________________ |
| Date | 2026-07-17 |
| Report ID | alpacaeval-gpt4turbo-winrate / alpacaeval_judge.json@05825e05 |

*This Eval Integrity Report certifies that the listed numbers were honestly measured under the
controls described. It does not certify that the annotator, or any model it ranks, is good,
safe, or fit for any purpose. Its central finding is a bounded, causally-demonstrated length
confound in the raw win-rate; it expressly declines to certify two further biases the generic
battery surfaces but the data cannot support.*
