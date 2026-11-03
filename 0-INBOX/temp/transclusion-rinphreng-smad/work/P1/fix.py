import csv, re, pathlib, collections, sys
sys.stdout.reconfigure(encoding="utf-8")
H = pathlib.Path(__file__).resolve().parents[2]
L = (H/"source.md").read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
head = {}; cur = ""
for i,l in enumerate(L,1):
    if l.startswith("#"):
        m = re.search(r"\^([\w-]+)\s*$", l); cur = m.group(1) if m else cur
    head[i] = cur
rows = list(csv.DictReader(open(H/"work/P1/rows.tsv",encoding="utf-8"),delimiter="\t"))
bad = [(r["line"],r["heading"],head[int(r["line"])]) for r in rows if r["heading"]!=head[int(r["line"])]]
print("heading mismatches:", bad)
for r in rows: r["heading"]=head[int(r["line"])]
rows.sort(key=lambda r:(int(r["line"]), [int(x) if x.isdigit() else 0 for x in r["root_block"].split("-")]))
with open(H/"place-P1.tsv","w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,delimiter="\t",lineterminator="\n"); w.writerow(["heading","root_block","line","kind","words"])
    for r in rows: w.writerow([r[k] for k in ["heading","root_block","line","kind","words"]])
seeds = list(csv.DictReader(open(H/"seeds/seeds-P1.tsv",encoding="utf-8"),delimiter="\t"))
S = {(int(s["line"]),s["root_block"]) for s in seeds}
R = {(int(r["line"]),r["root_block"]) for r in rows}
print("seeds",len(S),"kept",len(S&R),"dropped",len(S-R),"added",len(R-S))
print(collections.Counter(r["kind"] for r in rows))
print(sorted(collections.Counter(r["root_block"].split("-")[0] for r in rows).items()))
