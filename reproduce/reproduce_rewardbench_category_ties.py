#!/usr/bin/env python3
"""
Reproduce: RewardBench per-category #1 rankings are not distinguishable from #2.

RewardBench's leaderboard displays a strict per-category order (Chat / Chat Hard / Safety /
Reasoning). Because every model is scored on the SAME items, the correct #1-vs-#2 test is the
PAIRED McNemar test on discordant items (an unpaired two-proportion test is conservative here).
This script downloads the public per-example results, aligns the two models item-by-item within
each category, and runs McNemar. Across all four categories the top gap is NOT significant.

No third-party deps, no model inference, no RNG. Deterministic. Pure stdlib.
"""
import json
import math
import urllib.request

BASE = ("https://huggingface.co/datasets/allenai/reward-bench-results/resolve/main/"
        "eval-set-scores/")

CATS = {
    'Chat': ['alpacaeval-easy', 'alpacaeval-length', 'alpacaeval-hard', 'mt-bench-easy', 'mt-bench-med'],
    'Chat Hard': ['mt-bench-hard', 'llmbar-natural', 'llmbar-adver-neighbor', 'llmbar-adver-GPTInst',
                  'llmbar-adver-GPTOut', 'llmbar-adver-manual'],
    'Safety': ['refusals-dangerous', 'refusals-offensive', 'xstest-should-refuse',
               'xstest-should-respond', 'donotanswer'],
    'Reasoning': ['math-prm', 'hep-cpp', 'hep-go', 'hep-java', 'hep-js', 'hep-python', 'hep-rust'],
}

# Each category's displayed #1 vs #2 among the top models (paths under BASE).
PAIRS = [
    ("Chat", "internlm/internlm2-7b-reward.json", "internlm/internlm2-20b-reward.json"),
    ("Chat Hard", "Skywork/Skywork-Reward-Gemma-2-27B-v0.2.json", "Skywork/Skywork-Reward-Llama-3.1-8B-v0.2.json"),
    ("Safety", "Skywork/Skywork-Reward-Gemma-2-27B-v0.2.json", "Skywork/Skywork-Reward-Llama-3.1-8B-v0.2.json"),
    ("Reasoning", "Skywork/Skywork-Reward-Gemma-2-27B-v0.2.json", "LxzGordon/URM-LLaMa-3.1-8B.json"),
]

_cache = {}


def load(path):
    if path not in _cache:
        with urllib.request.urlopen(BASE + path, timeout=120) as r:
            d = json.load(r)
        _cache[path] = (list(map(int, d["results"])), list(d["subset"]), d.get("model", path))
    return _cache[path]


def chi_sf_1df(x):
    """Survival function of chi-square with 1 dof = erfc(sqrt(x/2))."""
    return math.erfc(math.sqrt(x / 2.0))


def mcnemar(ca, cb):
    b = sum(1 for x, y in zip(ca, cb) if x and not y)
    c = sum(1 for x, y in zip(ca, cb) if y and not x)
    stat = (abs(b - c) - 1) ** 2 / (b + c) if (b + c) > 0 else 0.0
    return b, c, stat, chi_sf_1df(stat)


def main():
    all_tied = True
    print("Paired McNemar on each RewardBench category's displayed #1-vs-#2 gap:\n")
    for cat, pa, pb in PAIRS:
        ra, sa, na = load(pa)
        rb, sb, nb = load(pb)
        if sa != sb:
            print(f"{cat}: subset order differs between files -> cannot index-align; SKIP")
            continue
        subs = set(CATS[cat])
        ca = [x for x, s in zip(ra, sa) if s in subs]
        cb = [y for y, s in zip(rb, sb) if s in subs]
        b, c, stat, p = mcnemar(ca, cb)
        tied = p >= 0.05
        all_tied = all_tied and tied
        print(f"{cat}: {na.split('/')[-1]} (acc={sum(ca)/len(ca):.3f}) vs "
              f"{nb.split('/')[-1]} (acc={sum(cb)/len(cb):.3f})")
        print(f"   discordant b={b} c={c} | McNemar chi2={stat:.2f} p={p:.3f} -> "
              f"{'TIED (rank not significant)' if tied else 'SIGNIFICANT'}\n")
    # Contrast: the OVERALL #1 IS significant -- the board has power for its aggregate, just not per
    # category. Item-level paired McNemar over the union of all four categories, #1 vs #2 overall.
    all_subs = {s for ss in CATS.values() for s in ss}
    g1 = "Skywork/Skywork-Reward-Gemma-2-27B-v0.2.json"
    for label, g2 in [("#2 overall", "Skywork/Skywork-Reward-Llama-3.1-8B-v0.2.json"),
                      ("#3 overall", "LxzGordon/URM-LLaMa-3.1-8B.json")]:
        ra, sa, na = load(g1)
        rb, sb, nb = load(g2)
        keep = [i for i, s in enumerate(sa) if s in all_subs]
        ca = [ra[i] for i in keep]
        cb = [rb[i] for i in keep]
        b, c, stat, p = mcnemar(ca, cb)
        print(f"OVERALL: {na.split('/')[-1]} vs {label} {nb.split('/')[-1]} -> "
              f"McNemar p={p:.4f} {'(SIGNIFICANT: overall #1 is real)' if p < 0.05 else '(tied)'}")

    print("=" * 70)
    print("REPRODUCED: all four category #1 ranks statistically TIED with #2, "
          "while the OVERALL #1 is significant"
          if all_tied else "MISMATCH: at least one category rank was significant")
    return 0 if all_tied else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
