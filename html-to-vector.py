import argparse
import numpy as np
import pandas as pd
from lxml import html
import xml.etree.ElementTree as ET

# program arguments
parser = argparse.ArgumentParser(description="Converts text and attributes in HTML to vectors.")
parser.add_argument('-i', dest="input_html", required=True, help="Path to html file.")
parser.add_argument('-e', dest='target_element', required=False, default='p', help="Element type you want to convert to a vector.")

args = parser.parse_args()

def get_body_elems(html_tree, element):
    """
    Return iterator of all *element*s in the <body> of *html_tree*.
    """
    doc_root = html_tree.find('body')
    elem = doc_root.iterfind(element)
    return elem

def elem_to_dict(element):
    """
    Return dict containing *element*'s attributes + text.
    """
    p_data = element.attrib
    p_data['text'] = ' '.join([txt.strip() for txt in element.itertext()])
    return p_data

def elems_to_df(elements):
    """
    Return dataframe where each row is one element, one column is the text string of that element, and
    """
    # empty list to store paragraph data
    data = []
    # iterate over all <p>s
    for elem in elements:
        record = elem_to_dict(elem)
        data.append(record)

    df = pd.DataFrame(data)
    return df

tree = ET.parse(args.input_html)
# p_elem is iterator of all <p> elements in input file
p_elem = get_body_elems(tree, args.target_element)
# para_data is dataframe of each p in html
para_df = elems_to_df(p_elem)
print (para_df)

"""
TO DO
* Pull target variable out into its own numpy array y
* Convert 'text' column to bag-of-words scipy.sparse matrix
* Process entire directory of html files, add some sort of document_id column
"""
