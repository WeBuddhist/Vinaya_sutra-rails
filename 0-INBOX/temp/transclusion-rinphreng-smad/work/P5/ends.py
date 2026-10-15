import sys, re, pathlib
sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(r"D:/Work/OpenPecha/Vinaya_sutra-rails/1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md")
B = {}
for l in ROOT.read_text(encoding="utf-8").split("\n"):
    m = re.search(r"\^([\w-]+)\s*$", l)
    if m: B[m.group(1)] = re.sub(r"\s*\^[\w-]+\s*$", "", l)
ch, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
n = int(sys.argv[4]) if len(sys.argv) > 4 else 70
for i in range(a, b + 1):
    t = B.get(f"{ch}-{i}", "")
    print(f"{ch}-{i}: {t[:n]} ⟶ … {t[-n:]}")
