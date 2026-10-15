import csv, re, sys
p = sys.argv[1]
rows = list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
def syl(s): return [x for x in re.split(r"[་།\s…]+", s) if x]
for r in rows:
    if len(syl(r["words"])) > 25:
        parts = [x.strip() for x in r["words"].split("…")]
        # trim each part proportionally
        out = []
        budget = 24
        for i, part in enumerate(parts):
            ss = syl(part)
            out.append(ss)
        tot = sum(len(x) for x in out)
        res = []
        for ss in out:
            k = max(2, round(len(ss) * budget / tot))
            res.append(ss if len(ss) <= k else ss[:k//2] + ["…"] + ss[-(k - k//2):])
        r["words"] = " … ".join("་".join(x).replace("་…་", " … ") for x in res)
        assert len(syl(r["words"])) <= 25, (r["line"], len(syl(r["words"])))
w = csv.DictWriter(open(p, "w", encoding="utf-8", newline=""), fieldnames=["heading","root_block","line","kind","words"], delimiter="\t", lineterminator="\n")
w.writeheader(); w.writerows(rows)
