import sys, csv, collections
a, b = int(sys.argv[1]), int(sys.argv[2])
L = open("source.md", encoding="utf-8").read().replace("\r\n","\n").split("\n")
seeds = collections.defaultdict(list)
for r in csv.DictReader(open("seeds/seeds-P7.tsv", encoding="utf-8"), delimiter="\t"):
    seeds[int(r["line"])].append(r)
out = []
for i in range(a, b+1):
    l = L[i-1]
    if not l.strip(): continue
    out.append(f"{i}: {l}")
    for r in seeds.get(i, []):
        out.append(f"   SEED {r['root_block']} n={r['matched_syllables']} also={r['same_words_also_match']} | {r['preview']}")
sys.stdout.reconfigure(encoding="utf-8")
print("\n".join(out))
