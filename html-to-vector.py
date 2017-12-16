import argparse
from lxml import html, etree
import xml.etree.ElementTree as ET

# program arguments
parser = argparse.ArgumentParser(description="Converts text and attributes in HTML to vectors.")
parser.add_argument('input_html', help="Path to html file.")

args = parser.parse_args()

def get_body_elems(html_path, element):
    """
    Return iterator of all *element*s in the <body> of *html_path*.
    """
    html_tree = ET.parse(html_path)
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

def elems_to_dict(elements):
    """
    Return dict where each key is the 'data-source-id' for a given element and each value is a dictionary containing that element's attributes and text.
    """
    # empty dict to store paragraph data
    data = {}
    # iterate over all <p>s
    for elem in elements:
        record = elem_to_dict(elem)
        data[record['data-source-id']] = record

    return data

# p_elem is iterator of all <p> elements in input file
p_elem = get_body_elems(args.input_html, 'p')
# para_data is dict of dicts of each p in html
para_data = elems_to_dict(p_elem)
print (para_data)
