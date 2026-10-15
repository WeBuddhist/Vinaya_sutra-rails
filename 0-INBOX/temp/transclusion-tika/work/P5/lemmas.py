import re, sys, csv, pathlib, collections
HERE = pathlib.Path(__file__).resolve().parent
T = HERE.parents[1]
VAULT = T.parents[2]
SRC = (T/"source.md").read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
ROOT = (VAULT/"1-SOURCES"/"Text"/"འདུལ་བ་མདོ་རྩ་བ།.md").read_text(encoding="utf-8")
A, B = 2539, 3420
def syl(s):
    s = re.sub(r"\^[\w-]+\s*$", "", s)
    s = re.sub(r"[༄༅༔་།\s]+", " ", s)
    return [x for x in s.split() if x]
rootb = {}
for l in ROOT.split("\n"):
    m = re.search(r"\^([\w-]+)\s*$", l)
    if m and not l.startswith("#"): rootb[m.group(1)] = syl(l)
ch8 = {k:v for k,v in rootb.items() if k.startswith("8-")}
# index n-grams of 3
idx = collections.defaultdict(set)
for k,v in rootb.items():
    for i in range(len(v)-2): idx[tuple(v[i:i+3])].add(k)
def best_run(q, v):
    # longest common substring length between lists q and v, and whether it ends at end of q (within 3)
    best=(0,0)
    prev=[0]*(len(v)+1)
    for i in range(1,len(q)+1):
        cur=[0]*(len(v)+1)
        for j in range(1,len(v)+1):
            if q[i-1]==v[j-1]:
                cur[j]=prev[j-1]+1
                if cur[j]>best[0]: best=(cur[j],i)
        prev=cur
    return best
blocks=[]
i=A-1
while i < B:
    l=SRC[i]
    if l.strip() and not l.startswith("#") and (i==0 or not SRC[i-1].strip() or SRC[i-1].startswith("#")):
        j=i; txt=[]
        while j<len(SRC) and SRC[j].strip(): txt.append(SRC[j]); j+=1
        blocks.append((i+1," ".join(txt))); i=j
    else: i+=1
out=open(HERE/"lemmas.txt","w",encoding="utf-8")
for ln,txt in blocks:
    bid = re.search(r"\^([\w-]+)\s*$", txt)
    out.write(f"=== {ln} ^{bid.group(1) if bid else '?'} len={len(txt)}\n")
    for m in re.finditer(r"ཞེས|ཞེ་ན", txt):
        pre = txt[max(0,m.start()-160):m.start()]
        q = syl(pre)[-18:]
        if len(q)<2: continue
        res=[]
        for k,v in rootb.items():
            r,end=best_run(q,v)
            if r>=3 and end>=len(q)-3: res.append((r,k))
        res.sort(reverse=True)
        top=[(r,k) for r,k in res if r>=res[0][0]-0] if res else []
        ch8top=[(r,k) for r,k in res if k.startswith("8-")][:3]
        out.write(f"  @{m.start()} …{'་'.join(q[-14:])} || top={top[:4]} ch8={ch8top}\n")
out.close()
print(len(blocks))
