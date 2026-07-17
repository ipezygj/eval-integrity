# Eval Integrity Finding — RewardBench v1: two length-degenerate subsets

> **Filed upstream:** [allenai/reward-bench#267](https://github.com/allenai/reward-bench/issues/267).
>
> A real measurement audit of a public leaderboard
> (`allenai/reward-bench`), produced with the Eval Integrity tooling. Every number was
> recomputed from the benchmark's own published gold data and from a top model's published
> per-example scores (Appendix A). No data was fabricated. Free to share.
>
> **Calibrated on purpose.** The claim is *not* "RewardBench is broken." The aggregate is
> sound and the hard subsets genuinely discriminate. The claim is narrow, quantified, and
> reproducible: **two specific subsets have zero power to separate the property the benchmark
> measures (reward quality) from answer length**, and they make up ~54% of the Chat category.

---

## 1. Target

- **Leaderboard:** RewardBench (Lambert et al., AI2) — the standard reward-model benchmark.
  Score = a reward model's accuracy at ranking a **chosen** response above a **rejected** one
  over 2,985 gold pairs, aggregated into four categories (Chat, Chat Hard, Safety, Reasoning).
- **Raw data audited (both public):**
  - Gold pairs with response *text*: `allenai/reward-bench`, split `filtered` (2,985 rows).
  - A top model's *per-example* correctness: `allenai/reward-bench-results`,
    `Skywork/Skywork-Reward-Gemma-2-27B-v0.2` (a former #1) and
    `NCSOFT/Llama-3-OffsetBias-RM-8B` (a reward model explicitly trained to *reduce* bias).

## 2. The measurement bug

A benchmark that claims to measure **reward-model quality** must not be solvable by a control
that has no access to quality. The natural null control for a preference benchmark is a
**length-only predictor**: *always pick the longer response.* On a quality benchmark that
control must sit near chance (50%). It does not, on two subsets:

### Length-only baseline ("pick the longer response"), recomputed from the gold pairs

| Slice | Length-only accuracy | n (decided) |
|---|---:|---:|
| **Overall (all 2,985 pairs)** | **42.6%** | 2,617 |
| Chat category | 80.6% | 356 |
| Chat Hard category | 29.3% | 454 |
| Safety category | 41.9% | 740 |
| Reasoning category | 36.2% | 1,067 |
| **`alpacaeval-easy` subset** | **100.0%** | 99 |
| **`alpacaeval-hard` subset** | **100.0%** | 94 |
| `alpacaeval-length` subset | 64.2% | 95 |
| `llmbar-adver-neighbor` subset | 11.9% | 134 |
| `math-prm` subset | 7.8% | 447 |
| `refusals-dangerous` subset | 8.0% | 100 |

**Reading it.** Overall the benchmark is length-*robust* (42.6% < chance — the authors
deliberately inverted length on the adversarial/reasoning subsets, e.g. `math-prm` 7.8%,
`llmbar-adver-neighbor` 11.9%). That is good design and is stated here explicitly. **But two
subsets are length-degenerate:** on `alpacaeval-easy` and `alpacaeval-hard` the gold "chosen"
answer is the longer one in **100% of pairs.** A zero-parameter length ruler scores **100%**
there.

### Why: strong-long vs weak-short model matchup (mechanism)

| Subset | chosen model (len) | rejected model (len) | chosen/rejected length ratio |
|---|---|---|---:|
| `alpacaeval-easy` | GPT4-Turbo (2064 ch) | alpaca-7b (428 ch) | **4.83×** |
| `alpacaeval-hard` | tulu-2-dpo-70b (1378 ch) | davinci-003 (314 ch) | **4.39×** |

The pairs contrast a strong, verbose model against a weak, terse one, so *length* and *the
gold label* are perfectly collinear. Anything that prefers length aces the subset;
the subset therefore cannot tell a quality reward model apart from a length preference.
(Contrast `alpacaeval-length`, which the authors length-balanced to 0.93× — that one works.)

### The confound is live in the leaderboard numbers

| Subset | length-ruler | Skywork-Gemma-27B (SOTA RM) | OffsetBias-8B (anti-bias RM) |
|---|---:|---:|---:|
| `alpacaeval-easy` | **100.0%** | 97.0% | 97.0% |
| `alpacaeval-hard` | **100.0%** | 94.7% | 94.7% |

On these two subsets a length ruler **matches or beats** the #1 reward model. Their
contribution to a model's Chat score is not evidence of reward quality — it is evidence the
model prefers the longer answer, which every model here does. Since the two subsets are
**~54% of the Chat category by count** (193 of 356 decided pairs), a meaningful share of the
headline Chat number is uninformative.

### Not an artifact of "the models are just length-biased"

The same two models beat the length signal decisively where length is *reversed* —
`llmbar-adver-neighbor` (length-ruler 11.9% → Skywork 87.3%), `math-prm` (7.8% → 100%),
`refusals-dangerous` (8.0% → 97%). So the reward models genuinely model quality; the defect is
in **two subsets' gold construction**, not in the models. This two-sided check is what
separates a real finding from a hasty "leaderboard is length-biased" claim.

## 3. Impact / recommendation

- **For anyone quoting a RewardBench v1 Chat number:** discount `alpacaeval-easy` and
  `alpacaeval-hard` — a model can score ~100% on them by preferring length, so they inflate
  the Chat category for any length-preferring model and cannot rank quality among strong ones.
- **Fix (matches the authors' own `alpacaeval-length` approach):** length-match or
  length-stratify the chosen/rejected pairs, or report a length-controlled Chat accuracy
  alongside the raw one. (RewardBench 2 rebuilt these subsets — this finding is the v1
  quantification of exactly that motivation, and v1 remains widely cited.)

## 4. Honesty boundaries

- This audits the **integrity of the measurement** on the published gold pairs and one model's
  published scores — not model quality, not the whole benchmark, not RewardBench 2.
- "Length-degenerate" means *a length-only control scores at ceiling on these subsets*, so they
  cannot discriminate quality from length there. It does **not** mean the chosen answers are
  worse — GPT4-Turbo genuinely beats alpaca-7b; the point is the subset can't *prove* a reward
  model knows that rather than just counting characters.
- Character length is the verbosity proxy; token length gives the same qualitative picture.

---

## Appendix A — Reproduction

**Data (public, downloaded 2026-07-17)**
- Gold pairs: HF `allenai/reward-bench`, split `filtered` (2,985 rows), via
  `https://datasets-server.huggingface.co/rows?dataset=allenai/reward-bench&config=default&split=filtered` (paginated).
  Derived file `rewardbench_filtered.json` SHA-256 `b2a9c08c4025e180f64ed41b7d798a62dcc58c78d5c0ca3c60e83bfd9d952a0d`.
- Model scores: HF `allenai/reward-bench-results`,
  `eval-set-scores/Skywork/Skywork-Reward-Gemma-2-27B-v0.2.json`
  (SHA-256 `fcb0fcbcfa3942ba63887aafa6bd198cb3901f42bfb7d82b08b3ec9df6d7580a`),
  `eval-set-scores/NCSOFT/Llama-3-OffsetBias-RM-8B.json`
  (SHA-256 `6a27c120d916f4778f4ae1641b5247842040ae5fce3521b172b4c75309c6aab9`).

**Method** — length-only baseline: for each gold pair predict *chosen* iff
`len(chosen) > len(rejected)`; accuracy = fraction of decided pairs where chosen is the longer
(ties excluded). Model per-subset accuracy = mean of the published `results` array grouped by
`subset`. Category mapping per the RewardBench paper. Pure Python stdlib, no RNG — deterministic.

**Expected result:** overall length baseline 42.6%; `alpacaeval-easy` and `alpacaeval-hard`
= 100.0%; Skywork 97.0% / 94.7% on the same two subsets; and the length baseline < 12% on
`math-prm` / `llmbar-adver-neighbor` / `refusals-dangerous` while the models exceed 87% there.
