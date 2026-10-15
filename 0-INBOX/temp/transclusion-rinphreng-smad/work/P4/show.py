import csv,sys
sys.stdout.reconfigure(encoding="utf-8")
a,b=int(sys.argv[1]),int(sys.argv[2])
L=open('source.md',encoding='utf-8').read().split('\n')
S={}
for r in csv.DictReader(open('seeds/seeds-P4.tsv',encoding='utf-8'),delimiter='\t'):
    S.setdefault(int(r['line']),[]).append(r)
for i in range(a,b+1):
    l=L[i-1]
    if not l.strip(): continue
    print(f"{i}: {l}")
    for r in S.get(i,[]):
        print(f"   >> {r['root_block']} m{r['matched_syllables']} also[{r['same_words_also_match']}] {r['preview']}")
