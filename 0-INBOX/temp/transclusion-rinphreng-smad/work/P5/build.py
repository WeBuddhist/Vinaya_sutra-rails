import sys, re, pathlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parents[1]
L = (BASE / "source.md").read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
rows = []
for l in (HERE / "rows.txt").read_text(encoding="utf-8").splitlines():
    if not l.strip(): continue
    ln, rb, kind, words = l.split("\t")
    ln = int(ln)
    h = ""
    for i in range(ln - 1, -1, -1):
        if L[i].startswith("#"):
            m = re.search(r"\^([\w-]+)\s*$", L[i]); h = m.group(1) if m else ""; break
    rows.append((ln, rb, h, kind, words))
key = lambda r: (r[0], [int(x) for x in r[1].split("-")])
rows.sort(key=key)
with open(BASE / "place-P5.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("heading\troot_block\tline\tkind\twords\n")
    for ln, rb, h, kind, words in rows:
        f.write(f"{h}\t{rb}\t{ln}\t{kind}\t{words}\n")
print(len(rows))
