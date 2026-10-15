import sys,re; sys.stdout.reconfigure(encoding="utf-8")
R=open(r"D:\Work\OpenPecha\Vinaya_sutra-rails\1-SOURCES\Text\འདུལ་བ་མདོ་རྩ་བ།.md",encoding="utf-8").read().split("\n")
def n(s): return re.sub(r"[།\s་]+","",s)
for q in sys.argv[1:]:
    for l in R:
        m=re.search(r"\^([\w-]+)\s*$",l)
        if m and n(q) in n(l):
            i=l.find(q[:6]); print(q[:20],"->",m.group(1), "|", l[max(0,i-60):i+120].replace("\n",""))
