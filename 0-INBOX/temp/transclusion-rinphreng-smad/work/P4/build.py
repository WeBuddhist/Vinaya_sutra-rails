import csv,re,sys
sys.stdout.reconfigure(encoding="utf-8")
L=open('source.md',encoding='utf-8').read().split('\n')
def heading(ln):
    for i in range(ln-1,-1,-1):
        if L[i].startswith('#'):
            m=re.search(r'\^([\w-]+)\s*$',L[i]); return m.group(1)
def syl(t): return len([x for x in re.split(r'[་།…\s]+',t) if x])
def trim(w,cap=25):
    if syl(w)<=cap: return w
    segs=[x for x in w.split('…')]
    out=[];tot=0
    for sg in segs:
        k=syl(sg)
        if tot+k<=cap: out.append(sg); tot+=k
        else: break
    if not out:
        out=['་'.join([x for x in re.split(r'་',segs[0]) if x][:cap])]
    return '…'.join(out)
rows=[]
for r in csv.reader(open('work/P4/rows.tsv',encoding='utf-8'),delimiter='\t'):
    rb,ln,kind,words=r
    rows.append((int(ln),rb,kind,words))
def key(rb): return tuple(int(x) for x in rb.split('-'))
rows.sort(key=lambda x:(x[0],key(x[1])))
with open('place-P4.tsv','w',encoding='utf-8',newline='') as f:
    f.write('heading\troot_block\tline\tkind\twords\n')
    for ln,rb,kind,words in rows:
        words=trim(words)
        n=len([s for s in re.split(r'[་།…\s]+',words) if s])
        if n>25: print('LONG',ln,rb,n)
        f.write(f'{heading(ln)}\t{rb}\t{ln}\t{kind}\t{words}\n')
# seed stats
S=list(csv.DictReader(open('seeds/seeds-P4.tsv',encoding='utf-8'),delimiter='\t'))
mine={(r[0],r[1]) for r in rows}
kept=sum(1 for s in S if (int(s['line']),s['root_block']) in mine)
print('seeds',len(S),'kept',kept,'dropped',len(S)-kept)
seedkeys={(int(s['line']),s['root_block']) for s in S}
print('added beyond seeds',sum(1 for r in rows if (r[0],r[1]) not in seedkeys))
from collections import Counter
print(Counter(r[2] for r in rows))
print(sorted(Counter(r[1].split('-')[0] for r in rows).items()))
