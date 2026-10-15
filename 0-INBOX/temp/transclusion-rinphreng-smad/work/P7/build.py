import csv, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
L = open("source.md", encoding="utf-8").read().replace("\r\n","\n").split("\n")
def heading(ln):
    for i in range(ln-1, 0, -1):
        l = L[i-1]
        if l.startswith("#"):
            m = re.search(r"\^([\w-]+)\s*$", l); return m.group(1) if m else ""
    return ""
rows = [l.rstrip("\n").split("\t") for l in open("work/P7/rows.tsv", encoding="utf-8") if l.strip()]
out = ["heading\troot_block\tline\tkind\twords"]
for ln, rb, kind, words in rows:
    syl = [s for s in re.split(r"[་།\s…]+", words) if s]
    if len(syl) > 25: print("LONG", ln, rb, len(syl))
    out.append(f"{heading(int(ln))}\t{rb}\t{ln}\t{kind}\t{words}")
open("place-P7.tsv", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
mine = {(int(r[0]), r[1]) for r in rows}
seeds = list(csv.DictReader(open("seeds/seeds-P7.tsv", encoding="utf-8"), delimiter="\t"))
sk = {(int(s["line"]), s["root_block"]) for s in seeds}
print("rows", len(rows), "kinds", collections.Counter(r[2] for r in rows))
print("seed pairs", len(sk), "kept", len(sk & mine), "dropped", len(sk - mine), "added", len(mine - sk))
print("added:", sorted(mine - sk))
print("chapters", sorted({r[1].split('-')[0] for r in rows}))
