# Rin chen phreng ba (stod) — TOC verification, 2026-10-15

Checked the headings now in `1-SOURCES/Commentaries/…རིན་པོ་ཆེའི་ཕྲེང་བ། སྟོད་ཆ།.md` (1373 headings, after `#` count was expanded to true depth, levels 1–23).

| Check | Result |
|---|---|
| IDs unique, ID path nested under an earlier parent, `#` = depth, no level skip | clean |
| Sibling numbering | 1 gap: under `^3-2-2-1-1-2-2-3-1-2` children go 1–7, 10–14. The text itself jumps བདུན་པ → བཅུ་པ (same in the pre-human OCR prep file) — a gap in the source, not a missing heading |
| Title ordinal vs ID | 3 mismatches (`^…-2-4-4-1-1-2-1-2-4-0` གསུམ་པ, `^…-3-2-6-4-0` གཉིས་པ, `^…-2-2-2-2-1-4-0` གཉིས་པ): each is the 4th sibling; the human text reads གསུམ་པ/གཉིས་པ where the OCR prep reads བཞི་པ. Heading titles were copied from the faulty text reading |
| Malformed title | `^3-2-2-1-1-1-2-2-3-2-8-3-5-2-1-1-0` is "དང་པོ་ནི། ཡན་ལག་གི་མཚན་ཉིད།" |
| Title attested in its section opening or parent's announcement (`attest.md`) | 1342 / 1373; the rest are elided names rebuilt from the parent's list (e.g. ཚད་ཀྱི་དང༌ → ཚད་ཀྱི་སེལ་བ) — checked by hand, acceptable |
| `qc_check_tree.py` vs earlier candidates/enumerations | 29: the 3 ordinals + the gap above + 25 "ordinal not attested" (sa bcad says `དང་པོ་ནི།` apart from the name — expected; the earlier run accepted 22 of these) |
| `qc_tree_vs_source.py` (tree rebuilt from headings, run on the file with headings removed) | 4 sibling-count flags — all checked by hand, all false (count belongs to an ancestor or to a list inside the prose); 199 "cursor loss" flags are an artefact of stacked first-child headings |
| vs earlier tree `toc-tree-anchored-rinphreng-stod.md` | only the 3 retitled ordinals, the 2 bare 8/9 placeholders, and nodes that live in the smad volume (`3.2.2.1.1.2.2.3.2.2`, `…2.4`, `…2.5`, `3.2.2.1.2`, `3.2.2.2`, `4`) |
| `linter-commentary` | TOC passes; fails on `license`, `source`, and block 2 (title-page line) has no block ID |

Volume split: the root announces 4 divisions (file has `^1`–`^3`) and `^3-2-2` announces 2 (file has 1) — the rest is in the smad file, which restarts its own numbering at `^1-0`.
