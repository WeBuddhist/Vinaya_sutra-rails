import sys
sys.stdout.reconfigure(encoding="utf-8")
L=open('source.md',encoding='utf-8').read().replace('\r\n','\n').split('\n')
ln=int(sys.argv[1]); pat=sys.argv[2]
t=L[ln-1]; i=t.find(pat)
print(ln, t[max(0,i-250):i+250] if i>=0 else 'NOTFOUND')
