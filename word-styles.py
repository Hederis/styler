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
max_variations = 3
max_levels = 5
identifier = "h"
style_source_file = "stylenames.csv"

def style_names(source_file, number_of_variations, number_of_levels, id_prefix):
    variations = list(string.ascii_lowercase[:number_of_variations])
    # range end is exclusive, so add 1
    levels = list(range(1,number_of_levels+1))
    wrappers = ["start", "end"]
    # document = Document()
    # docstyles = document.styles
    finalnames = []
    with open(source_file, 'rU') as csvfile:
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
    return finalnames

def add_styles_to_doc(word_docx, list_of_styles):
    document = Document(word_docx)
    docstyles = document.styles
    for stylename in list_of_styles:
        if stylename not in docstyles:
            docstyles.add_style(stylename, WD_STYLE_TYPE.PARAGRAPH)
            # p = document.add_paragraph(finalname, style=finalname)
    document.save(word_docx)

styles = style_names(style_source_file, max_variations, max_levels, identifier)
docs = sys.argv[1]
if os.path.exists(docs):
    if os.path.isdir(docs):
        os.chdir(docs)
        # reverse to print countdown as files are processed
        for i, file in enumerate(glob.glob("*.docx")):
            print i
            add_styles_to_doc(file, styles)
    elif os.path.isfile(docs):
        add_styles_to_doc(docs, styles)
