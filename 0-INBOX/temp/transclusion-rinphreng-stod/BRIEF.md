# Brief — root-text transclusion map for the Rin chen phreng ba (stod), one part

You map where a Tibetan commentary quotes, glosses or cites its root text, for ONE part of the file
(your part id and line range are given in your task). Same method as the Dgongs rgyan run
(`0-INBOX/temp/transclusion-dgongs-rgyan/place-*.tsv` shows finished examples of the output).

Run every command from the vault root `D:\Work\OpenPecha\Vinaya_sutra-rails`. Use `python -I` for scripts.

## Files (read-only)
- Commentary: `0-INBOX/temp/transclusion-rinphreng-stod/source.md` — exact copy of
  `1-SOURCES/Commentaries/…རིན་པོ་ཆེའི་ཕྲེང་བ། སྟོད་ཆ།.md` (Gendun Drub's commentary on the Vinayasūtra).
  Blocks are separated by blank lines; each content block ends with its own `^id`; headings start with `#`.
- Root text: `1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md` (Guṇaprabha's Vinayasūtra; 34 `##` chapters, block ids `^C-N`,
  front `^I-N`, colophon `^a-N`). Look a root block up with e.g. `grep -n "\^7-12\s*$" <root>`.
- Seeds: `0-INBOX/temp/transclusion-rinphreng-stod/seeds/seeds-<PART>.tsv` — every place where a commentary block
  shares ≥ 6 consecutive syllables with a root block (`line` = first line of the commentary block,
  `matched_syllables` = length of the shared run, `same_words_also_match` = other root blocks the same words also
  match, `preview` = the shared words with a little context). Seeds are evidence, not answers.

Never edit any file except your output file. Do not read the whole commentary at once: read your range in pieces
(e.g. 150 lines at a time).

## What to produce
`0-INBOX/temp/transclusion-rinphreng-stod/place-<PART>.tsv`, UTF-8, tab-separated, this header exactly:

```
heading	root_block	line	kind	words
```

One row per (commentary block, root block) that the block quotes, glosses or cites:
- `heading` — the block id of the nearest heading above the block (e.g. `3-2-1-1-2-0`), for reference.
- `root_block` — the root block id without `^` (e.g. `1-23`).
- `line` — the FIRST line number (1-based, in source.md) of the commentary block. Never a heading line, never a blank
  line, never the 2nd+ line of a multi-line block. The transclusion will be inserted directly before this block.
- `kind` — one of:
  - `lemma`: the block quotes the root's words in order to explain them (typically `… ཞེས་པ / ཞེས་སོ / ཞེས་བྱ་བ /
    ཞེས་སོགས / ཞེས་པ་ནས … ཞེས་པའི་བར`, or introduced by `རྩ་བར། / མདོ་རྩ་བར། / གཞུང་ལས།`).
  - `gloss`: the block explains a specific root block in its own words without quoting more than a few syllables
    (e.g. a `ངག་དོན་ནི།` paraphrase, or a `ཚིག་དོན།` section going through a sūtra).
  - `proof`: the block cites the root as authority for a point about some other topic (`འདི་ཉིད་ལས། / རྩ་བ་ལས། /
    མདོ་རྩ་བ་ལས། …` + a root sentence).
- `words` — the root words as the commentary gives them (short; ≤ 25 syllables; `…` to elide), so a reviewer can see why.

## Rules
1. **Only the root text counts.** The commentary also quotes the āgama (`ལུང་`, `ལུང་རྣམ་འབྱེད`, `ལུང་ཕྲན་ཚེགས` …),
   Guṇaprabha's own commentary (`འགྲེལ་པ`, `རང་འགྲེལ`), Dharmamitra's (`ཊཱིཀ་`), the Kośa (`མཛོད`), Tsonawa (`མཚོ་སྣ་བ`)
   and others. A quotation from another work is not a root citation — unless the shared words are the root's own
   sentence that the commentary is explaining there.
2. **Seeds: decide each one.** Keep a seed when the block really quotes/explains/cites THAT root block. When
   `same_words_also_match` lists other root blocks (a rule or formula worded the same in several places), choose the
   one the commentary is discussing here — normally the one in the root chapter this part of the commentary explains
   (pārājika section → root ch.3–6, saṃghāvaśeṣa → ch.7, naiḥsargika → ch.8, pāyantika → ch.9, …); a proof may come
   from any chapter. Drop seeds that are only a stock phrase (e.g. `ཉེས་པ་མེད་དོ།`, `ཉེས་བྱས་སུ་འགྱུར་རོ།`) with no
   specific root sentence behind them, and drop matches that sit inside a quotation of another work (rule 1).
3. **Look for what the matcher missed.** Read every content block in your range. Short lemmas (< 6 syllables, e.g.
   `… ཞེས་སོགས་`), abbreviated lemmas (`… ཞེས་པ་ནས་ … ཞེས་པའི་བར་`) and paraphrases do not appear in the seeds. Find their
   root block by searching the root text for the quoted syllables; add a row only when you are confident which root
   block it is.
4. A block can carry several root blocks (several rows with the same `line`); a root block can appear at many lines.
   Do not add a row just because a block lies inside a section about some sūtra — only blocks that quote, gloss or
   cite it.
5. **Validate before you finish** and fix every problem it reports:
   `python -I 0-INBOX/temp/transclusion-rinphreng-stod/validate_place.py 0-INBOX/temp/transclusion-rinphreng-stod/place-<PART>.tsv <PART>`

## Reply (≤ 15 lines)
The output path; rows by kind; seeds kept / dropped (and the main reasons for drops); rows added beyond the seeds;
root chapters covered; anything you were unsure of (line + root block), and the validator's last line.
