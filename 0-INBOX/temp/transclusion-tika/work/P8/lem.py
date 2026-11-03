import re, sys, pathlib, collections
import sys; sys.stdout.reconfigure(encoding="utf-8")
V = pathlib.Path(r"D:\Work\OpenPecha\Vinaya_sutra-rails")
SRC = V/"0-INBOX/temp/transclusion-tika/source.md"
ROOT = V/"1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md"
L = SRC.read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
def syl(s):
    s = re.sub(r"\^[\w-]+\s*$","",s)
    s = re.sub(r"[།༄༅༎༑\s]+","་",s)
    return [x for x in s.split("་") if x]
# root blocks
rb = {}
for l in ROOT.read_text(encoding="utf-8").split("\n"):
    m = re.search(r"\^([\w-]+)\s*$", l)
    if m and not l.startswith("#"): rb[m.group(1)] = syl(l)
def norm(x):  # normalise final particle variations
    return x
ridx = collections.defaultdict(set)
for k,v in rb.items():
    for i in range(len(v)-2):
        ridx[tuple(v[i:i+3])].add(k)
def find(lem):
    s = syl(lem)
    if len(s) < 2: return []
    # try full, then drop last syllable (case endings) 
    res=[]
    for cut in (0,1):
        t = s[:len(s)-cut] if cut else s
        if len(t)<2: break
        n=len(t)
        for k,v in rb.items():
            for i in range(len(v)-n+1):
                if v[i:i+n]==t: res.append(k); break
        if res: return [(r,cut) for r in res]
    return []
start, end = int(sys.argv[1]), int(sys.argv[2])
pat = re.compile(r"([^།]*?)\s*ཞེས་(?:བྱ་བ|པ|བྱའོ|སོ|གསུངས|སྨོས|བཤད)")
for i in range(start-1, end):
    l = L[i]
    if not l.strip() or l.startswith("#"): continue
    if i>0 and L[i-1].strip() and not L[i-1].startswith("#"): continue
    bid = re.search(r"\^([\w-]+)\s*$", l); bid = bid.group(1) if bid else "?"
    print(f"=== {i+1} {bid}")
    for m in pat.finditer(l):
        lem = m.group(1).strip()
        lem = re.sub(r"^.*?(དེའི་ཕྱིར|ཞེ་ན)[།\s]*","",lem) if "དེའི་ཕྱིར" in lem else lem
        hits = find(lem)
        ch9 = [h for h,c in hits if h.startswith("9-")]
        other = [h for h,c in hits if not h.startswith("9-")]
        tag = ",".join(ch9) if ch9 else ("other:"+",".join(other[:4]) if other else "-")
        print(f"  [{tag}] {lem[:80]}")
