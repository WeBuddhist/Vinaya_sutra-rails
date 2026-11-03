import re, csv, sys, json, pathlib, collections
sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
T = HERE.parents[1]
VAULT = T.parents[2]
SRC = T / "source.md"
ROOT = VAULT / "1-SOURCES" / "Text" / "འདུལ་བ་མདོ་རྩ་བ།.md"
A, B = 503, 1247
L = SRC.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
# blocks
blocks = []; heading = None; cur = None
for i in range(len(L)):
    ln = i + 1; l = L[i]
    if l.startswith("#"):
        m = re.search(r"\^([\w-]+)\s*$", l)
        heading = m.group(1) if m else heading
        cur = None; continue
    if not l.strip():
        cur = None; continue
    if cur is None:
        cur = {"line": ln, "heading": heading, "text": l}
        blocks.append(cur)
    else:
        cur["text"] += "\n" + l
blocks = [b for b in blocks if A <= b["line"] <= B]
for b in blocks:
    m = re.search(r"\^([\w-]+)\s*$", b["text"]); b["id"] = m.group(1) if m else "?"
# root
root = {}
rl = ROOT.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
buf = []
for l in rl:
    if l.startswith("#"): buf = []; continue
    if not l.strip(): continue
    buf.append(l)
    m = re.search(r"\^([\w-]+)\s*$", l)
    if m:
        root[m.group(1)] = " ".join(buf); buf = []
def syl(s):
    s = re.sub(r"\^[\w-]+", " ", s)
    s = re.sub(r"[།༎༏༐༑༔༄༅༆༇༈༉༊་\s]+", " ", s)
    return [x for x in s.split() if x]
rootsyl = {k: " " + " ".join(syl(v)) + " " for k, v in root.items()}
def find(seq):
    q = " " + " ".join(seq) + " "
    return [k for k, v in rootsyl.items() if q in v]
MARK = re.compile(r"ཞེས་(?:བྱ་བ|སྨོས|པ|སོ|གསུངས|བཤད|བྱའོ|བྱ་སྟེ)")
def lemmas(text):
    out = []
    for m in MARK.finditer(text):
        pre = text[max(0, m.start() - 400):m.start()]
        s = syl(pre)[-20:]
        best = None
        for n in range(len(s), 1, -1):
            hits = find(s[-n:])
            if hits:
                best = (n, hits, " ".join(s[-n:])); break
        if best and best[0] >= 3:
            out.append(best)
    return out
seeds = collections.defaultdict(list)
for r in csv.DictReader(open(T / "seeds" / "seeds-P2.tsv", encoding="utf-8"), delimiter="\t"):
    seeds[int(r["line"])].append(r)
mode = sys.argv[1] if len(sys.argv) > 1 else "report"
if mode == "report":
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    for b in blocks:
        if not lo <= b["line"] <= hi: continue
        print(f"=== L{b['line']} [{b['id']}] h={b['heading']} len={len(b['text'])}")
        for r in seeds.get(b["line"], []):
            print(f"  S {r['root_block']} m={r['matched_syllables']} also={r['same_words_also_match']} | {r['preview'][:80]}")
        sd = {r["root_block"] for r in seeds.get(b["line"], [])}
        for n, hits, s in lemmas(b["text"]):
            if len(hits) > 4 and n < 5: continue
            hs = ",".join(hits[:6]) + ("+" if len(hits) > 6 else "")
            new = "*" if not (set(hits) & sd) else " "
            print(f"  L{new}n={n} [{hs}] {s[-60:]}")
elif mode == "text":
    ln = int(sys.argv[2])
    for b in blocks:
        if b["line"] == ln: print(b["text"])
elif mode == "root":
    for k in sys.argv[2:]: print(k, root.get(k))
elif mode == "ctx":
    ln = int(sys.argv[2]); pat = sys.argv[3]; w = int(sys.argv[4]) if len(sys.argv) > 4 else 150
    for b in blocks:
        if b["line"] == ln:
            t = b["text"]
            for m in re.finditer(pat, t):
                print("...", t[max(0, m.start()-w):m.end()+w].replace("\n", " "), "...")
elif mode == "compact":
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    for b in blocks:
        if not lo <= b["line"] <= hi: continue
        ss = seeds.get(b["line"], [])
        c2 = [f"{r['root_block']}({r['matched_syllables']})" for r in ss if r["root_block"].startswith("2-")]
        oth = [r for r in ss if not r["root_block"].startswith("2-")]
        print(f"=== L{b['line']} [{b['id']}] ch2: {' '.join(c2)}")
        if oth:
            print("   other: " + " ".join(f"{r['root_block']}({r['matched_syllables']})" for r in oth))
            for r in oth:
                if int(r["matched_syllables"]) >= 8: print(f"     ! {r['root_block']} {r['preview'][:90]}")
        sd = {r["root_block"] for r in ss}
        for n, hits, s in lemmas(b["text"]):
            if set(hits) & sd: continue
            if len(hits) > 3 and n < 6: continue
            if n < 4 and not any(h.startswith("2-") for h in hits): continue
            print(f"   L* n={n} [{','.join(hits[:5])}] {s[-50:]}")
elif mode == "sc":
    # sc line:root [line:root ...]
    for arg in sys.argv[2:]:
        ln, rb = arg.split(":"); ln = int(ln)
        b = [x for x in blocks if x["line"] == ln][0]
        for r in seeds.get(ln, []):
            if r["root_block"] != rb: continue
            sy = [s for s in re.split(r"[་།\s]+", r["preview"]) if s and not re.match(r"^[\d-]+$", s)]
            pat = r"[་།\s]*".join(map(re.escape, sy[:6]))
            m = re.search(pat, b["text"])
            if m:
                print(f"--- {ln}:{rb} ... " + b["text"][max(0, m.start()-120):m.end()+120].replace("\n", " "))
            else:
                print(f"--- {ln}:{rb} (not located) {r['preview']}")
elif mode == "lem":
    for a in sys.argv[2:]:
        ln = int(a)
        b = [x for x in blocks if x["line"] == ln][0]
        out = [m.group(1)[-70:] for m in re.finditer(r"([^།]*(?:།\s*།?)?[^།]*?)ཞེས་(?:བྱ་བ|སྨོས|གསུངས)", b["text"])]
        print(f"== {ln}: " + " || ".join(out))
elif mode == "missing":
    done = {int(l.split()[0]) for l in open(HERE / "rows.txt", encoding="utf-8") if l.strip()}
    for b in blocks:
        if b["line"] not in done:
            print(b["line"], b["id"], b["text"][:170].replace("\n", " "))
elif mode == "build":
    bl = {b["line"]: b for b in blocks}
    out = ["heading\troot_block\tline\tkind\twords"]
    nowords = []
    seen = set()
    for l in open(HERE / "rows.txt", encoding="utf-8"):
        p = l.rstrip("\n").split(" ", 3)
        if len(p) < 3: continue
        ln, rb, kind = int(p[0]), p[1], p[2]
        if (ln, rb) in seen: print("DUP", ln, rb); continue
        seen.add((ln, rb))
        words = p[3].strip() if len(p) > 3 else ""
        if not words:
            best = None
            for n, hits, s in lemmas(bl[ln]["text"]):
                if rb in hits and (best is None or n > best[0]): best = (n, s)
            if best and best[0] >= 4:
                words = "་".join(best[1].split()[-25:])
            else:
                cand = [r for r in seeds.get(ln, []) if r["root_block"] == rb]
                if cand:
                    r = max(cand, key=lambda r: int(r["matched_syllables"]))
                    sy = [x for x in re.split(r"[་།\s]+", r["preview"]) if x and not re.match(r"^[\d-]+$", x)]
                    words = "་".join(sy[:25])
                elif best:
                    words = "་".join(best[1].split())
        if not words: nowords.append((ln, rb))
        out.append(f"{bl[ln]['heading']}\t{rb}\t{ln}\t{kind}\t{words}")
    (T / "place-P2.tsv").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(len(out) - 1, "rows; no words:", nowords)
