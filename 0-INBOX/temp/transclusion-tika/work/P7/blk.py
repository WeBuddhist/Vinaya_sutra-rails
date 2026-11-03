import sys
sys.stdout.reconfigure(encoding="utf-8")
L=open('source.md',encoding='utf-8').read().replace('\r\n','\n').split('\n')
for x in sys.argv[1:]:
    i=int(x)-1; print(f"--{x}: {L[i]}")
