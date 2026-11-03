"""Extract lemma candidates from P4 commentary blocks and locate them in root ch.7 blocks.
usage: python -I lemmas.py  (run from vault root) -> writes work/P4/lemmas.txt
"""
import re, csv, pathlib, difflib
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent
T = HERE.parents[1]
VAULT = T.parents[2]
SRC = T / "source.md"
ROOT = VAULT / "1-SOURCES" / "Text" / "འདུལ་བ་མདོ་རྩ་བ།.md"
LO, HI = 2035, 2538

def syl(s):
    s = re.sub(r"\^[\w-]+\s*$", "", s)
    s = re.sub(r"[།༎༑༔\s]+", "་", s)
    return [x for x in s.split("་") if x]

# root blocks of ch 7 (and all, for reference)
root = {}
for l in ROOT.read_text(encoding="utf-8").splitlines():
    m = re.search(r"\^([\w-]+)\s*$", l)
    if m and not l.startswith("#"):
        root[m.group(1)] = l
ch7 = [(k, syl(v)) for k, v in root.items() if k.startswith("7-")]
ch7.sort(key=lambda kv: int(kv[0].split("-")[1]))

L = SRC.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
blocks = []
for i in range(LO - 1, HI):
    l = L[i]
    if l.strip() and not l.startswith("#") and (i == 0 or not L[i - 1].strip() or L[i - 1].startswith("#")):
        blocks.append([i + 1, l])
    elif l.strip() and blocks and not l.startswith("#"):
        blocks[-1][1] += " " + l

seeds = defaultdict(list)
for r in csv.DictReader(open(T / "seeds" / "seeds-P4.tsv", encoding="utf-8"), delimiter="\t"):
    seeds[int(r["line"])].append(r)

LEM = re.compile(r"([^།]*?)\s*ཞེས་(?:བྱ་བ|པ)(?:་(ནི|སྨྲས|སྨོས|ལ|ནས|ཡང|དང|གསུངས|འདི|ལས|བཤད|སྨོས་པ)|འི་བར)")

def best(lem):
    out = []
    for k, rs in ch7:
        sm = difflib.SequenceMatcher(None, lem, rs, autojunk=False)
        m = sum(b.size for b in sm.get_matching_blocks())
        longest = max((b.size for b in sm.get_matching_blocks()), default=0)
        out.append((longest, m, k))
    out.sort(reverse=True)
    return out[:3]

with open(HERE / "lemmas.txt", "w", encoding="utf-8") as f:
    for ln, text in blocks:
        bid = re.search(r"\^([\w-]+)\s*$", text)
        f.write(f"=== {ln} ^{bid.group(1) if bid else '?'}\n")
        for m in LEM.finditer(text):
            lem_txt = m.group(1).strip()
            lem_txt = re.sub(r"^.*དེའི་ཕྱིར[།\s]*", "", lem_txt)
            if "ཐ་ཚིག" in text[m.end():m.end() + 12]:
                continue
            ls = syl(lem_txt)
            if not ls:
                continue
            b = best(ls[-12:])
            f.write(f"  L[{len(ls)}] {lem_txt[-80:]}  ->  " + "; ".join(f"{k}:{lg}/{mm}" for lg, mm, k in b) + "\n")
        s7 = sorted({(r["root_block"], int(r["matched_syllables"])) for r in seeds[ln] if r["root_block"].startswith("7-")}, key=lambda x: -x[1])
        so = [(r["root_block"], r["matched_syllables"], r["preview"][:60]) for r in seeds[ln] if not r["root_block"].startswith("7-")]
        if s7:
            f.write("  S7 " + " ".join(f"{a}:{b}" for a, b in s7) + "\n")
        for a, b, p in so:
            f.write(f"  SX {a}:{b} {p}\n")
print(len(blocks), "blocks")
