"""Make heading ordinals consistent among siblings.

usage: python -I fix_sibling_ordinals.py FILE.md [--write]

Rule (user, 2026-10-15): if ANY heading in a group of siblings (same parent ID path) starts with a
Tibetan ordinal (དང་པོ / གཉིས་པ / …), ALL of them must; a heading without one gets the ordinal of the
last segment of its own ID. Groups where no heading has an ordinal are left alone. Only heading
lines change; **bold** on deep headings is kept. Without --write it only reports.
"""
import re, sys, collections

sys.stdout.reconfigure(encoding="utf-8")
ORD = ["དང་པོ", "གཉིས་པ", "གསུམ་པ", "བཞི་པ", "ལྔ་པ", "དྲུག་པ", "བདུན་པ", "བརྒྱད་པ", "དགུ་པ", "བཅུ་པ",
       "བཅུ་གཅིག་པ", "བཅུ་གཉིས་པ", "བཅུ་གསུམ་པ", "བཅུ་བཞི་པ", "བཅོ་ལྔ་པ", "བཅུ་དྲུག་པ", "བཅུ་བདུན་པ",
       "བཅོ་བརྒྱད་པ", "བཅུ་དགུ་པ", "ཉི་ཤུ་པ", "ཉེར་གཅིག་པ", "ཉེར་གཉིས་པ", "ཉེར་གསུམ་པ", "ཉེར་བཞི་པ", "ཉེར་ལྔ་པ"]
H = re.compile(r"^(#+ )(\*\*)?(.*?)(\*\*)?( \^([\w-]+))\s*$")


def ordinal(t):
    for w in sorted(ORD, key=len, reverse=True):
        if t.startswith(w + "་") or t == w or t.startswith(w + "།"):
            return w


path = sys.argv[1]
raw = open(path, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw[:3000] else "\n"
L = raw.split(nl)
sib = collections.defaultdict(list)
for i, l in enumerate(L):
    m = H.match(l)
    if not m:
        continue
    segs = m.group(6).split("-")[:-1]
    if not segs or not segs[-1].isdigit():
        continue
    sib[tuple(segs[:-1])].append((i, int(segs[-1]), m))

changed, groups = [], 0
for _, s in sib.items():
    has = [ordinal(m.group(3)) for _, _, m in s]
    if any(has) and not all(has):
        groups += 1
        for (i, n, m), h in zip(s, has):
            if h:
                continue
            if n > len(ORD):
                print(f"  SKIP L{i+1}: no ordinal word for {n}"); continue
            L[i] = m.group(1) + (m.group(2) or "") + ORD[n - 1] + "་" + m.group(3) + (m.group(4) or "") + m.group(5)
            changed.append(i + 1)
print(f"{path.split('/')[-1]}: mixed sibling groups {groups}, headings given an ordinal {len(changed)}")
if "--write" in sys.argv:
    open(path, "w", encoding="utf-8", newline="").write(nl.join(L))
