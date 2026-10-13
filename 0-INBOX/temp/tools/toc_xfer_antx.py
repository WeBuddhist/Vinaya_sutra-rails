"""Transfer TOC heading lines from an old headed text onto a human-segmented text with antx,
then stamp body block IDs. Writes to --out; never touches the inputs.
usage: toc_xfer.py HEADED_SOURCE HUMAN_TARGET --out OUT [--lib SEG_TOC_LIB_DIR]"""
import sys, re, time, argparse
from diff_match_patch import diff_match_patch
import antx.core as core

class PyDMP:                                   # pure-python DMP instead of antx's downloaded binary
    def __init__(self):
        self.d = diff_match_patch(); self.d.Diff_Timeout = 0
    def diff_main(self, a, b):
        return self.d.diff_main(a, b)
core.optimized_diff_match_patch = PyDMP

ap = argparse.ArgumentParser()
ap.add_argument("source"); ap.add_argument("target"); ap.add_argument("--out", required=True)
ap.add_argument("--lib", required=True)
a = ap.parse_args()
sys.path.insert(0, a.lib)
from toc_tree_ingest import split_doc, stamp_body_ids

FM = re.compile(r"\A---\n.*?\n---\n", re.S)
src = FM.sub("", open(a.source, encoding="utf-8").read())
src = "\n".join(l if l.startswith("#") else re.sub(r"[ \t]+\^[\w-]+[ \t]*$", "", l)
                for l in src.split("\n"))                           # drop old body IDs
tgt_raw = open(a.target, encoding="utf-8").read()
m = FM.match(tgt_raw); tgt_fm = m.group(0) if m else ""; tgt = tgt_raw[len(tgt_fm):]
assert not re.search(r"(?m)^#{1,6} ", tgt), "target already has headings"
assert "\x00" not in tgt

t = time.time()
diffs = core.transfer(src, [["heading", r"(?m)(^#{1,6} [^\n]*$)"]], tgt, output="diff")
print(f"antx diff: {time.time()-t:.1f}s")

heads, buf = [], []
for op, txt, tag in diffs:
    if tag == "heading":
        buf.append(f"\x00{len(heads)}\x00"); heads.append(txt)
    elif op != -1:
        buf.append(txt)
text = "".join(buf)
assert len(heads) == len(re.findall(r"(?m)^#{1,6} ", src)), "lost a heading"

# the ingest convention (commentary-toc-ingest): a first child (depth > 1, last segment 1)
# stacks at the start of the block that contains it -- the human paragraph, or the point
# where an earlier heading in that paragraph cut it; every other heading cuts the block
def first_child(h):
    m = re.search(r"\^([\w-]+)-0\s*$", h)
    segs = m.group(1).split("-") if m else []
    return len(segs) >= 2 and segs[-1] == "1"
pre_text = text
toks = re.split(r"(\x00\d+\x00)", text)
out_t, block_start = [], 0                   # block_start: index in out_t where the current block begins
for tk in toks:
    mk = re.fullmatch(r"\x00(\d+)\x00", tk)
    if not mk:
        breaks = list(re.finditer(r"\n[ \t]*\n", tk))
        if breaks:
            cut = breaks[-1].end()
            out_t.append(tk[:cut]); out_t.append(tk[cut:])
            block_start = len(out_t) - 1
        else:
            out_t.append(tk)
        continue
    if first_child(heads[int(mk.group(1))]):
        out_t.insert(block_start, tk)         # stack at the start of the containing block
        block_start += 1
    else:
        out_t.append(tk)                      # a new section cuts the block here
        block_start = len(out_t)
text = "".join(out_t)
assert re.sub(r"\x00\d+\x00", "", text) == re.sub(r"\x00\d+\x00", "", pre_text)
# a heading that lands inside a paragraph splits it; count those
splits = []
for mm in re.finditer(r"\x00(\d+)\x00", text):
    before = re.sub(r"\x00\d+\x00", "", text[:mm.start()]).rstrip(" \t")
    after = re.sub(r"\x00\d+\x00", "", text[mm.end():]).lstrip(" \t")
    if before and not before.endswith("\n\n") and after and not after.startswith("\n\n"):
        splits.append(int(mm.group(1)))
text = re.sub(r"\s*(\x00\d+\x00)\s*", r"\n\n\1\n\n", text).strip("\n")
text = re.sub(r"\x00(\d+)\x00", lambda k: heads[int(k.group(1))], text)

# position check: the words after each heading, old vs new (marks, shads, spaces ignored)
def canon(s): return re.sub(r"[\s༄༅།]", "", s)
def follow(doc):
    out, ls = [], doc.split("\n")
    for i, l in enumerate(ls):
        if re.match(r"#{1,6} ", l):
            rest = "".join(x for x in ls[i+1:i+40] if not re.match(r"#{1,6} ", x))
            out.append((l, canon(rest)[:15]))
    return out
fo, fn = follow(src), follow(re.sub(r'\x00(\d+)\x00', lambda k: '\n'+heads[int(k.group(1))]+'\n', pre_text))
bad = [(o[0], o[1], n[1]) for o, n in zip(fo, fn) if o[1] != n[1]]

_, paras = split_doc(text)
out = stamp_body_ids(paras)
open(a.out, "w", encoding="utf-8").write(tgt_fm + "\n\n".join(out) + "\n")
ids = re.findall(r"\^([\w-]+)$", "\n".join(out), flags=re.M)
print(f"headings transferred: {len(heads)}  paragraphs split by a heading: {len(splits)}  "
      f"position mismatches: {len(bad)}  block IDs: {len(ids)}  duplicate IDs: {len(ids)-len(set(ids))}")
for i in splits[:40]: print("  split:", heads[i][:90])
for h, o, n in bad[:40]: print("  MISMATCH:", h[:70], "| old:", o, "| new:", n)
