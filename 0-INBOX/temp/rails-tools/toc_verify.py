"""Verify the heading TOC already ingested into a commentary file.

usage: toc_verify.py FILE OUTDIR [--old-tree TREE]
Writes OUTDIR/structure.md (own checks), OUTDIR/tree.md (tree rebuilt from the
headings, [[N]] pointers into OUTDIR/body.md) and OUTDIR/body.md (file without
headings/frontmatter) so the skill's QC checkers can run on them.
"""
import re, sys, argparse, pathlib, collections

ap = argparse.ArgumentParser()
ap.add_argument("file"); ap.add_argument("outdir"); ap.add_argument("--old-tree")
a = ap.parse_args()
out = pathlib.Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

ORD = [("བཅུ་གསུམ་པ", 13), ("བཅུ་གཉིས་པ", 12), ("བཅུ་གཅིག་པ", 11), ("དང་པོ", 1), ("གཉིས་པ", 2),
       ("གསུམ་པ", 3), ("བཞི་པ", 4), ("ལྔ་པ", 5), ("དྲུག་པ", 6), ("བདུན་པ", 7), ("བརྒྱད་པ", 8),
       ("དགུ་པ", 9), ("བཅུ་པ", 10)]
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")

raw = pathlib.Path(a.file).read_text(encoding="utf-8").replace("\r\n", "\n")
raw = re.sub(r"\A---\n.*?\n---\n", "", raw, flags=re.S)
lines = raw.split("\n")

heads, body = [], []      # heads: dict(line, level, title, id, path, body_line)
for i, l in enumerate(lines, 1):
    m = H.match(l)
    if m:
        t = re.sub(r"\*\*(.+?)\*\*", r"\1", m.group(2)).strip()
        segs = m.group(3).split("-")
        heads.append(dict(line=i, level=len(m.group(1)), title=t, id=m.group(3),
                          path=tuple(segs[:-1]), last0=segs[-1] == "0", body_line=len(body) + 1))
    else:
        body.append(l)

issues = collections.defaultdict(list)
ids = collections.Counter(h["id"] for h in heads)
for k, v in ids.items():
    if v > 1: issues["duplicate heading ID"].append(f"^{k} ×{v}")
seen = {}
children = collections.defaultdict(list)
for idx, h in enumerate(heads):
    if not h["last0"]:
        issues["heading ID not ending in -0"].append(f"L{h['line']} ^{h['id']}")
    want = len(h["path"]) + 1
    if h["level"] != want:
        issues["# count ≠ ID depth"].append(f"L{h['line']} has {h['level']} #, ID depth needs {want}: ^{h['id']}")
    if idx and h["level"] > heads[idx - 1]["level"] + 1:
        issues["level skip"].append(f"L{h['line']} h{h['level']} after h{heads[idx-1]['level']}")
    par = h["path"][:-1]
    if h["path"] and par and par not in seen:
        issues["parent missing or after child"].append(f"L{h['line']} ^{h['id']} (parent {'-'.join(par)}-0)")
    children[par].append(h)
    seen[h["path"]] = h
    # Tibetan ordinal in the title vs last decimal
    last = h["path"][-1] if h["path"] else None
    if last and last.isdigit():
        for w, n in ORD:
            if h["title"].startswith(w):
                if n != int(last):
                    issues["title ordinal ≠ ID ordinal"].append(f"L{h['line']} '{w}' but ^{h['id']}: {h['title'][:50]}")
                break
# sibling sequences
for par, kids in children.items():
    kids = [k for k in kids if k["path"]]
    if not kids: continue
    nums = [k["path"][-1] for k in kids]
    if all(n.isdigit() for n in nums):
        nn = [int(n) for n in nums]
        if nn != list(range(nn[0], nn[0] + len(nn))) or nn[0] not in (0, 1):
            issues["sibling numbering gap/dup/order"].append(f"under {'-'.join(par) or 'root'}: {nn[:25]}")
# empty sections: heading followed directly by a heading that is not its child
for idx, h in enumerate(heads):
    nxt = heads[idx + 1] if idx + 1 < len(heads) else None
    between = "\n".join(lines[h["line"]:nxt["line"] - 1]).strip() if nxt else "\n".join(lines[h["line"]:]).strip()
    if not between and (nxt is None or nxt["path"][:len(h["path"])] != h["path"] or len(nxt["path"]) <= len(h["path"])):
        issues["empty section (no text, no children)"].append(f"L{h['line']} ^{h['id']} {h['title'][:50]}")

# rebuilt tree for the skill's checkers (decimal = ID path; zones like I / a kept out)
pathlib.Path(out, "body.md").write_text("\n".join(body), encoding="utf-8")
tl = ["## TOC rebuilt from file headings", ""]
for h in heads:
    if not h["path"] or not all(s.isdigit() for s in h["path"]):
        continue
    tl.append("   " * (len(h["path"]) - 1) + f"* {'.'.join(h['path'])} {h['title']} [[{h['body_line']}]]")
pathlib.Path(out, "tree.md").write_text("\n".join(tl) + "\n", encoding="utf-8")

# compare with the old tree
old_diff = []
if a.old_tree:
    olds = []
    for l in pathlib.Path(a.old_tree).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*\*\s+([\dIVXa-z]+(?:\.\d+)*)\.?\s+(.*?)(?:\s*\[\[.*\]\])?\s*$", l)
        if m: olds.append((m.group(1), re.sub(r"[།\s]+$", "", m.group(2))))
    news = [(".".join(h["path"]), re.sub(r"[།\s]+$", "", h["title"])) for h in heads if h["path"]]
    od, nd = dict(olds), dict(news)
    for k in od:
        if k not in nd: old_diff.append(f"in old tree only: {k} {od[k][:50]}")
        elif od[k] != nd[k]: old_diff.append(f"title differs {k}: old '{od[k][:45]}' / file '{nd[k][:45]}'")
    for k in nd:
        if k not in od: old_diff.append(f"in file only: {k} {nd[k][:50]}")

rep = [f"# TOC structure check — {pathlib.Path(a.file).name}", "",
       f"headings: {len(heads)}; max depth: {max(h['level'] for h in heads)}; "
       f"top-level ##: {sum(1 for h in heads if h['level']==2)}", ""]
total = sum(len(v) for v in issues.values())
rep.append(f"**issues: {total}**"); rep.append("")
for k, v in issues.items():
    rep.append(f"## {k} ({len(v)})"); rep += [f"- {x}" for x in v]; rep.append("")
if a.old_tree:
    rep.append(f"## vs. earlier tree `{a.old_tree}` ({len(old_diff)} differences)")
    rep += [f"- {x}" for x in old_diff]
pathlib.Path(out, "structure.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
print("\n".join(rep[:6]))
for k, v in issues.items(): print(f"  {k}: {len(v)}")
print(f"  vs old tree: {len(old_diff)} differences")
