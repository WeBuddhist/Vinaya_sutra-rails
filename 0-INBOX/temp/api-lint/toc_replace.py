#!/usr/bin/env python3
"""Replace a commentary's live table of contents with the freshly parsed one (dry run by default).

    python 0-INBOX/temp/api-lint/toc_replace.py <stem>
    python 0-INBOX/temp/api-lint/toc_replace.py <stem> --execute --confirm <stem>

<stem> = the commentary file name without .md (1-SOURCES/Commentaries/<stem>.md); the payload is
4-SYSTEM/scripts/parser-commentary/output/<stem>/<stem>.toc.json (run the linter + parser first).

Dry run: reads the old toc (GET /v2/table-of-contents/{toc_id}), checks it belongs to the file's
edition, and compares it node by node (title, span) with the payload. Execute:
    1. DELETE /v2/table-of-contents/{old toc_id}
    2. POST   /v2/editions/{edition_id}/table-of-contents  <- toc.json  -> new toc_id
    3. writes the new toc_id into the frontmatter and the ledger (old id kept under "replaced_tocs")
    4. GET the new toc and checks it equals the payload node by node.
Text, edition, durchens and alignment are not touched (headings are not edition content).
"""
import argparse, datetime as _dt, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_upload_batch as ub  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
VAULT = HERE.parents[2]
LEDGER = HERE / "commentary-upload-status.json"


def flatten(sections, depth=0, out=None):
    out = [] if out is None else out
    for s in sections:
        out.append((depth, s["title"].get("bo", ""), s["span"]["start"], s["span"]["end"]))
        flatten(s.get("subsections", []), depth + 1, out)
    return out


ap = argparse.ArgumentParser()
ap.add_argument("stem"); ap.add_argument("--execute", action="store_true"); ap.add_argument("--confirm", default="")
a = ap.parse_args()
if a.execute and a.confirm != a.stem:
    ap.error(f"--execute needs --confirm {a.stem}")

src = VAULT / "1-SOURCES" / "Commentaries" / f"{a.stem}.md"
ids = ub.read_fm_ids(src)
eid, old = ids.get("edition_id"), ids.get("toc_id")
assert eid and old, "frontmatter needs edition_id and toc_id"
payload = json.loads((VAULT / "4-SYSTEM/scripts/parser-commentary/output" / a.stem / f"{a.stem}.toc.json").read_text(encoding="utf-8"))
new_flat = flatten(payload["sections"])

live = ub.call("GET", f"/v2/table-of-contents/{old}")
assert live["edition_id"] == eid, f"live toc {old} belongs to edition {live['edition_id']}, not {eid}"
old_flat = flatten(live["sections"])
same_shape = [(d, s, e) for d, _, s, e in old_flat] == [(d, s, e) for d, _, s, e in new_flat]
titles = sum(1 for x, y in zip(old_flat, new_flat) if x[1] != y[1])
print(f"== {'EXECUTE' if a.execute else 'DRY RUN'}: {a.stem[:60]}")
print(f"  edition {eid} | live toc {old}: {len(old_flat)} nodes | payload: {len(new_flat)} nodes | same tree shape & spans: {same_shape} | titles that differ: {titles}")
if not a.execute:
    print("  plan: DELETE /v2/table-of-contents/%s ; POST /v2/editions/%s/table-of-contents <- toc.json ; nothing sent." % (old, eid))
    sys.exit(0)

ub.call("DELETE", f"/v2/table-of-contents/{old}")
new_id = ub.call("POST", f"/v2/editions/{eid}/table-of-contents", payload)["id"]
ub.patch_fm(src, "toc_id", new_id)
ledger = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {}
entry = ledger.setdefault(a.stem, {})
entry.setdefault("replaced_tocs", []).append({"toc_id": old, "replaced_at": _dt.datetime.now().isoformat(timespec="seconds")})
entry["toc_id"] = new_id
entry.setdefault("log", []).append({"step": "toc-replace", "ts": _dt.datetime.now().isoformat(timespec="seconds"), "old": old, "new": new_id})
entry["updated"] = _dt.datetime.now().isoformat(timespec="seconds")
LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
back = flatten(ub.call("GET", f"/v2/table-of-contents/{new_id}")["sections"])
print(f"  deleted toc {old}; new toc {new_id}; read back {len(back)} nodes, identical to payload: {back == new_flat}")
