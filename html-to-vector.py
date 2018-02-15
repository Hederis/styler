import argparse
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from lxml import html
from lxml import etree, objectify
import xml.etree.ElementTree as ET

# program arguments
parser = argparse.ArgumentParser(description="Converts text and attributes in HTML to vectors.")
parser.add_argument('-i', dest="input_html", required=True, help="Path to html file.", metavar="FILE")
parser.add_argument('-e', dest='target_element', required=False, default='p', help="Element type you want to convert to a vector.")

args = parser.parse_args()

def getAllText(node):
    text = node.text if node.text else None
    if text:
        yield text
    for child in node:
        yield from getAllText(child)
    tail = node.tail if node.tail else None
    if tail:
        yield tail

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
    Return dataframe where each row is one element, one column is the text string of that element, and the element's attributes are the rest of the columns
    """
    # empty list to store paragraph data
    data = []
    # iterate over all <p>s
    for elem in elements:
        record = elem_to_dict(elem)
        data.append(record)

    df = pd.DataFrame(data)
    return df

# tree = etree.parse(args.input_html)
# p_elem is iterator of all <p> elements in input file
# p_elem = get_body_elems(tree, args.target_element)
# para_data is dataframe of each p in html
# para_df = elems_to_df(p_elem)
# print (para_df)

# need array of all class names - export from csv?

dataframe = []
targets = []
root = etree.parse(args.input_html)
for para in root.findall(".//p"):
    targets.append(para.get("class"))
    g = getAllText(para)
    mytext = ' '.join(g)
    dataframe.append(mytext)

last_feature = []
last_feature.append(dataframe.pop())
print(last_feature)
last_target = []
last_target.append(targets.pop())
print(last_target)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(dataframe)
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
training_features = tf_transformer.transform(X_train_counts)

labels = LabelEncoder()
training_labels = labels.fit_transform(targets)

# this is our algorithm!
clf = MultinomialNB().fit(training_features, training_labels)

newpara_count = count_vect.transform(last_feature)
newpara_transformer = TfidfTransformer(use_idf=False).transform(newpara_count)

predicted = clf.predict(newpara_transformer)

#print(labels.inverse_transform(training_labels)[9])
# for label in labels.inverse_transform(training_labels):
#     print(label)
# print(predicted)

"""
TO DO
* Pull target variable out into its own numpy array y
* Convert 'text' column to bag-of-words scipy.sparse matrix
* Process entire directory of html files, add some sort of document_id column
"""
