import re, sys, csv, pathlib, collections
sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
T = HERE.parents[1]
VAULT = T.parents[2]
SRC = T / "source.md"
ROOT = VAULT / "1-SOURCES" / "Text" / "འདུལ་བ་མདོ་རྩ་བ།.md"
A, B = int(sys.argv[1]), int(sys.argv[2])
def syl(s):
    s = re.sub(r"\^[\w-]+\s*$", "", s)
    s = re.sub(r"[།༎༄༅\s]+", "་", s)
    return [x for x in s.split("་") if x]
roots = {}
for l in ROOT.read_text(encoding="utf-8").split("\n"):
    m = re.search(r"\^([\w-]+)\s*$", l)
    if m and not l.startswith("#"): roots[m.group(1)] = syl(l)
idx = collections.defaultdict(list)
for b, s in roots.items():
    for i in range(len(s) - 1): idx[(s[i], s[i+1])].append((b, i))
def best(w):
    res = {}
    for i in range(len(w) - 1):
        for b, p in idx.get((w[i], w[i+1]), []):
            k = 0
            rs = roots[b]
            while i + k < len(w) and p + k < len(rs) and w[i+k] == rs[p+k]: k += 1
            # prefer runs ending nearer the end of window
            sc = (k, i + k)
            if b not in res or sc > res[b][0]: res[b] = (sc, i, k)
    return res
seeds = collections.defaultdict(list)
for r in csv.DictReader(open(T/"seeds"/"seeds-P3.tsv", encoding="utf-8"), delimiter="\t"):
    seeds[int(r["line"])].append(f'{r["root_block"]}:{r["matched_syllables"]}' + (f'[{r["same_words_also_match"]}]' if r["same_words_also_match"] else "") + "{" + r["preview"] + "}")
L = SRC.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
head = ""
MK = re.compile(r"(ཞེས|ཅེས|ཤེས)་(བྱ|པ|སོ|སོགས|གསུངས|བཤད|སྨོས|འབྱུང|ཟེར|ཏེ|པའི)")
for i in range(A - 1, B):
    l = L[i]
    if l.startswith("#"):
        m = re.search(r"\^([\w-]+)\s*$", l); head = m.group(1) if m else head
        print(f"\n######## {l[:80]}"); continue
    if not l.strip() or (i > 0 and L[i-1].strip() and not L[i-1].startswith("#")): continue
    m = re.search(r"\^([\w-]+)\s*$", l); cid = m.group(1) if m else "?"
    print(f"\n=== L{i+1} [{cid}] h={head} seeds: {' '.join(seeds.get(i+1, []))}")
    print("  >> " + "་".join(syl(l)[:(18 if MK.search(l) else 45)]))
    for mm in MK.finditer(l):
        pre = l[:mm.start()]
        w = syl(pre)[-22:]
        if not w: continue
        r = best(w)
        cand = sorted(r.items(), key=lambda x: (-x[1][0][0], -x[1][0][1]))
        ch = [c for c in cand if c[0].split("-")[0] in ("3","4","5","6")]
        top = []
        for b, (sc, st, k) in (ch[:2] + cand[:1]):
            if k >= 3 and (b, k) not in [(t[0], t[1]) for t in top]:
                top.append((b, k, "་".join(w[st:st+k])))
        tail = "་".join(w[-10:])
        print(f"  * …{tail} |{mm.group(0)}| " + " ; ".join(f"{b}({k}):{s}" for b, k, s in top))
    for mm in re.finditer(r"(འདི་ཉིད་ལས|རྩ་བ|མདོ་རྩ|གཞུང་ལས|ལུང་|འགྲེལ་པ|རང་གི་རྣམ་པར་བཤད|མཛོད|སློབ་དཔོན)", l):
        print(f"  @ {mm.group(0)}: " + l[mm.start():mm.start()+90].replace("\n"," "))
