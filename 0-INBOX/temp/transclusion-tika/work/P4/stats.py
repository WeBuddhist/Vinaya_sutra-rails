import csv, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
H = pathlib.Path(__file__).resolve().parents[2]
seeds = list(csv.DictReader(open(H/'seeds/seeds-P4.tsv', encoding='utf-8'), delimiter='\t'))
rows = list(csv.DictReader(open(H/'place-P4.tsv', encoding='utf-8'), delimiter='\t'))
R = {(int(r['line']), r['root_block']) for r in rows}
S = {(int(s['line']), s['root_block']) for s in seeds}
kept = S & R; dropped = S - R; added = R - S
print('seed pairs', len(S), 'kept', len(kept), 'dropped', len(dropped), 'added', len(added))
from collections import Counter
print('kinds', Counter(r['kind'] for r in rows))
print('chapters', sorted(Counter(r['root_block'].split('-')[0] for r in rows).items()))
rl = {int(r['line']) for r in rows}
print('lines with seeds but no rows:', sorted({int(s['line']) for s in seeds} - rl))
mode = sys.argv[1] if len(sys.argv) > 1 else ''
if mode == 'd7':
    for s in seeds:
        k = (int(s['line']), s['root_block'])
        if k in dropped and s['root_block'].startswith('7-') and int(s['matched_syllables']) >= 7:
            print(s['line'], s['root_block'], s['matched_syllables'], s['preview'][:70])
