"""Fill pass-1 and pass-2 chunk files in parallel using extract_toc_tree's own functions.
The main script later skips every chunk whose file exists, then merges / builds / QCs."""
import sys, importlib.util, threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
vault = Path(sys.argv[1]); src = Path(sys.argv[2]); cid = sys.argv[3]; workers = int(sys.argv[4])
spec = importlib.util.spec_from_file_location("ett", vault/"4-SYSTEM/Skills/seg-toc-lib/toc_tree_extractor/extract_toc_tree.py")
ett = importlib.util.module_from_spec(spec); spec.loader.exec_module(ett)
lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
chunks = ett.make_chunks(lines, 50, 10)
base = vault/"0-INBOX/temp"/f"TOC-{cid}"; cdir = base/"candidates"; edir = base/"enumerations"
cdir.mkdir(parents=True, exist_ok=True); edir.mkdir(parents=True, exist_ok=True)
client = ett.get_client(); model = ett.DEFAULT_MODEL; fb = ett.DEFAULT_FALLBACK_MODEL
lock = threading.Lock()
def job(kind, idx, start, end, text, numbered):
    if kind == "c":
        out = cdir/f"chunk_{idx:03d}.md"
        if out.exists(): return kind, idx, "skip"
        r = ett.extract_from_chunk(client, model, numbered, fallback_model=fb)
        head = f"<!-- chunk {idx:03d} | lines {start}–{end} | source: {cid} -->\n\n"
        body = "<!-- no candidates -->\n" if (not r or r.strip().upper()=="NO CANDIDATES") else r.rstrip()+"\n"
        out.write_text(head+body, encoding="utf-8")
    else:
        out = edir/f"chunk_{idx:03d}.md"
        if out.exists(): return kind, idx, "skip"
        r = ett.extract_enumerations_from_chunk(client, model, text, fallback_model=fb)
        out.write_text("NO ENUMERATIONS\n" if (not r or r.strip().upper()=="NO ENUMERATIONS") else r.rstrip()+"\n", encoding="utf-8")
    return kind, idx, "ok"
tasks = [(k,)+c for k in ("c","e") for c in chunks]
if len(sys.argv) > 5 and sys.argv[5] == "reverse": tasks.reverse()
done = fail = 0
with ThreadPoolExecutor(workers) as ex:
    futs = {ex.submit(job, *t): t for t in tasks}
    for f in as_completed(futs):
        t = futs[f]
        try: f.result(); done += 1
        except Exception as e:
            fail += 1; print(f"FAIL {t[0]} chunk_{t[1]:03d}: {type(e).__name__}: {str(e)[:120]}", flush=True)
        if (done+fail) % 10 == 0: print(f"progress {done+fail}/{len(tasks)} (fail {fail})", flush=True)
print(f"prefill done: ok={done} fail={fail} of {len(tasks)}", flush=True)
