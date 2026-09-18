"""Corrections after re-reading every sourced claim, 18 September 2026.

Two of these are structural and serious: in both the GPQA and the RewardBench
reports the models audited as "rank 1 and rank 2" were not the top of the board.
In GPQA the ranking was taken from a partial pull of the leaderboard; in
RewardBench the pairs were hardcoded in the reproduce script and never derived
from the data at all. The methodological conclusions survive - in GPQA it becomes
stronger - but the facts stated under them were wrong, and one named someone's
model as the leaderboard leader when it sits seventh.
"""
import io, sys, pathlib

FILES = {}


def edit(path, old, new, label):
    FILES.setdefault(path, []).append((old, new, label))


G = "reports/gpqa-power-underpowered.md"

edit(G,
     """| C1 | Model **#1** outranks model **#2** on GPQA — its higher GPQA score reflects genuinely stronger graduate-level reasoning. | GPQA accuracy | #1 = **44.55%**, #2 = **40.86%** (a **+3.5pp** lead that sets the #1 rank) | `open-llm-leaderboard/contents` (HF), field `GPQA Raw` |""",
     """| C1 | The top-ranked model outranks the second on GPQA — its higher GPQA score reflects genuinely stronger graduate-level reasoning. | GPQA accuracy | rank 1 = **47.06%**, rank 2 = **46.90%** (a **+0.16pp** lead that sets the top rank) | `open-llm-leaderboard/contents` (HF), field `GPQA Raw`, all 4,576 rows |""",
     "gpqa claim row")

edit(G,
     """The #1-vs-#2 GPQA gap that determines the top ranking (**+3.5pp**) is **not statistically
distinguishable from noise** at any plausible GPQA sample size.""",
     """The gap that determines the top ranking (**+0.16pp**) is **not statistically
distinguishable from noise** at any plausible GPQA sample size (p = 0.94 at n = 1,192).""",
     "gpqa headline")

edit(G,
     """percentage points is inside the sampling noise. Auditing the #1-vs-#2 gap (44.55% vs 40.86%) as a
two-proportion comparison, across every plausible GPQA `n`:""",
     """percentage points is inside the sampling noise. The table below audits a **3.69pp** gap as a
two-proportion comparison across every plausible GPQA `n`. That gap is not the top-rank gap — see the
correction note at the end — but it is retained here because it is the *harder* case: the real
top-rank gap is 0.16pp and fails to separate by a wider margin at every `n` in the table.""",
     "gpqa table intro")

edit(G,
     """**Reading it.** This does not say model #1 is *not* better — it says the GPQA score *cannot tell you
whether it is*. The whole top of the GPQA ranking is compressed: the top ~12 models span roughly
5pp (44.6% down to ~39.4%), a spread smaller than the benchmark's own MDE.""",
     """**Reading it.** This does not say the leading model is *not* better — it says the GPQA score
*cannot tell you whether it is*. The whole top of the GPQA ranking is compressed: over the full
leaderboard the top ten models span **3.6pp** (47.06% down to 43.46%), a spread far inside the
benchmark's own MDE.""",
     "gpqa reading")

edit(G,
     """**Data (public):** `open-llm-leaderboard/contents` on Hugging Face (via datasets-server `/rows`),
field **`GPQA Raw`** (raw accuracy). Top two by GPQA Raw at time of pull (2026-07-18):
#1 `Daemontatox/Llama3.3-70B-CogniLink` = 0.4455, #2 (tie at 0.4086) e.g. `EVA-UNIT-01/EVA-Qwen2.5-72B-v0.2`.""",
     """**Data (public):** `open-llm-leaderboard/contents` on Hugging Face (via datasets-server `/rows`),
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
author's model as the leaderboard's best on GPQA when it is not.""",
     "gpqa appendix")


R = "reports/rewardbench-category-ties.md"

edit(R,
     """**On its own sample, RewardBench cannot separate the displayed #1 from #2 in any of the four categories.**""",
     """**On its own sample, RewardBench cannot separate the top pair in three of its four categories.**""",
     "rb headline")

edit(R,
     """The ~2,985-item headline metric separates most models fine.""",
     """The headline metric — a weighted average of section scores rather than a pooled 2,985-item
accuracy — separates most models fine.""",
     "rb headline metric")


L = "reports/livecodebench-second-tier.md"

edit(L,
     """Ranks 2–6 — O3, O4-Mini (Medium), DeepSeek-R1, and both Gemini-2.5-Pro snapshots — are mutually indistinguishable (all #2-vs-#k p ≥ 0.05).""",
     """Ranks 2–5 are mutually indistinguishable. Rank 6, `Gemini-2.5-Pro-05-06`, sits **exactly on the
threshold**: the p-value printed as 0.050 in the table above is below 0.05 before rounding, so under
the stated rule it separates and the tier is four models, not five. A tier boundary decided in the
fourth decimal is not a boundary, which is the report's own argument turned on itself.""",
     "lcb tier")


M = "reports/mt-bench-gpt4-judge.md"

edit(M,
     """| Claim as stated | "GPT-4's pairwise A/B verdicts are a reliable, order-invariant measure of answer quality." |""",
     """| Claim as used | "GPT-4's pairwise A/B verdicts are a reliable, order-invariant measure of answer quality." *(This is how the verdicts are used downstream, not a claim Zheng et al. make. Their paper examines position, verbosity and self-enhancement bias and limited reasoning ability, and reports GPT-4 consistency at 65.0%.)* |""",
     "mtbench claim as stated")

edit(M,
     """measure of answer quality, tested for the four documented LLM-judge biases (position,""",
     """measure of answer quality, tested for the three biases and one limitation the paper documents (position,""",
     "mtbench four biases")

edit(M,
     """  CRITICAL. The honest read: order matters a little, and 12.9% of paired verdicts literally
  **flip when the two answers swap seats** (87.1% consistency), matching the order-sensitivity
  the paper reports.""",
     """  CRITICAL. The honest read: order matters a little, and 12.9% of paired verdicts literally
  **flip when the two answers swap seats** (87.1% consistency). This is *not* the same quantity the
  paper reports: Zheng et al. measure 65.0% consistency for GPT-4 on a deliberately hard set of
  near-identical answers, and note the test is hard for humans too. Our 87.1% on their released
  file is a different measurement, not agreement with theirs.""",
     "mtbench consistency")

edit(M,
     """  for losers (1.13×). This is the "LLM judges reward length" effect the MT-Bench authors""",
     """  for losers (1.13×). This is what the MT-Bench authors call verbosity bias — their words are
  "favors longer, verbose responses", not the phrase used here — and note that for this judge they
  report resistance rather than the effect (8.7% failure under their verbosity attack, against 91.3%
  for the other judges they tested). The MT-Bench authors""",
     "mtbench length attribution")


B2 = "reports/rewardbench2-focus-length.md"

edit(B2,
     """**Credit first:** RewardBench 2 *fixed* the v1 length degeneracy. A content-blind "pick the longest completion" baseline scores **21.3% overall — below the 24.8% chance rate.** The authors clearly corrected the aggregate.""",
     """**Credit first:** on RewardBench 2 the v1 length degeneracy is gone. A content-blind "pick the longest completion" baseline scores **21.3% overall — below the 24.8% chance rate.** Whether that was deliberate is not something this measurement can say, and the paper does not discuss length bias or length control anywhere; the earlier version of this report asserted that the authors corrected it on purpose, which is not supported.""",
     "rb2 intent")

edit(B2,
     """(RewardBench 2 rebuilt these subsets — this finding is the v1 quantification of exactly that motivation, and v1 remains widely cited.)""",
     """(RewardBench 2 has no Chat domain and no AlpacaEval-derived subsets; the paper describes Math, Safety and Focus as new datasets "inspired by improving upon" v1's Math, Safety and Chat-Hard, and uses unseen prompts rather than existing downstream evaluations. The earlier wording here, that it "rebuilt these subsets", overstated the connection. v1 remains widely cited.)""",
     "rb2 rebuilt")


T = "reports/leaderboard-significance-tiers.md"

edit(T, """| MBPP+ | 378 | O1 Preview (80.2%) | ~10 |""",
     """| MBPP+ | 378 | O1 Preview (80.2%) | 6 |""", "mbpp count")

edit(T, """| Open LLM · MUSR | 756 | calme-3.2 (60.2%) | top-15 all one tier |""",
     """| Open LLM · MUSR | 756 | calme-3.2 (60.2%) | 8 |""", "musr count")


LN = "reports/rewardbench-length-degeneracy.md"

edit(LN,
     """`math-prm` / `llmbar-adver-neighbor` / `refusals-dangerous` while the models exceed 87% there.""",
     """`math-prm` / `llmbar-adver-neighbor` / `refusals-dangerous`, while Skywork reaches 87.3 / 100.0 /
97.0 there. OffsetBias does not: it scores 76.1 on `llmbar-adver-neighbor` and 82.0 on
`refusals-dangerous`, so "the models exceed 87%" held for one of the two, not both.""",
     "length models exceed")


D = "docs/index.md"

edit(D,
     """MMLU-PRO (12,032 items) separates a 1-point gap; IFEval (541–834) and MUSR (756) cannot resolve their tightly-packed tops.""",
     """MMLU-PRO (12,032 items) separates a 1-point gap; MUSR (756) cannot resolve its tightly-packed top. IFEval does separate its leader (p = 0.037 at n = 834) and then flattens: the report has this right and an earlier version of this page had it backwards.""",
     "index ifeval")

edit(D,
     """I checked MMLU-Pro for answer-position skew — the full 12,032-item pull is uniform (an earlier hunch, refuted by the data).""",
     """I checked MMLU-Pro for answer-position skew — uniform across the 9,981 items that have all ten options (an earlier hunch, refuted by the data). Pooling all 12,032 makes the marginal look skewed only because 2,051 items have fewer than ten options; the earlier wording here claimed uniformity over the full pull, which is not what the data shows.""",
     "index mmlu uniform")


NOTE = """

---

## Corrections, 18 September 2026

Every claim in these reports about an external source, and every number
describing a leaderboard's own ranking, was re-checked against the source. Fifteen
did not survive. Two of them are structural and are the reason this note leads
with them.

**The GPQA report audited the wrong models.** It named
`Daemontatox/Llama3.3-70B-CogniLink` as the GPQA leader with a 3.69pp lead. That
model ranks seventh of 4,576. The ranking had been taken from roughly the first
tenth of the dataset in its native order and never sorted against the whole. The
true top gap is 0.16pp at p = 0.94, so the conclusion is stronger than before,
but a named author's model was published as the board's best when it is not.

**The RewardBench report audited the wrong pairs, in all four categories.** The
models were hardcoded in the reproduce script rather than derived from the board.
Recomputed over all 151 models with complete coverage: Chat is led by
`sfairXC/FsfairX-LLaMA3-RM-v0.1`, Chat Hard and Reasoning by
`infly/INF-ORM-Llama3.1-70B`, Safety by `Skywork/Skywork-Reward-Gemma-2-27B-v0.2`,
and the overall board by INF-ORM rather than the Skywork model named here. On the
corrected pairs, three of the four categories are still not separable
(p = 1.000, 0.864, 0.568) but **Reasoning is** (p = 0.002), so "in any of the four
categories" was too strong. The issue filed on the RewardBench tracker has been
corrected in place.

The rest, in brief: the LiveCodeBench second tier has four models rather than five,
because the sixth sits just below the 0.05 threshold it was printed as meeting;
the MT-Bench report attributed to Zheng et al. a claim of order-invariance they
never make and in fact test and report failing, compared our 87.1% swap
consistency to their 65.0% as though the two agreed, put the phrase "LLM judges
reward length" in their mouths, and counted "blind leakage" among their documented
biases when it is our own probe; the RewardBench 2 report credited the authors
with deliberately correcting a length bias their paper never discusses, and said
they "rebuilt" subsets that do not exist in v2; the MBPP+ tie count is 6, not
about 10; the MUSR tie count is 8, not the top fifteen; one of the two reward
models quoted as exceeding 87% on three subsets reaches 76.1 and 82.0 on two of
them; the RewardBench headline is a weighted average of section scores, not a
pooled 2,985-item accuracy; and on this site the IFEval claim contradicted the
report it summarised, with the data on the report's side, while the MMLU-Pro
uniformity claim holds for the ten-option items rather than the full pull.

Nothing in the measurements changed. Every hash, every item count, every McNemar
and bootstrap that was recomputed came back identical.
"""


def main():
    for path, edits in FILES.items():
        p = pathlib.Path(path)
        if not p.exists():
            print("MISSING FILE:", path)
            continue
        s = io.open(p, encoding="utf-8").read()
        applied, missed = 0, []
        for old, new, label in edits:
            n = s.count(old)
            if n == 1:
                s = s.replace(old, new)
                applied += 1
            else:
                missed.append("%s(%d)" % (label, n))
        io.open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("%-46s %d/%d %s" % (path, applied, len(edits),
                                  ("MISSED: " + ", ".join(missed)) if missed else ""))
    idx = pathlib.Path("docs/index.md")
    s = io.open(idx, encoding="utf-8").read()
    if "## Corrections, 18 September 2026" not in s:
        io.open(idx, "w", encoding="utf-8", newline="\n").write(s.rstrip() + "\n" + NOTE)
        print("corrections note appended to docs/index.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
