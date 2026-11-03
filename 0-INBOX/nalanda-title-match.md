# Vinaya sources vs Nalanda-texts-rails — title match

Nalanda candidates scanned: 3566 titles (1-SOURCES/Text, 0-INBOX/commentary, 0-INBOX/root, 0-INBOX/processed/commentaries frontmatter + H1; text_catalog.json; openpecha-v2-catalog.json).

Normalisation: head marks, shad, spaces stripped; trailing ཞེས་བྱ་བ / བཞུགས་སོ dropped. `contains` = one normalised title inside the other (≥4 syllables each); `fuzzy` = syllable similarity ≥ 0.80.


## Verdict (2026-10-15)

| Vinaya file | In Nalanda? | Nalanda file | Nalanda ids | Note |
|---|---|---|---|---|
| `Text/འདུལ་བ་མདོ་རྩ་བ།.md` | **Yes** — exact title | `1-SOURCES/Text/Gu_3CFS.md` (Guṇaprabha) | text_id `BUFmgHSn21hSGhxBHJqqN`, edition_id `u5iZFSA1oC6740V46UHK6` | Same text: first 20k chars 97.8 % similar (Nalanda copy is longer: 336k vs 282k chars of text). |
| `Commentaries/…མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ།.md` | **Yes** — split into 3 volumes there | `0-INBOX/commentary/Gu_3CFU.md`, `Gu_3CFV.md`, `Gu_3CFW.md` (དེབ་དང་པོ / གཉིས་པ / གསུམ་པ) | none — not in `COMMENTARY-UPLOAD-IDS.md`, no text_id | Same text: first 20k chars 98 % similar. Ours is one file (1.76M chars), theirs three (2.06M together). |
| `Commentaries/འདུལ་བའི་མདོའི་རྒྱ་ཆེར་འགྲེལ་པ།.md` | **No** | — | — | Only hit is a fuzzy title match to `འདུལ་བའི་མདོའི་འགྲེལ་པ།` (Gu_3CFX/Y in Nalanda; text_id `5Qae83A4ydsEE1iOKThh0` in openpecha-v2-catalog). That is the *Vinayasūtravṛtti* (བི་ན་ཡ་སཱུ་ཏྲ་བྲྀཏྟི), not this *Vinayasūtraṭīkā* (བི་ན་ཡ་སཱུ་ཏྲ་ཊཱི་ཀ): 0 of 6 random 40-char probes from our file occur in Gu_3CFX/Y. |
| `Commentaries/…དགོངས་རྒྱན།.md` (བློ་གྲོས་ལེགས་བཟང་) | **No** | — | — | Tibetan commentary; Nalanda covers only 17 Indian masters. |
| `Commentaries/…རིན་པོ་ཆེའི་ཕྲེང་བ། སྟོད་ཆ།.md` (དགེ་འདུན་གྲུབ་) | **No** | — | — | Same reason. |
| `Commentaries/…རིན་པོ་ཆེའི་ཕྲེང་བ། སྨད་ཆ།.md` (དགེ་འདུན་གྲུབ་) | **No** | — | — | Same reason. |

Raw title hits follow.

## 1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md

Titles checked: filename `འདུལ་བ་མདོ་རྩ་བ།`; title `འདུལ་བའི་མདོ།`; alt_titles[0] `འདུལ་བ་མདོ་རྩ་བ།`; alt_titles[1] `འདུལ་བའི་མདོ་ཞེས་བྱ་བ།`; h1 `# འདུལ་བའི་མདོ། ^0`

| kind | score | our title | Nalanda title | source | file / id | meta |
|---|---|---|---|---|---|---|
| exact | 1.00 | title | འདུལ་བའི་མདོ། | frontmatter | `1-SOURCES/Text/Gu_3CFS.md` | file_type=root-text, author=སློབ་དཔོན་ཡོན་ཏན་འོད།, author_in_english=Guṇaprabha, text_id=BUFmgHSn21hSGhxBHJqqN, edition_id=u5iZFSA1oC6740V46UHK6 |
| exact | 1.00 | title | # ༄༅། །འདུལ་བའི་མདོ། ^0 | h1 | `1-SOURCES/Text/Gu_3CFS.md` | file_type=root-text, author=སློབ་དཔོན་ཡོན་ཏན་འོད།, author_in_english=Guṇaprabha, text_id=BUFmgHSn21hSGhxBHJqqN, edition_id=u5iZFSA1oC6740V46UHK6 |
| exact | 1.00 | title | འདུལ་བའི་མདོ། | frontmatter | `0-INBOX/root/Gu_3CFS.md` | file_type=root-text, author=སློབ་དཔོན་ཡོན་ཏན་འོད།, author_in_english=Guṇaprabha |
| exact | 1.00 | title | ༄༅། །འདུལ་བའི་མདོ། | text_catalog.json | `Gu_3CFS.md` | pandita=15-Gunaprabha, url=https://wb.pub/3CFS |

## 1-SOURCES/Commentaries/བསྟན་བཅོས་འདུལ་བ་མདོ་རྩ་བའི་སྤྱི་དོན་ཊཱིཀ་ཆེན་རིན་ཆེན་ཕྲེང་བའི་དགོངས་རྒྱན།.md

Titles checked: filename `བསྟན་བཅོས་འདུལ་བ་མདོ་རྩ་བའི་སྤྱི་དོན་ཊཱིཀ་ཆེན་རིན་ཆེན་ཕྲེང་བའི་དགོངས་རྒྱན།`; title `བསྟན་བཅོས་འདུལ་བ་མདོ་རྩ་བའི་སྤྱི་དོན་ཊཱིཀ་ཆེན་རིན་ཆེན་ཕྲེང་བའི་དགོངས་རྒྱན།`; alt_titles[0] `བསྟན་བཅོས་འདུལ་བ་མདོ་རྩ་བའི་སྤྱི་དོན་ཊཱིཀ་ཆེན་རིན་ཆེན་ཕྲེང་བའི་དགོངས་རྒྱན་ལས་གཞི་སྟོད།`; alt_titles[1] `བསྟན་བཅོས་འདུལ་བ་མདོ་རྩ་བའི་སྤྱི་དོན་ཊཱིཀ་ཆེན་རིན་ཆེན་ཕྲེང་བའི་དགོངས་རྒྱན་ལས་གཞི་སྨད།`

**No match in Nalanda.**

## 1-SOURCES/Commentaries/འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་ཕྲེང་བ། སྟོད་ཆ།.md

Titles checked: filename `འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་ཕྲེང་བ། སྟོད་ཆ།`; title `ལེགས་པར་གསུངས་པའི་དམ་པའི་ཆོས་འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་འཕྲེང་བ་ཞེས་བྱ་བ་ལས་གཞི་སྟོད།`; alt_titles[0] `འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་ཕྲེང་བ། སྟོད་ཆ།`; alt_titles[1] `ལེགས་པར་གསུངས་པའི་དམ་པའི་ཆོས་འདུལ་བའི་མདོའི་དགོངས་པ་གསལ་བར་བྱེད་པ་རིན་པོ་ཆེའི་འཕྲེང་བ།`; alt_titles[2] `འདུལ་ཊཱིཀ་རིན་ཆེན་འཕྲེང་བ།`; h1 `# ལེགས་པར་གསུངས་པའི་དམ་པའི་ཆོས་འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་འཕྲེང་བ་ཞེས་བྱ་བ་ལས་གཞི་སྟོད། ^0`

**No match in Nalanda.**

## 1-SOURCES/Commentaries/འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་ཕྲེང་བ། སྨད་ཆ།.md

Titles checked: filename `འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་ཕྲེང་བ། སྨད་ཆ།`; title `ལེགས་པར་གསུངས་པའི་དམ་པའི་ཆོས་འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་ཕྲེང་བ་ཞེས་བྱ་བའི་སྨད་ཆ།`; alt_titles[0] `འདུལ་བ་མཐའ་དག་གི་སྙིང་པོའི་དོན་ལེགས་པར་བཤད་པ་རིན་པོ་ཆེའི་ཕྲེང་བ། སྨད་ཆ།`; alt_titles[1] `འདུལ་ཊཱིཀ་རིན་ཆེན་འཕྲེང་བ།`

**No match in Nalanda.**

## 1-SOURCES/Commentaries/འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ།.md

Titles checked: filename `འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ།`; title `འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ།`; alt_titles[0] `འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ་ཞེས་བྱ་བ།`; alt_titles[1] `འདུལ་བ་མདོའི་འགྲེལ་པ་བཅོམ་བརླག་མ།`

| kind | score | our title | Nalanda title | source | file / id | meta |
|---|---|---|---|---|---|---|
| contains | 0.88 | filename | འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ།༼དེབ་དང་པོ།༽ | frontmatter | `0-INBOX/commentary/Gu_3CFU.md` | file_type=commentary |
| contains | 0.88 | filename | འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ།༼དེབ་གཉིས་པ།༽ | frontmatter | `0-INBOX/commentary/Gu_3CFV.md` | file_type=commentary |
| contains | 0.88 | filename | འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ།༼དེབ་གསུམ་པ།༽ | frontmatter | `0-INBOX/commentary/Gu_3CFW.md` | file_type=commentary |
| contains | 0.88 | filename | ༄༅། །འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ། ༼དེབ་དང་པོ།༽ | text_catalog.json | `Gu_3CFU.md` | pandita=15-Gunaprabha, url=https://wb.pub/3CFU |
| contains | 0.88 | filename | ༄༅། །འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ། ༼དེབ་གཉིས་པ།༽ | text_catalog.json | `Gu_3CFV.md` | pandita=15-Gunaprabha, url=https://wb.pub/3CFV |
| contains | 0.88 | filename | ༄༅། །འདུལ་བའི་མདོའི་འགྲེལ་པ་མངོན་པར་བརྗོད་པ་རང་གི་རྣམ་པར་བཤད་པ། ༼དེབ་གསུམ་པ།༽ | text_catalog.json | `Gu_3CFW.md` | pandita=15-Gunaprabha, url=https://wb.pub/3CFW |
| contains | 0.33 | filename | འདུལ་བའི་མདོའི་འགྲེལ་པ། | openpecha-v2-catalog.json | `5Qae83A4ydsEE1iOKThh0` | file_type=root-text, author=སློབ་དཔོན་ཡོན་ཏན་འོད། [bdrc:P6242], text_id=5Qae83A4ydsEE1iOKThh0 |

## 1-SOURCES/Commentaries/འདུལ་བའི་མདོའི་རྒྱ་ཆེར་འགྲེལ་པ།.md

Titles checked: filename `འདུལ་བའི་མདོའི་རྒྱ་ཆེར་འགྲེལ་པ།`; title `འདུལ་བའི་མདོའི་རྒྱ་ཆེར་འགྲེལ་པ།`

| kind | score | our title | Nalanda title | source | file / id | meta |
|---|---|---|---|---|---|---|
| fuzzy | 0.83 | filename | འདུལ་བའི་མདོའི་འགྲེལ་པ། | openpecha-v2-catalog.json | `5Qae83A4ydsEE1iOKThh0` | file_type=root-text, author=སློབ་དཔོན་ཡོན་ཏན་འོད། [bdrc:P6242], text_id=5Qae83A4ydsEE1iOKThh0 |
