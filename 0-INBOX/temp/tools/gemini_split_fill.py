"""Fill chunk files that keep hitting max_output_tokens by splitting the chunk into smaller line parts."""
import sys, importlib.util
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
vault = Path(sys.argv[1]); src = Path(sys.argv[2]); cid = sys.argv[3]; nparts = int(sys.argv[4])
todo = [(a[0], int(a[1:])) for a in sys.argv[5:]]          # e.g. c74 c76 c125 e123
spec = importlib.util.spec_from_file_location("ett", vault/"4-SYSTEM/Skills/seg-toc-lib/toc_tree_extractor/extract_toc_tree.py")
ett = importlib.util.module_from_spec(spec); spec.loader.exec_module(ett)
lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
chunks = {c[0]: c for c in ett.make_chunks(lines, 50, 10)}
base = vault/"0-INBOX/temp"/f"TOC-{cid}"
client = ett.get_client(); model = ett.DEFAULT_MODEL; fb = ett.DEFAULT_FALLBACK_MODEL
def parts(s, n):
    ls = s.splitlines(keepends=True); k = -(-len(ls)//n)
    return ["".join(ls[i:i+k]) for i in range(0, len(ls), k)]
def run(kind, idx):
    _, start, end, text, numbered = chunks[idx]
    if kind == "c":
        out = base/"candidates"/f"chunk_{idx:03d}.md"
        if out.exists(): return f"{kind}{idx} exists"
        rs = list(ex.map(lambda p: ett.extract_from_chunk(client, model, p, fallback_model=fb), parts(numbered, nparts)))
        rs = [r.rstrip() for r in rs if r and r.strip().upper() != "NO CANDIDATES"]
        head = f"<!-- chunk {idx:03d} | lines {start}–{end} | source: {cid} -->\n\n"
        out.write_text(head + ("\n\n".join(rs) + "\n" if rs else "<!-- no candidates -->\n"), encoding="utf-8")
    else:
        out = base/"enumerations"/f"chunk_{idx:03d}.md"
        if out.exists(): return f"{kind}{idx} exists"
        rs = list(ex.map(lambda p: ett.extract_enumerations_from_chunk(client, model, p, fallback_model=fb), parts(text, nparts)))
        rs = [r.rstrip() for r in rs if r and r.strip().upper() != "NO ENUMERATIONS"]
        out.write_text("\n\n".join(rs) + "\n" if rs else "NO ENUMERATIONS\n", encoding="utf-8")
    return f"{kind}{idx} written"
ex = ThreadPoolExecutor(12)
with ThreadPoolExecutor(len(todo)) as outer:
    for r in outer.map(lambda t: run(*t), todo): print(r, flush=True)
print("split fill done", flush=True)
