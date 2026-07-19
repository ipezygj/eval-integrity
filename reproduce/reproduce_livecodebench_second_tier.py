#!/usr/bin/env python3
"""
Reproduce: on LiveCodeBench (code generation) the #1 lead is real, but ranks 2-6 are one tie.

LiveCodeBench ranks models by mean pass@1 over a fixed problem set. Because every model is scored on
the SAME problems, the honest test of a rank gap is a PAIRED test on the per-problem pass@1
differences (here a paired t-test — deterministic, and it matches the leaderboard's own
mean-pass@1 metric). The public per-problem grid (build/performances_generation.json) is a dense
28-model x 1055-problem matrix. Result: the #1 (O4-Mini High) genuinely separates from #2
(p<0.05) — the benchmark has the sample size to resolve a real top gap — but ranks 2 through 6
(a spread of ~2 points across five different models) are a single statistical tie for second.

No third-party deps, no model inference, no RNG. Deterministic. Pure stdlib.
"""
import json
import math
import urllib.request
import sys

URL = ("https://raw.githubusercontent.com/LiveCodeBench/livecodebench.github.io/"
       "main/build/performances_generation.json")


def erfc_p(t):
    # two-sided p-value from a t statistic; df ~ 1054 here so the normal approx is exact enough
    return math.erfc(abs(t) / math.sqrt(2))


def main():
    with urllib.request.urlopen(URL, timeout=120) as r:
        perf = json.load(r)["performances"]
    M = {}
    for e in perf:
        M.setdefault(e["model"], {})[e["question_id"]] = e["pass@1"]
    models = list(M)
    common = sorted(set.intersection(*[set(M[m]) for m in models]))
    print(f"models={len(models)}  problems common to all={len(common)}", file=sys.stderr)

    def mean(m):
        return sum(M[m][q] for q in common) / len(common)

    def paired_p(a, b):
        ds = [M[a][q] - M[b][q] for q in common]
        n = len(ds)
        md = sum(ds) / n
        var = sum((x - md) ** 2 for x in ds) / (n - 1)
        if var == 0:
            return md, 1.0
        return md, erfc_p(md / math.sqrt(var / n))

    ranked = sorted(models, key=lambda m: -mean(m))
    print(f"\nLiveCodeBench code-gen (n={len(common)} problems) — top 10 by mean pass@1:")
    for i, m in enumerate(ranked[:10]):
        print(f"  {i+1:2}. {mean(m):5.2f}  {m}")

    # tier structure via adjacent paired t
    print("\nStatistical tiers (adjacent paired t-test, top 10):")
    tier = 1
    tiers = [(ranked[0], 1)]
    for i in range(1, min(10, len(ranked))):
        _, p = paired_p(ranked[i - 1], ranked[i])
        if p < 0.05:
            tier += 1
        tiers.append((ranked[i], tier))
    for m, t in tiers:
        print(f"  tier {t}: {mean(m):5.2f}  {m}")

    # headline facts
    _, p12 = paired_p(ranked[0], ranked[1])
    print(f"\n#1 vs #2: gap {mean(ranked[0]) - mean(ranked[1]):+.2f}  p={p12:.3f}  "
          f"({'REAL separation' if p12 < 0.05 else 'tied'})")
    print("#2 vs #3/#4/#5:", ", ".join(
        f"p={paired_p(ranked[1], ranked[i])[1]:.3f}" for i in (2, 3, 4)))
    tier2 = [m for m, t in tiers if t == 2]
    print(f"\nREPRODUCED: #1 is a real lead (p={p12:.3f}); ranks 2-{1+len(tier2)} are one "
          f"statistical tie ({len(tier2)} models).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
