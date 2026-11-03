import sys,re
sys.stdout.reconfigure(encoding="utf-8")
L=open('source.md',encoding='utf-8').read().replace('\r\n','\n').split('\n')
rows=[]
for f in ['rows1','rows2','rows3','rows4']:
    for l in open(f'work/P7/{f}.tsv',encoding='utf-8'):
        l=l.rstrip('\n')
        if not l.strip(): continue
        p=l.split('\t'); assert len(p)==4,l
        rows.append(p)
def head(n):
    for i in range(n-2,-1,-1):
        if L[i].startswith('#'):
            m=re.search(r'\^([\w-]+)\s*$',L[i]); return m.group(1) if m else ''
    return ''
def key(r):
    a=r[1].split('-'); return (int(r[0]),int(a[0]),int(a[1]))
rows.sort(key=key)
with open('place-P7.tsv','w',encoding='utf-8',newline='\n') as o:
    o.write('heading\troot_block\tline\tkind\twords\n')
    for ln,rb,k,w in rows:
        o.write(f"{head(int(ln))}\t{rb}\t{ln}\t{k}\t{w}\n")
print(len(rows))
