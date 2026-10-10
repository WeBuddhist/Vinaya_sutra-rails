Read `4-SYSTEM/Skills/commentary-toc-ingest/SKILL.md` in full, then execute it on the file(s) or input the user specifies.

Skill purpose: Step 4 of commentary-pipeline: ingest an anchored TOC tree (written by commentary-toc-extract's pass 5) into a segmented commentary by inserting markdown headings with block IDs, the way the vault's human-edited commentaries carry them: each heading at the start of the block where its section begins, parent and first-child headings stacked, front/back-matter frame headings (^I-0, ^a-0, ^b-1-0), siblings in the order of the text.
