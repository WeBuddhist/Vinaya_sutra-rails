import sys, re, csv
sys.stdout.reconfigure(encoding="utf-8")
a,b=int(sys.argv[1]),int(sys.argv[2])
L=open('source.md',encoding='utf-8').read().replace('\r\n','\n').split('\n')
R=open('../../../1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md',encoding='utf-8').read()
def syl(t):
    t=re.sub(r'\^[\w-]+\s*$','',t)
    t=re.sub(r'[།༄༅༎༑༈\s]+','་',t)
    return [s for s in t.split('་') if s]
roots=[]
for m in re.finditer(r'^(.*?)\^([\w-]+)\s*$',R,re.M):
    roots.append((m.group(2),'་'+'་'.join(syl(m.group(1)))+'་'))
def find(seq):
    s='་'+'་'.join(seq)+'་'
    return [rid for rid,t in roots if s in t]
S={}
for r in csv.DictReader(open('seeds/seeds-P7.tsv',encoding='utf-8'),delimiter='\t'):
    S.setdefault(int(r['line']),[]).append(r['root_block']+':'+r['matched_syllables'])
starts=[i for i in range(a-1,b) if L[i].strip() and not L[i].startswith('#') and (i==0 or not L[i-1].strip() or L[i-1].startswith('#'))]
head=''
for i in range(0,a-1):
    if L[i].startswith('#'): head=L[i]
for i in range(a-1,b):
    if L[i].startswith('#'): print('HEAD',i+1,L[i][:120]); continue
    if i not in starts: continue
    j=i; txt=[]
    while j<len(L) and L[j].strip() and not L[j].startswith('#'): txt.append(L[j]); j+=1
    t=' '.join(txt); bid=re.search(r'\^([\w-]+)\s*$',t); bid=bid.group(1) if bid else '?'
    sy=syl(t)
    out=[]
    for k,s in enumerate(sy):
        if s in ('ཞེས','ཅེས','ཤེས') and k>0:
            best=None
            for n in range(2,min(30,k)+1):
                seq=sy[k-n:k]
                # strip trailing 'ཞེས' variants handled; try also last syllable with 'འོ' merged
                f=find(seq)
                if f: best=(n,seq,f)
                else: break
            if best and best[0]>=2:
                n,seq,f=best
                c9=[x for x in f if x.startswith('9-')]
                out.append(f"{n}:{'་'.join(seq)}=>{','.join(c9[:6]) if c9 else ','.join(f[:4])}{'' if c9 else ' (nonch9)'}{' +'+str(len(f)) if len(f)>1 else ''}")
    mk=[m for m in ['འདི་ཉིད་ལས','རྩ་བ་ལས','མདོ་ལས','ལུང་','འགྲེལ་པ','རང་གི་རྣམ་པར་བཤད','སློབ་དཔོན','མཛོད','ཞུ་བ','གཞི་','ཕྲན་ཚེགས','འོག་ནས','སྔར'] if m in t]
    print(f"{i+1} ^{bid} len{len(sy)} seeds[{' '.join(S.get(i+1,[]))}] mk[{','.join(mk)}]")
    for o in out: print('    ',o)
