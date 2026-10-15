import csv,sys,re
sys.stdout.reconfigure(encoding="utf-8")
P={(r['line'],r['root_block']) for r in csv.DictReader(open('place-P7.tsv',encoding='utf-8'),delimiter='\t')}
S={(r['line'],r['root_block']) for r in csv.DictReader(open('seeds/seeds-P7.tsv',encoding='utf-8'),delimiter='\t')}
print('seeds',len(S),'kept',len(S&P),'dropped',len(S-P),'added',len(P-S))
d=S-P
print('dropped ch9',sum(1 for x in d if x[1].startswith('9-')),'other ch',sum(1 for x in d if not x[1].startswith('9-')))
for r in csv.DictReader(open('place-P7.tsv',encoding='utf-8'),delimiter='\t'):
    n=len([s for s in re.split(r'[་།\s…]+',r['words']) if s])
    if n>25: print('long',r['line'],r['root_block'],n)
print(sorted({r[1] for r in P}, key=lambda x:int(x.split('-')[1]))[:3], len({r[1] for r in P}))
