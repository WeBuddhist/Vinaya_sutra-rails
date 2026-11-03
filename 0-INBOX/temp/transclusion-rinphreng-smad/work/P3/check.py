import csv,re,sys
L=open('source.md',encoding='utf-8').read().replace('\r\n','\n').split('\n')
rows=list(csv.DictReader(open('place-P3.tsv',encoding='utf-8'),delimiter='\t'))
bad=0
for r in rows:
    i=int(r['line'])-1
    while not L[i].startswith('#'): i-=1
    h=re.search(r'\^([\w-]+)\s*$',L[i]).group(1)
    if h!=r['heading']: print('heading',r['line'],r['heading'],'->',h); bad+=1
seeds={(s['line'],s['root_block']) for s in csv.DictReader(open('seeds/seeds-P3.tsv',encoding='utf-8'),delimiter='\t')}
placed={(r['line'],r['root_block']) for r in rows}
print('bad headings',bad,'seeds',len(seeds),'kept',len(seeds&placed),'dropped',len(seeds-placed),'added',len(placed-seeds))
print(sorted(set(r['root_block'].split('-')[0] for r in rows)))
print('added:',sorted(placed-seeds,key=lambda x:int(x[0])))
