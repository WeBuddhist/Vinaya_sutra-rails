# Rin chen phreng ba (smad) — TOC verification, 2026-10-15

Headings in `1-SOURCES/Commentaries/…རིན་པོ་ཆེའི་ཕྲེང་བ། སྨད་ཆ།.md`. Before the check: 449 of 566 headings were capped at `######`; expanded to true depth (levels 2–14). Afterwards a `#` title (`^0`) and `## མཆོད་བརྗོད། ^I-0` were added, with the title-page line as `^I-1` (same opening as the stod volume).

| Check | Result |
|---|---|
| IDs unique, nested, `#` = depth, no level skip, sibling numbering | clean |
| Title ordinal vs ID | 2 mismatches: `^4-3-3-1-5-0` says བཞི་པ (5th of 6; OCR prep reads ལྔ་པ), `^5-2-4-1-2-2-0` says བཞི་པ (2nd of 2; OCR prep reads གཉིས་པ). The human text carries the same wrong ordinals |
| Title attested in its section opening or parent's announcement | 550 / 566; the 16 others checked by hand — elided names rebuilt from the parent's list, one variant reading `(འགྱུར་,འབྱུང་)`, and the editorial labels `^b-0` / `^b-1-0` |
| `qc_check_tree.py` vs earlier candidates/enumerations | 14: the 2 ordinals + 12 "ordinal not attested" (expected for sa bcad) |
| `qc_tree_vs_source.py` | 0 sibling-count flags; 170 "cursor loss" are an artefact of stacked first-child headings |
| vs earlier tree | only the 2 retitled ordinals |
| `linter-commentary` | TOC passes; fails only on missing `license` and `source` |

Numbering: this volume restarts at `^1-0` (སོ་སོའི་མཚན་ཉིད), continuing the stod volume's `3.2.2.1.1.2.2.3.2` and on — the two files are not one continuous ID space.
