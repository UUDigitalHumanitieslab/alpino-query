#!/usr/bin/env python3
"""
Run the commands and write their output
"""

import sys
from os import path
import glob

testdir = path.dirname(__file__)
datadir = path.join(testdir, "data")
# import this implementation
sys.path.insert(0, path.join(testdir, ".."))

from alpino_query.xpath_generator import main as xpath_generator
from alpino_query.subtree import main as subtree
from alpino_query import mark

def read(filename):
    with open(path.join(datadir, filename)) as f:
        return f.read()


def write(filename, content):
    with open(path.join(datadir, filename), "w") as f:
        f.write(content)


def update(basename):
    [tokens, attributes, options, order] = read(basename + ".txt").splitlines()

    alpino_xml = read(basename + ".xml")
    marked = mark(alpino_xml,
                  tokens.split(' '),
                  attributes.split(' '))
    write(basename + ".marked.xml", marked)

    tree = subtree([marked, options])
    write(basename + ".subtree.xml", tree)

    xpath = xpath_generator([tree, order])
    write(basename + ".xpath", xpath)

input_files = glob.glob(path.join(datadir, '*.txt'))
for input in input_files:
    head, ext = path.splitext(path.basename(input))
    update(head)
