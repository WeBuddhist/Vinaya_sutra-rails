# 2026-10-15 — Root text re-segmented to Nalanda's structure

**File:** `1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md`
**Pre-change copy:** `འདུལ་བ་མདོ་རྩ་བ།.pre-nalanda-seg.md` (this folder; same as git `HEAD` before the change)
**Structure taken from:** Nalanda-texts-rails `1-SOURCES/Text/Gu_3CFS.md` @ `fd801eb3`

## What changed

- **TOC:** 19 headings → 39 headings, identical to Nalanda (36 `##` chapters, `^1-0` … `^34-0`, plus `^I-0`, `^a-0`, `^a-1-0`, `^a-2-0`). The old file had 14 coarser chapters (`^1-0` … `^14-0`), so **the same chapter number now names a different chapter** (e.g. old `^4-0` གསོ་སྦྱོང་གི་གཞི = new `^19-0`).
- **Segmentation:** 1217 human-paragraph block IDs → 1188 content blocks with Nalanda's block IDs, in Nalanda's order. 0 duplicates.
- **Text:** unchanged. Letters identical to the pre-change file (295,339 non-whitespace chars both sides). Only whitespace changed: where one Nalanda block spans two old paragraphs, the old paragraph break became a space.
- **Frontmatter:** added Nalanda's `bdrc_work_id`, `category_id`, `category_name`, `text_id`, `edition_id`, `toc_id`, `openpecha_text_id`.

## Consequence

Any rail or transclusion that cites a block ID in this file and was written before this date is citing the old scheme and must be re-checked. At the time of the change nothing in `2-RAILS/` or `1-SOURCES/Commentaries/` cited it.

A human contributor should record this in the vault annex (`4-SYSTEM/Guidelines/vault-annex.md` → *Re-segmentation and ID-migration log*).

## Edition variants against Nalanda

Our text and Nalanda's (footnotes removed) agree on 79,287 of ~79,300 syllables. The 18 blocks whose wording differs, i.e. where our reading was kept and Nalanda's was not taken:

`^2-28` `^2-43` `^2-59` `^4-13` `^8-40` `^9-158` `^14-1` `^14-5` `^18-6` `^20-18` `^25-2` `^26-20` `^34-44` `^34-48` `^34-59` `^34-69` `^34-92` `^a-2`

Because of these, our file is **not byte-identical to the edition behind `edition_id u5iZFSA1oC6740V46UHK6`**, and it carries none of Nalanda's 2090 durchen footnotes.
