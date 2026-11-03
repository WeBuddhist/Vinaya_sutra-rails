import csv, pathlib, collections
H = pathlib.Path(__file__).resolve().parent
T = H.parents[1]
rows=[]; seen=set()
for l in open(H/"rows.tsv",encoding="utf-8"):
    l=l.rstrip("\n")
    if not l.strip(): continue
    ln,rb,kind,words=l.split("\t")
    k=(int(ln),rb)
    if k in seen: print("dup",k); continue
    seen.add(k); rows.append((int(ln),rb,kind,words))
def bkey(r): 
    c,n=r[1].split("-"); return (r[0], int(c)!=8, int(n))
rows.sort(key=bkey)
with open(T/"place-P5.tsv","w",encoding="utf-8",newline="") as f:
    f.write("heading\troot_block\tline\tkind\twords\n")
    for ln,rb,kind,w in rows: f.write(f"8-0\t{rb}\t{ln}\t{kind}\t{w}\n")
seeds=set((int(r["line"]),r["root_block"]) for r in csv.DictReader(open(T/"seeds"/"seeds-P5.tsv",encoding="utf-8"),delimiter="\t"))
kept=seen&seeds
print("rows",len(rows), collections.Counter(r[2] for r in rows))
print("seeds",len(seeds),"kept",len(kept),"dropped",len(seeds-kept),"added",len(seen-seeds))
print("chapters",collections.Counter(r[1].split("-")[0] for r in rows))
print("ch8 blocks covered", len({r[1] for r in rows if r[1].startswith("8-")}), "missing", sorted({f"8-{i}" for i in range(1,103)}-{r[1] for r in rows}, key=lambda x:int(x[2:])))
