import sys, re, pathlib, csv
sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parents[1] / "source.md"
L = SRC.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
a, b = int(sys.argv[1]), int(sys.argv[2])
seeds = {}
for r in csv.DictReader(open(HERE.parents[1] / "seeds" / "seeds-P5.tsv", encoding="utf-8"), delimiter="\t"):
    seeds.setdefault(int(r["line"]), []).append(f'{r["root_block"]}({r["matched_syllables"]}{"|"+r["same_words_also_match"] if r["same_words_also_match"] else ""})')
for i in range(a - 1, b):
    l = L[i]
    if not l.strip(): continue
    if l.startswith("#"):
        print(f"{i+1} H {l[:80]}"); continue
    s = " ".join(seeds.get(i + 1, []))
    print(f"{i+1}: {l}" + (f"\n   SEEDS: {s}" if s else ""))
