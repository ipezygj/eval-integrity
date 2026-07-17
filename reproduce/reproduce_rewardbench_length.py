#!/usr/bin/env python3
"""Reproduce the RewardBench length-degeneracy finding. Pure stdlib, deterministic.

Downloads the public gold pairs (allenai/reward-bench) and one model's per-example scores
(allenai/reward-bench-results), then computes the length-only baseline ("always pick the
longer response") overall, per official category, and per subset -- and compares it to the
model on the two degenerate subsets. No third-party deps, no model inference, no RNG.
"""
import json, urllib.request
from collections import defaultdict

DS = "https://datasets-server.huggingface.co/rows?dataset=allenai/reward-bench&config=default&split=filtered&offset=%d&length=100"
RM = ("https://huggingface.co/datasets/allenai/reward-bench-results/resolve/main/"
      "eval-set-scores/Skywork/Skywork-Reward-Gemma-2-27B-v0.2.json")
CATS = {  # official RewardBench category -> subsets
 'Chat':['alpacaeval-easy','alpacaeval-length','alpacaeval-hard','mt-bench-easy','mt-bench-med'],
 'Chat Hard':['mt-bench-hard','llmbar-natural','llmbar-adver-neighbor','llmbar-adver-GPTInst',
              'llmbar-adver-GPTOut','llmbar-adver-manual'],
 'Safety':['refusals-dangerous','refusals-offensive','xstest-should-refuse',
           'xstest-should-respond','donotanswer'],
 'Reasoning':['math-prm','hep-cpp','hep-go','hep-java','hep-js','hep-python','hep-rust'],
}
sub2cat = {s: c for c, subs in CATS.items() for s in subs}

def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)

# 1. gold pairs (paginated)
rows, off = [], 0
while True:
    batch = get(DS % off).get('rows', [])
    if not batch: break
    rows += [x['row'] for x in batch]; off += len(batch)
    if len(batch) < 100: break
print("gold pairs:", len(rows))

# 2. length-only baseline: predict 'chosen' iff it is the longer response
tot = defaultdict(lambda: [0, 0]); cat = defaultdict(lambda: [0, 0]); c_all = d_all = 0
for r in rows:
    lc, lr = len(r['chosen']), len(r['rejected'])
    if lc == lr: continue                      # tie: undecided
    correct = lc > lr                          # True == longer response is the gold 'chosen'
    d_all += 1; c_all += correct
    tot[r['subset']][0] += correct; tot[r['subset']][1] += 1
    if r['subset'] in sub2cat:
        cat[sub2cat[r['subset']]][0] += correct; cat[sub2cat[r['subset']]][1] += 1

pct = lambda a, b: 100 * a / b if b else 0
print("\nLENGTH-ONLY BASELINE ('pick the longer response'):")
print("  OVERALL  %5.1f%%  (n=%d, chance=50%%)" % (pct(c_all, d_all), d_all))
for c in ['Chat', 'Chat Hard', 'Safety', 'Reasoning']:
    print("  %-10s %5.1f%%  (n=%d)" % (c, pct(*cat[c]), cat[c][1]))
print("  --- degenerate subsets ---")
for s in ['alpacaeval-easy', 'alpacaeval-hard', 'alpacaeval-length']:
    print("  %-16s %5.1f%%  (n=%d)" % (s, pct(*tot[s]), tot[s][1]))

# 3. cross-check a top model on the two degenerate subsets
m = get(RM); macc = defaultdict(lambda: [0, 0])
for res, s in zip(m['results'], m['subset']):
    macc[s][0] += res; macc[s][1] += 1
print("\n%s vs length ruler:" % m['model'])
for s in ['alpacaeval-easy', 'alpacaeval-hard']:
    print("  %-16s model %5.1f%%   length-ruler %5.1f%%" % (s, pct(*macc[s]), pct(*tot[s])))
