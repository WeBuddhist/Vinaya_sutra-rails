import csv,sys
sys.stdout.reconfigure(encoding="utf-8")
P={(r['line'],r['root_block']) for r in csv.DictReader(open('place-P7.tsv',encoding='utf-8'),delimiter='\t')}
for r in csv.DictReader(open('seeds/seeds-P7.tsv',encoding='utf-8'),delimiter='\t'):
    if r['root_block'].startswith('9-') and (r['line'],r['root_block']) not in P and int(r['matched_syllables'])>=8:
        print(r['line'],r['root_block'],r['matched_syllables'],r['preview'][:80])
