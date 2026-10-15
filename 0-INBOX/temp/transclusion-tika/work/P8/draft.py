import sys; sys.stdout.reconfigure(encoding="utf-8")
import re
exec(open(__file__.replace("draft.py","lem2.py"),encoding="utf-8").read().split("start, end, p =")[0])
start,end,p = 4500,5063,110
pat = re.compile(r"([^།]*?)\s*ཞེས་(?:བྱ་བ|པ|བྱའོ|སོ|གསུངས|སྨོས|བཤད)")
out=[]
for i in range(start-1,end):
    l=L[i]
    if not l.strip() or l.startswith("#"): continue
    if i>0 and L[i-1].strip() and not L[i-1].startswith("#"): continue
    got={}
    for m in pat.finditer(l):
        lem=m.group(1).strip()
        if "ཞེ་ན" in lem or "དེའི་ཕྱིར" in lem: lem=re.split(r"དེའི་ཕྱིར[།\s]*|ཞེ་ན[།\s]*",lem)[-1]
        if re.match(r"(འདིར་|དེ་ལྟར་ཡང་འདིར་)?(གཞུང་|ཁུངས་)",lem): continue
        s=syl(lem)
        if len(s)<2: continue
        sc=sorted(((lcs(s,rb[k]),k) for k in range(max(1,p-3),p+4) if k in rb),reverse=True)
        b,k=sc[0]
        if "་".join(s) in STOP: continue
        if b>=3 and b>=0.5*len(s) and sc[1][0]<b:
            got.setdefault(k,[]).append("་".join(s[:25]))
            if b>=max(4,0.6*len(s)): p=max(p,k)
    for k,ws in got.items():
        out.append(f"9-0\t9-{k}\t{i+1}\tlemma\t{' … '.join(ws)[:200]}")
print("heading\troot_block\tline\tkind\twords")
print("\n".join(out))
