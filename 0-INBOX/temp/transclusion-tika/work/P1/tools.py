import csv, re, sys, pathlib, collections
sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parents[2]
VAULT = HERE.parents[2]
SRC = HERE / "source.md"
ROOT = VAULT / "1-SOURCES" / "Text" / "འདུལ་བ་མདོ་རྩ་བ།.md"
L = SRC.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")

def syl(s):
    s = re.sub(r"\^[\w-]+\s*$", "", s)
    s = re.sub(r"[༄༅།༎༔\s]+", "་", s)
    return [x for x in s.split("་") if x]

# root blocks
RB = {}
cur = []
for line in ROOT.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n"):
    if line.startswith("#"):
        cur = []; continue
    if not line.strip():
        continue
    cur.append(line)
    m = re.search(r"\^([\w-]+)\s*$", line)
    if m:
        RB[m.group(1)] = syl(" ".join(cur)); cur = []
RJ = {k: "་" + "་".join(v) + "་" for k, v in RB.items()}

def blocks(a, b):
    out = []; head = None; i = 0
    while i < len(L):
        l = L[i]
        if l.startswith("#"):
            m = re.search(r"\^([\w-]+)\s*$", l); head = m.group(1) if m else head; i += 1; continue
        if not l.strip() or l.startswith("---"):
            i += 1; continue
        st = i; txt = []
        while i < len(L) and L[i].strip() and not L[i].startswith("#"):
            txt.append(L[i]); i += 1
        if a <= st + 1 <= b:
            m = re.search(r"\^([\w-]+)\s*$", txt[-1])
            out.append((st + 1, m.group(1) if m else "?", head, "\n".join(txt)))
    return out

def find(q, chap=None):
    s = "་" + "་".join(syl(q)) + "་"
    return [k for k, v in RJ.items() if s in v and (chap is None or k.split("-")[0] == chap)]

def seeds():
    d = collections.defaultdict(list)
    for r in csv.DictReader(open(HERE / "seeds" / "seeds-P1.tsv", encoding="utf-8"), delimiter="\t"):
        d[int(r["line"])].append(r)
    return d

MARK = re.compile(r"(ཞེས་བྱ|ཞེས་པ|ཞེས་སྨོས|ཞེས་སོ|ཅེས་བྱ|ཅེས་པ|ཤེས་བྱ|ཞེས་གསུངས|ཞེས་བཤད|ཞེས་འབྱུང|ཞེས་སྨྲས)")
def lemmas(text, chap="1"):
    res = []
    for m in MARK.finditer(text):
        pre = syl(text[max(0, m.start() - 300):m.start()])[-25:]
        best = None
        for i in range(len(pre)):
            for j in range(len(pre), i + 1, -1):
                if j - i < 2 or (best and j - i <= best[0]): break
                ks = find("་".join(pre[i:j]), chap)
                if ks:
                    best = (j - i, "་".join(pre[i:j]), ks); break
        if best and best[0] >= 3:
            res.append(best)
    return res

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "show":
        a, b = int(sys.argv[2]), int(sys.argv[3]); sd = seeds()
        for ln, bid, head, txt in blocks(a, b):
            print(f"=== L{ln} ^{bid} [h {head}]")
            print(txt)
            for r in sd.get(ln, []):
                print(f"   SEED {r['root_block']} m{r['matched_syllables']} also[{r['same_words_also_match']}] {r['preview']}")
            for n, s, ks in lemmas(txt):
                print(f"   LEM {n} {ks[:6]} {s}")
            print()
    elif cmd == "find":
        print(find(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None))
    elif cmd == "root":
        for k in sys.argv[2:]:
            print(k, "་".join(RB[k]))
