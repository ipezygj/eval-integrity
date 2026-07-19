#!/usr/bin/env python3
"""
Reproduce: the top of the SWE-bench Verified leaderboard is one statistical tier.

SWE-bench Verified is scored as % of 500 fixed instances resolved, and the leaderboard shows a
strict rank order. Because every submission is scored on the SAME 500 instances, the honest test of
a #1-vs-#k gap is the PAIRED McNemar test on the discordant instances (the ones exactly one of the
two solves). This script downloads the canonical 500 instance IDs and each submission's public
`resolved` list from the official swe-bench/experiments repo, builds per-instance pass/fail vectors,
and runs paired McNemar. The top ~8 submissions are mutually indistinguishable; #1 first separates
around rank 9.

No third-party deps, no model inference, no RNG. Deterministic. Pure stdlib.
"""
import json
import math
import urllib.request
import sys

# split: "verified" (n=500, default) or "lite" (n=300) — same method, both reproducible
SPLIT = sys.argv[1] if len(sys.argv) > 1 else "verified"
_DS = {"verified": ("princeton-nlp/SWE-bench_Verified", 500),
       "lite": ("princeton-nlp/SWE-bench_Lite", 300),
       "multimodal": ("princeton-nlp/SWE-bench_Multimodal", 510)}[SPLIT]
HF = (f"https://datasets-server.huggingface.co/rows?dataset={_DS[0]}"
      "&config=default&split=test")
LIST = f"https://api.github.com/repos/swe-bench/experiments/contents/evaluation/{SPLIT}"
RAW = ("https://raw.githubusercontent.com/swe-bench/experiments/main/evaluation/"
       + SPLIT + "/{}/results/results.json")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "eval-integrity-repro"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def chi_sf_1df(x):
    return math.erfc(math.sqrt(x / 2.0))


def mcnemar(a, b):
    B = sum(1 for x, y in zip(a, b) if x and not y)
    C = sum(1 for x, y in zip(a, b) if y and not x)
    stat = (abs(B - C) - 1) ** 2 / (B + C) if (B + C) > 0 else 0.0
    return B, C, stat, chi_sf_1df(stat)


def main():
    # 1) canonical 500 Verified instance IDs
    IDS = []
    for off in range(0, _DS[1], 100):
        d = get(f"{HF}&offset={off}&length=100")
        IDS += [row["row"]["instance_id"] for row in d["rows"]]
    idset = set(IDS)
    print(f"Verified instances: {len(IDS)}", file=sys.stderr)

    # 2) all submission names, keep the recent (2025/2026) high scorers
    names = [x["name"] for x in get(LIST)]
    subs = [s for s in names if s[:4] in ("2025", "2026")]
    scores = {}
    for s in subs:
        try:
            scores[s] = set(get(RAW.format(s)).get("resolved", []))
        except Exception:
            pass
    print(f"submissions scored: {len(scores)}", file=sys.stderr)

    # 3) rank by resolved-of-500
    ranked = sorted(scores.items(), key=lambda kv: -len(kv[1] & idset))

    def vec(res):
        return [1 if i in res else 0 for i in IDS]

    print("\nSWE-bench Verified — top 12 by resolved (of 500):")
    for i, (s, res) in enumerate(ranked[:12]):
        n = len(res & idset)
        print(f"  {i+1:2}. {n/len(IDS)*100:5.1f}%  ({n}/{len(IDS)})  {s}")

    # 4) #1 vs each lower rank -> tier-1 size
    v1 = vec(ranked[0][1])
    tied = 1
    print("\n#1 vs each lower rank (paired McNemar):")
    for i in range(1, min(15, len(ranked))):
        s2, res2 = ranked[i]
        B, C, stat, p = mcnemar(v1, vec(res2))
        sep = p < 0.05
        print(f"  #1 vs #{i+1:2} ({len(res2 & idset)/len(IDS)*100:.1f}%): disc {B}/{C}  p={p:.3f}  "
              f"{'** SEPARATES **' if sep else 'TIED'}")
        if sep:
            break
        tied += 1

    print("\n" + "=" * 66)
    print(f"REPRODUCED: the top {tied} SWE-bench {SPLIT} submissions are one statistical "
          f"tie; #1 first separates at rank {tied+1}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
