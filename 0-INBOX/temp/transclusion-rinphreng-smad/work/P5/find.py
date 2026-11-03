import sys, re, pathlib
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(r"D:/Work/OpenPecha/Vinaya_sutra-rails/1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md")
def norm(s):
    s = s.replace("༌", "་")
    s = re.sub(r"[།༎\s༔]+", "་", s)
    s = re.sub(r"་+", "་", s)
    return s.strip("་")
blocks = []
for l in ROOT.read_text(encoding="utf-8").split("\n"):
    m = re.search(r"\^([\w-]+)\s*$", l)
    if m: blocks.append((m.group(1), norm(re.sub(r"\^[\w-]+\s*$", "", l))))
for q in sys.argv[1:]:
    n = norm(q)
    hits = [(i, t) for i, t in blocks if n in t]
    print(f"== {q}: {len(hits)}")
    for i, t in hits[:12]:
        k = t.find(n)
        print(f"  {i}: …{t[max(0,k-40):k+len(n)+40]}…")
