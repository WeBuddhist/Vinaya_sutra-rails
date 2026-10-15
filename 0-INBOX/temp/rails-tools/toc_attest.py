"""Is each heading's title attested in the text of its own section?

usage: toc_attest.py FILE QC_TREE_REPORT OUT
"""
import re, sys, pathlib, collections

f, qcrep, outp = sys.argv[1:4]
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")
ORD = ["བཅུ་བཞི་པ", "བཅུ་གསུམ་པ", "བཅུ་གཉིས་པ", "བཅུ་གཅིག་པ", "དང་པོ", "གཉིས་པ", "གསུམ་པ", "བཞི་པ",
       "ལྔ་པ", "དྲུག་པ", "བདུན་པ", "བརྒྱད་པ", "དགུ་པ", "བཅུ་པ"]


def canon(s):
    s = re.sub(r"\*\*|[\s།༎༄༅༑༔]", "", s)
    s = s.replace("༌", "་").strip("་")
    for w in ("ནི", "ལ", "འོ", "དོ", "པོ"):
        if s.endswith("་" + w): s = s[: -len(w) - 1]
    return s


def strip_ord(t):
    for w in ORD:
        if t.startswith(w + "་"): return t[len(w) + 1:], w
    return t, None


raw = pathlib.Path(f).read_text(encoding="utf-8").replace("\r\n", "\n")
raw = re.sub(r"\A---\n.*?\n---\n", "", raw, flags=re.S)
lines = raw.split("\n")
heads = [(i, len(m.group(1)), re.sub(r"\*\*", "", m.group(2)).strip(), m.group(3))
         for i, l in enumerate(lines) if (m := H.match(l))]
canon_lines = [canon(l) if not H.match(l) else "" for l in lines]
whole = "".join(canon_lines)

res = collections.Counter(); bad = []
for k, (i, lvl, title, hid) in enumerate(heads):
    if hid in ("0",): continue
    t, ordw = strip_ord(canon(title))
    if len(t) < 3:
        res["bare / too short to check"] += 1; continue
    # first content block after this heading (skipping nested headings)
    j = i + 1
    while j < len(lines) and (not lines[j].strip() or H.match(lines[j])): j += 1
    first = "".join(canon_lines[j:j + 4])
    # own section span: until next heading of same or higher level
    end = next((h[0] for h in heads[k + 1:] if h[1] <= lvl), len(lines))
    span = "".join(canon_lines[i:end])
    # the parent's own text (its announcement)
    par_i = next((h[0] for h in reversed(heads[:k]) if h[1] < lvl), 0)
    par_first = "".join(canon_lines[par_i:i])
    if t in first:
        res["in its own opening text"] += 1
    elif t in span:
        res["inside its own section (not at the start)"] += 1
    elif t in par_first:
        res["only in the parent's announcement"] += 1
    elif t in whole:
        res["only elsewhere in the file"] += 1; bad.append(("elsewhere", i + 1, hid, title))
    else:
        res["not found in the text"] += 1; bad.append(("missing", i + 1, hid, title))

# the 25 'ordinal not attested in corpus' titles: does the SOURCE carry ordinal+title?
ordchk = []
for l in pathlib.Path(qcrep).read_text(encoding="utf-8").splitlines():
    m = re.search(r"ordinal (\d+) \((\S+)\) not attested.*->\s+([\d.]+)\s+(.*)$", l)
    if not m: continue
    num, ow, dec, title = m.groups()
    t = canon(title)
    ordchk.append((dec, title, "source has it" if t in whole else "NOT in source"))

out = ["# Heading-title attestation in the source", ""]
out += [f"- {k}: {v}" for k, v in res.most_common()]
out += ["", "## Titles found only elsewhere / not found", ""]
out += [f"- {kind}: L{ln} ^{hid} {title}" for kind, ln, hid, title in bad]
out += ["", "## qc_check_tree 'ordinal not attested in corpus' — checked against the source", ""]
out += [f"- {d} {t}: {r}" for d, t, r in ordchk]
pathlib.Path(outp).write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out[:12])); print(f"bad: {len(bad)}")
print(collections.Counter(r for _, _, r in ordchk))
