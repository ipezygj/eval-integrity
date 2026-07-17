# Eval Integrity Report

> Fill every `‹…›` placeholder. Delete guidance blockquotes before issuing. One
> "Claim" section per metric under audit. Probe tables are populated directly from the
> `measurement_audit.py` / `judge_audit.py` probe output — one row per probe.

---

## 1. Engagement header

| Field | Value |
|---|---|
| Client | ‹legal entity name› |
| Client contact | ‹name, role, email› |
| Engagement type | ‹Single Headline Claim · Full Eval Suite · Pre-Fundraise Retainer · VC Diligence› |
| Commissioned by | ‹client / investor name› |
| Report date | ‹YYYY-MM-DD› |
| Report version | ‹v1.0› |
| Auditor | ‹auditor name› |
| Tooling | measurement_audit.py ‹commit/version›, judge_audit.py ‹commit/version› |
| Determinism | Fixed seed (‹1337›); all figures reproducible per Appendix A. |

### Scope

> State exactly which claims are in scope and which are explicitly out of scope.

**In scope:** ‹list the claims/metrics audited›

**Out of scope:** ‹e.g. model quality, benchmark selection, data provenance, security›

### Claims under audit

| # | Claim (as stated by client) | Metric | Claimed value | Source (deck/page, doc, commit) |
|---|---|---|---|---|
| C1 | ‹"…"› | ‹recall› | ‹0.50› | ‹pitch deck p.7› |
| C2 | ‹"…"› | ‹judge win-rate› | ‹0.61› | ‹…› |

---

## 2. Overall verdict

> Derived from the per-claim verdicts. The engagement verdict is no stronger than its
> weakest in-scope claim.

**Overall: ‹TRUSTWORTHY · SUSPECT · ARTIFACT / JUDGE-BIASED›**

| Claim | Metric | Claimed | Recomputed | Verdict |
|---|---|---|---|---|
| C1 | ‹recall› | ‹0.50› | ‹0.50› | ‹TRUSTWORTHY› |
| C2 | ‹judge win-rate› | ‹0.61› | ‹0.61› | ‹JUDGE-BIASED› |

Summary: ‹two or three sentences: what holds, what does not, and the single most
important finding.›

---

## 3. Per-claim findings

> Duplicate this section per claim.

### Claim C1 — ‹short label›

| Field | Value |
|---|---|
| Claim as stated | ‹"…"› |
| Metric | ‹recall› |
| Claimed value | ‹0.50› |
| Recomputed value | ‹0.50› |
| Sample size (n) | ‹rows; positives / negatives› |
| Claimed cause (if any) | ‹"lens X"› |
| **Verdict** | **‹TRUSTWORTHY · SUSPECT · ARTIFACT›** |

#### Probe table

> One row per probe from `measurement_audit.py`. Severity ∈ {OK, INFO, WARN, CRITICAL}.
> Mark structural (metric-choice) criticals as such — they cap the verdict at SUSPECT but
> do not on their own declare an ARTIFACT.

| Probe | Result / key figures | Severity | Structural? |
|---|---|---|---|
| control_blind | ‹blind score vs floor› | ‹OK› | — |
| control_promiscuous | ‹flag-everything score on headline› | ‹WARN› | ‹yes/no› |
| permutation_test | ‹real score vs null band (p=…)› | ‹OK› | — |
| base_rate | ‹majority-class baseline› | ‹INFO› | — |
| metric_panel | ‹P / R / F1 / MCC / acc› | ‹OK› | — |
| surface_area | ‹volume↔hits correlation› | ‹OK› | — |
| ground_truth | ‹dupes / degenerate / leakage / balance› | ‹OK› | — |
| ablation_coherence | ‹metric delta when cause removed vs noise› | ‹CRITICAL› | ‹no› |

#### Reasoning

> Explain how the verdict follows from the probes. Cite the *discriminating* evidence that
> drove it (ablation flip, failed permutation, MCC collapse, blind leak, broken ground
> truth). If a critical was structural, say so and explain why it caps at SUSPECT rather
> than declaring an ARTIFACT.

‹reasoning›

---

### Claim C2 — ‹short label› (LLM-judge)

| Field | Value |
|---|---|
| Claim as stated | ‹"…"› |
| Metric | ‹judge win-rate› |
| Claimed value | ‹0.61› |
| Recomputed value | ‹0.61› |
| Number of judgments (n) | ‹pairwise comparisons› |
| Judge family | ‹claude / gpt / …› |
| **Verdict** | **‹TRUSTWORTHY · SUSPECT · JUDGE-BIASED›** |

#### Probe table

> One row per probe from `judge_audit.py`. Each bias is gated behind a significance test —
> record the rate and its p-value.

| Probe | Result / key figures | Severity |
|---|---|---|
| position_bias | ‹P(pos-1 wins)=…, flip_rate=…, p=…› | ‹OK› |
| verbosity_bias | ‹P(longer wins)=…, p=…› | ‹CRITICAL› |
| self_preference | ‹own-family win-rate=…, p=…› | ‹OK / n/a› |
| blind_control | ‹blind-predicts-real rate=…› | ‹OK› |
| degeneracy | ‹tie / one-sided share› | ‹OK› |

#### Reasoning

‹reasoning — which bias(es) reached significance, and what that means for the claim.›

---

## Appendix A — Reproduction

> Everything an independent party needs to re-run the audit and obtain identical figures.

**Tooling**
- `measurement_audit.py` — ‹commit hash / version›
- `judge_audit.py` — ‹commit hash / version›
- Python ‹version›; no third-party ML dependencies (pure stdlib).
- Seed: ‹1337› (deterministic).

**Inputs** (delivered with this report; hashes fix the exact bytes audited)
| File | Description | SHA-256 |
|---|---|---|
| ‹C1_claim.json› | predictions + labels (+ groups / ablation) for C1 | ‹hash› |
| ‹C2_judge.json› | pairwise judgments for C2 | ‹hash› |

**Commands**
```bash
python measurement_audit.py C1_claim.json
python judge_audit.py       C2_judge.json
```

**Expected result:** ‹paste the VERDICT line(s) the client should reproduce.›

> Exit codes: measurement_audit.py exits non-zero on MEASUREMENT-ARTIFACT; judge_audit.py
> exits non-zero on JUDGE-BIASED — so re-execution can be wired into the client's CI.

---

## Appendix B — Limitations

- This report attests to the **integrity of the measurement** on the data supplied, not to
  the provenance of that data. Fabricated inputs are outside its assurance.
- Verdicts describe the audited data set only; they are not a prediction of performance on
  other data or in production.
- Out-of-scope items (§1) were not examined and carry no assurance.
- ‹engagement-specific caveats›

---

## Sign-off

> The auditor attests only to what the controls show, and derives every verdict from them.

| | |
|---|---|
| Auditor | ‹name› |
| Signature | __________________________ |
| Date | ‹YYYY-MM-DD› |
| Report ID | ‹unique id / hash of this document› |

*This Eval Integrity Report certifies that the listed numbers were honestly measured under
the controls described. It does not certify that the model is good, safe, or fit for any
purpose.*
