import csv
import string
import glob
import os
import sys
from distutils.util import strtobool
from docx import Document
from docx.enum.style import WD_STYLE_TYPE

"""
stylenames.csv has one row for each *base* style name, and columns for the following:
prefix:
    "sec" = section-start style
    "wpr" = wrapper style
    "blk" = block style (paragraph)
    "inl" = inline style (character)
name: descriptive name for the style
levels: are levels allowed for this style? [boolean]
variations: are variations allowed? [boolean]
type: "1" for Paragraph, "2" for Character

All versions for wrappers, levels, variations, etc. will be expanded automatically here; edit first variables below to adjust number of variations and number of levels created for each.

See README for explanation of style name syntax rules.
"""

# various settings here
number_of_variations = 3
number_of_levels = 5
id_prefix = "h"

variations = list(string.ascii_lowercase[:number_of_variations])
# range end is exclusive, so add 1
levels = list(range(1,number_of_levels+1))
wrappers = ["start", "end"]
# document = Document()
# docstyles = document.styles
finalnames = []
with open("stylenames.csv") as csvfile:
    ourstyles = csv.DictReader(csvfile)
    for style in ourstyles:
        if int(style["type"]) == WD_STYLE_TYPE.PARAGRAPH:
            stylenames = [style["name"]]
            if strtobool(style["levels"]) == True:
                stylenames = [x + str(y) for x in stylenames for y in levels]
            if strtobool(style["variations"]) == True:
                stylenames = [x + "_" + y for x in stylenames for y in variations]
            if style["prefix"] == "wpr":
                stylenames = [x + "_" + y for x in stylenames for y in wrappers]

            finalnames = finalnames + ["_".join([id_prefix,style["prefix"],x]) for x in stylenames]

    docdir = sys.argv[1]
    if os.path.exists(docdir):
        os.chdir(docdir)
        # reverse to print countdown as files are processed
        for i, file in enumerate(glob.glob("*.docx")):
            print i
            document = Document(file)
            docstyles = document.styles

            for finalname in finalnames:
                docstyles.add_style(finalname, int(style["type"]))
                # p = document.add_paragraph(finalname, style=finalname)
            document.save(file)
#document.save('styles.docx')
