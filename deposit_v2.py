"""Version 2: corrections to what this census says about its sources. No new measurement."""
import argparse, io, json, os, sys, time
import urllib.request, urllib.error

API = "https://zenodo.org/api/deposit/depositions"
PUBLISHED_ID = "22343059"
FILES = ["../eval-integrity.zip"]

NOTE = """

<p><strong>Version 2 (18 September 2026).</strong> No measurement changed: every hash, item count,
McNemar test and bootstrap that was recomputed came back identical. Fifteen statements about external
sources or about a leaderboard's own ranking did not. Two are structural. The GPQA report named
<code>Daemontatox/Llama3.3-70B-CogniLink</code> as the leader and audited its 3.69-point lead; that
model ranks seventh of 4,576, because the ranking was taken from roughly the first tenth of the
dataset in its native order and never sorted against the whole. The real top gap is 0.16 points at
p = 0.94, so the conclusion is stronger, but a named author's model was published as the board's best
when it is not. The RewardBench report hardcoded the model pairs it called rank 1 and rank 2 and got
all four categories wrong; recomputed over all 151 models with complete coverage, three of the four
top pairs are still not separable but Reasoning is (p = 0.002), so "in any of the four categories"
was too strong, and the issue filed on the RewardBench tracker has been corrected in place. The
remaining thirteen are listed in the corrections note on the site page: a tier boundary decided in the
fourth decimal, several claims attributed to the MT-Bench authors that they do not make, credit given
to the RewardBench 2 authors for an intent their paper never states, two tie counts, a subset claim
about models that held for one of two, and a summary page that contradicted the report beneath
it.</p>"""


def call(url, token, method="GET", payload=None, raw=None, ctype="application/json"):
    data = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
    last = None
    for attempt in range(5 if method in {"GET", "PUT", "DELETE"} else 1):
        if attempt:
            time.sleep(5 * attempt)
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", "Bearer " + token)
        if data is not None:
            req.add_header("Content-Type", ctype)
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                body = r.read()
                return r.status, (json.loads(body) if body else {})
        except urllib.error.HTTPError as e:
            last = e.code
            if e.code in (502, 503, 504):
                continue
            return e.code, {"error": e.read().decode("utf-8", "replace")[:500]}
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = type(e).__name__
            continue
    return 504, {"error": "gave up (%s)" % last}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default=os.environ.get("ZENODO_TOKEN"))
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--finish-draft")
    a = ap.parse_args()
    if not a.token:
        sys.exit("no token")
    for f in FILES:
        if not os.path.exists(f):
            sys.exit("missing %s" % f)

    st, cur = call("%s/%s" % (API, PUBLISHED_ID), a.token)
    if st >= 300:
        sys.exit("cannot read published deposition: %s" % cur)
    meta = cur["metadata"]
    for k in ("doi", "prereserve_doi", "relations"):
        meta.pop(k, None)
    meta["publication_date"] = "2026-09-18"
    meta["version"] = "2"
    if "Version 2 (18 September 2026)" not in meta["description"]:
        meta["description"] = meta["description"] + NOTE

    if a.finish_draft:
        dep = a.finish_draft
    else:
        st, r = call("%s/%s/actions/newversion" % (API, PUBLISHED_ID), a.token, "POST")
        print("newversion:", st)
        if st >= 300:
            sys.exit(str(r))
        dep = r["links"]["latest_draft"].rsplit("/", 1)[1]
        print("draft:", dep)

    st, r = call("%s/%s" % (API, dep), a.token)
    if st >= 300:
        sys.exit(str(r))
    for f in r.get("files", []):
        st2, _ = call("%s/%s/files/%s" % (API, dep, f["id"]), a.token, "DELETE")
        print("removed old file %s: %s" % (f.get("filename"), st2))
    for f in FILES:
        st, rr = call("%s/%s" % (r["links"]["bucket"], os.path.basename(f)), a.token, "PUT",
                      raw=io.open(f, "rb").read(), ctype="application/octet-stream")
        print("upload %-28s %s" % (f, st))
        if st >= 300:
            sys.exit(str(rr))
    st, r2 = call("%s/%s" % (API, dep), a.token, "PUT", payload={"metadata": meta})
    print("metadata:", st, r2.get("error", ""))
    if st >= 300:
        sys.exit(str(r2))
    if a.publish:
        st, r3 = call("%s/%s/actions/publish" % (API, dep), a.token, "POST")
        print("publish:", st, r3.get("doi") or r3.get("error", r3))
        if st < 300:
            print("PUBLISHED: https://doi.org/%s" % r3.get("doi"))
    else:
        print("draft ready: https://zenodo.org/deposit/%s" % dep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
