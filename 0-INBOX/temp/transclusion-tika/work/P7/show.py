import sys, csv
sys.stdout.reconfigure(encoding="utf-8")
a,b=int(sys.argv[1]),int(sys.argv[2])
L=open('source.md',encoding='utf-8').read().replace('\r\n','\n').split('\n')
S={}
for r in csv.DictReader(open('seeds/seeds-P7.tsv',encoding='utf-8'),delimiter='\t'):
    S.setdefault(int(r['line']),[]).append(r)
for i in range(a-1,b):
    l=L[i]
    if not l.strip(): continue
    print(f"{i+1}: {l}")
    for r in S.get(i+1,[]):
        print(f"   >> {r['root_block']} m{r['matched_syllables']} also[{r['same_words_also_match']}] {r['preview']}")
