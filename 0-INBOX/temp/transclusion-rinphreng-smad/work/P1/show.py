import sys, csv, pathlib
H = pathlib.Path(__file__).resolve().parents[2]
L = (H/"source.md").read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
seeds = {}
for r in csv.DictReader(open(H/"seeds"/"seeds-P1.tsv",encoding="utf-8"),delimiter="\t"):
    seeds.setdefault(int(r["line"]),[]).append(r)
a,b = int(sys.argv[1]), int(sys.argv[2])
out = []
for i in range(a-1, b):
    l = L[i]
    if not l.strip(): continue
    out.append(f"[{i+1}] {l}")
    if seeds.get(i+1):
        out.append("   SEEDS: "+" ".join(f"{r['root_block']}({r['matched_syllables']})" for r in seeds[i+1]))
sys.stdout.reconfigure(encoding="utf-8")
print("\n".join(out))
