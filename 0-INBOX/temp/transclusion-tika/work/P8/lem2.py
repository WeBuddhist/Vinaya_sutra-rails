import sys; sys.stdout.reconfigure(encoding="utf-8")
import re, pathlib, collections
V = pathlib.Path(r"D:\Work\OpenPecha\Vinaya_sutra-rails")
SRC = V/"0-INBOX/temp/transclusion-tika/source.md"
ROOT = V/"1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md"
L = SRC.read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
def syl(s):
    s = re.sub(r"\^[\w-]+\s*$","",s)
    s = re.sub(r"[།༄༅༎༑\s]+","་",s)
    return [x for x in s.split("་") if x]
rb = {}
for l in ROOT.read_text(encoding="utf-8").split("\n"):
    m = re.search(r"\^(9-\d+)\s*$", l)
    if m and not l.startswith("#"): rb[int(m.group(1)[2:])] = syl(l)
def lcs(a,b):
    best=0; bi=0
    prev=[0]*(len(b)+1)
    for i in range(1,len(a)+1):
        cur=[0]*(len(b)+1)
        for j in range(1,len(b)+1):
            if a[i-1]==b[j-1]:
                cur[j]=prev[j-1]+1
                if cur[j]>best: best=cur[j]
        prev=cur
    return best
STOP = {"ཉེས་བྱས་སོ","ལྟུང་བ་མེད་དོ","ཉེས་པ་མེད་དོ","མ་ཡིན་ནོ","དངོས་གཞིའོ","ཡིན་ནོ"}
start, end, p = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
pat = re.compile(r"([^།]*?)\s*ཞེས་(?:བྱ་བ|པ|བྱའོ|སོ|གསུངས|སྨོས|བཤད)")
for i in range(start-1, end):
    l = L[i]
    if not l.strip() or l.startswith("#"): continue
    if i>0 and L[i-1].strip() and not L[i-1].startswith("#"): continue
    bid = re.search(r"\^([\w-]+)\s*$", l); bid = bid.group(1) if bid else "?"
    print(f"=== {i+1} {bid}  (ptr 9-{p}) {l[:70]}")
    for m in pat.finditer(l):
        lem = m.group(1).strip()
        if "ཞེ་ན" in lem or "དེའི་ཕྱིར" in lem: lem = re.split(r"དེའི་ཕྱིར[།\s]*|ཞེ་ན[།\s]*", lem)[-1]
        s = syl(lem)
        if len(s)<2: continue
        sc = sorted(((lcs(s,rb[k]),k) for k in range(max(1,p-3), p+4) if k in rb), reverse=True)
        b, k = sc[0]
        mark = "" 
        if b>=3 and (b>=len(s)*0.6 or b>=5):
            mark = f"9-{k}:{b}/{len(s)}"
            if sc[1][0]==b: mark += f" (tie 9-{sc[1][1]})"
            elif "་".join(s) not in STOP and b>=max(4,0.6*len(s)): p = max(p,k)
        print(f"  [{mark or '-'}] {lem[:90]}")
