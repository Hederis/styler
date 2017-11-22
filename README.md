# Style Yr Manuscripts
* _stylenames.csv_: stores style names we're using, see below for syntax/rules
* _word-styles.py_: pass path to a file or directory as an argument, it will add styles to _.docx_ (or all _.docx_ files in directory)

# Style name syntax
1. Single letter id
2. Underscore + type of style
    `sec`: section start
    `wpr`: wrapper
    `blk`: block
    `inl`: inline
1. Underscore + descriptive style name; multiple words separated by hyphens
2. Level number (no underscore), if levels are required
3. Underscore + version letter, if versions are allowed
4. Underscore + `start` or `end`, if it's a wrapper style.

ID, number of levels, and number of variations can be configured in *word-styles.py*.

## Rules
* Base style names must include only lowercase letters.
* Numerals allowed only for different levels.
* Base style names with more than one word must be separated by hyphens ("copyright-page").
* Each item other than level must be separated by an underscore.
* No spaces or special characters.
* Can't have both level and version (?).
* If it can have levels or versions, always needs to have it in the name (i.e., must have `1` or `a`, even if the only one is in use in that doc).

## Examples
`h_sec_titlepage`
`h_wpr_bullet-list_a_start`
`h_blk_li1`
`h_inl_bold`

# Styling Notes
1. Replace soft returns with hard returns in source before styling manuscript.
2. Delete source data at begin / end of manuscript file.

# To do
[x] Handle "style already exists"
[x] If parameter value is a file, add style to file only; if value is a directory, add styles to all .docx in directory.
[] Add simple formatting, particularly something to distinguish start/end
[] Add more granular copyright page styles
[] Add simple heuristics to style relatively standard items
[] Character styles
