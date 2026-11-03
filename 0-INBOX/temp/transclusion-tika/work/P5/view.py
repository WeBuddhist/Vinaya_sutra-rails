import re, csv, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent
T = HERE.parents[1]
SRC = (T/"source.md").read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
seeds = collections.defaultdict(list)
for r in csv.DictReader(open(T/"seeds"/"seeds-P5.tsv",encoding="utf-8"),delimiter="\t"):
    alt = r["same_words_also_match"]
    seeds[int(r["line"])].append(f"{r['root_block']}:{r['matched_syllables']}" + (f"(+{alt})" if alt else ""))
lem = collections.defaultdict(list); cur=None
for l in open(HERE/"lemmas.txt",encoding="utf-8"):
    m = re.match(r"=== (\d+)", l)
    if m: cur=int(m.group(1)); continue
    m = re.search(r"ch8=\[(.*)\]", l)
    if m and m.group(1):
        first = re.findall(r"\((\d+), '([\w-]+)'\)", m.group(1))
        if first and int(first[0][0])>=3:
            lem[cur].append(f"{first[0][1]}:{first[0][0]}")
A,B=2539,3420
out=open(HERE/"view.txt","w",encoding="utf-8")
i=A-1
while i<B:
    l=SRC[i]
    if l.strip() and not l.startswith("#") and (not SRC[i-1].strip() or SRC[i-1].startswith("#")):
        j=i; txt=[]
        while SRC[j].strip(): txt.append(SRC[j]); j+=1
        out.write(f"[{i+1}] " + " ".join(txt) + "\n")
        out.write(f"   SEEDS: {' '.join(seeds[i+1])}\n   LEM8: {' '.join(lem[i+1])}\n")
        i=j
    else: i+=1
