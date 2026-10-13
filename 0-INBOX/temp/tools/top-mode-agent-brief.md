# Task: top-level TOC tree for a word-commentary on the Vinaya Sutra (mode `top`)

Read `4-SYSTEM/Skills/commentary-toc-extract/prompts/verse-headings.md` (section "Mode `top`", "Anchors", "Output") and
`4-SYSTEM/Skills/seg-toc-lib/prompts/pass5-anchors.md` (sections "Frame nodes", "Copying the context") first. Their worked
example is a Tara praise; here the root text is the Vinaya Sutra, so apply the same rules with these substitutions.
(Vault root = `/Users/tashitsering/Desktop/work/Obsidian/Vinaya_sutra-rails`; run commands from there.)

## Substitutions
The commentary is a word-by-word explanation that follows the root text part by part. The "root text's own sections" are
its 14 parts, in this order. Titles are fixed: copy them exactly from here (they are the root text's own headings).

1 རབ་ཏུ་འབྱུང་བའི་གཞི། · 2 དགེ་སློང་གི་རྣམ་པར་འབྱེད་པ། · 3 དགེ་སློང་མའི་རྣམ་པར་འབྱེད་པ། · 4 གསོ་སྦྱོང་གི་གཞི། ·
5 དབྱར་གྱི་གཞི། · 6 དགག་དབྱེའི་གཞི། · 7 ཆོས་གོས་སྲ་བརྐྱང་གི་གཞི། · 8 གོས་ཀྱི་གཞི། · 9 ཀོ་ལྤགས་ཀྱི་གཞི། ·
10 བཤང་བའི་བསྐྱབ་བྱ། · 11 གཅི་བའི་བསྐྱབ་བྱ། · 12 ས་གཞན་ན་གནས་པའི་སྤྱོད་པའི་གཞི། · 13 འཁོར་ལོ་དབྱེ་བའི་གཞི། · 14 འཁྲུག་ལོང་གི་རྒྱུ་བཞི།

(The root text with these headings: `1-SOURCES/Text/འདུལ་བ་མདོ་རྩ་བ།.md`; you only need it if a boundary is unclear.)

Rules, fixed (do not decide case by case):
1. Top level `1.`–`14.` = those parts, in order, **no children** ("no descent"). Include only parts the commentary really has.
2. A part begins where the commentary starts explaining that part's first root sentence, or at its own announcement if it
   has one. The previous part's closing line (typically `… རྫོགས་སོ།` such as `རབ་ཏུ་བྱུང་བའི་གཞི་རྫོགས་སོ།`,
   `དགེ་སློང་གི་རྣམ་པར་འབྱེད་པ་རྫོགས་སོ།`, `གསོ་སྦྱོང་གི་གཞི་རྫོགས་སོ།`) ends it; the next block begins the next part.
   Closers of sub-sections (`… ཕྲན་ཚེགས་ཀྱི་སྐབས་རྫོགས་སོ།`, `… སྤང་བ་རྣམས་རྫོགས་སོ།`) do NOT end a top-level part.
3. Frame nodes per the pass-5 table, only where the text has them: `* I. མཆོད་བརྗོད།` (homage and opening verses at the top,
   before part 1; also the author's promise to explain), `* II. <own title>` only for a distinct introductory section
   before part 1 (e.g. an outline or purpose section; may have its own numbered children only if the commentary announces
   them), `* a. བསྔོ་བ།` (closing dedication verses, e.g. `ཁྱེད་ཀྱིས་དགེ་བ་གང་ཐོབ་པ། …`), `* b. མཇུག་བྱང།` with children
   `* b.1 མཛད་བྱང།` / `* b.2 འགྱུར་བྱང།` (author's and translators' colophons; order as in the text; if there is no
   dedication, use `a.` / `a.1`). The frame line order in the file: I, II, 1..14, a, b.
4. If the file ends before all 14 parts are treated (it may be an incomplete file), list only the parts present, and say so in
   your reply. Do not invent a part.

## Method (the file is several MB: NEVER read it whole)
- Find the part boundaries with grep, e.g. `grep -n 'རྫོགས་སོ' "<file>" | grep -E '<part closer>'` and `grep -n` for each of the
  14 part names. Then read only about 10–25 lines (`sed -n 'A,Bp'`) around each boundary and the first ~40 and last ~40 lines of
  the file.
- Copy each `[[context]]` as the first 12–20 syllables at the node's beginning, character for character (tshegs, shads,
  spaces exactly as in the file). It must occur in order, each after the previous node's context.
- Verify before finishing, with a small script (`python3 -I`): remove all whitespace from the file and from each context;
  every context must be found, contexts must be unique-or-ordered (each found at or after the previous one's position),
  and positions must be strictly increasing in file order. Fix any failure.

## Output
Write the tree to the output path you are given, in this exact format (3 spaces per indent level, none needed here):

```
## དཀར་ཆག / Table of Contents

* I. མཆོད་བརྗོད། [[…]]
* 1. རབ་ཏུ་འབྱུང་བའི་གཞི། [[…]]
…
* a. བསྔོ་བ། [[…]]
* b. མཇུག་བྱང། [[…]]
   * b.1 མཛད་བྱང། [[…]]
   * b.2 འགྱུར་བྱང། [[…]]
```
Do not edit any other file. Reply with: the output path, which of parts 1–14 were found, the line number where each begins,
where the text ends (last line number and what it is in the root's structure), and any doubtful boundary.
