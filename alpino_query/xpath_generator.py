#!/usr/bin/env python3
# XPathGenerator.pl
# Alpino-XML XPath Generator

# version 1.7 date: 10.06.2015  bug fix (@number)
# version 1.6 date: 15.12.2014  bug fix (ignore not-function if word order is checked)
# version 1.5 date: 14.10.2014  RELEASED WITH GrETEL2.0
# written by Vincent Vandeghinste and Liesbeth Augustinus (c) 2014
# for the GrETEL2.0 project

# script converts an XML tree into an XPath expression

############################################################################
# argument: -xml: path to xml-subtree
# options: -order/-o: word order is important
#          -r: exclude root node from the XPath expression
#          -version/-v: script details
#          -in: attributes to include (comma-separated list)
#          -ex: attributes to exclude (comma-separated list)

############################################################################

import sys
import re
from lxml import etree

def generate_xpath(twig, order):
    root = twig

    if root.xpath('/alpino_ds'):
        # for ALPINO XML, leave out the alpino_ds node
        subtree = root.find('node')
    else:
        subtree = root    # start at root node

    # generate XPath expression

    topxpath = GetXPath(subtree)
    xpath = ProcessTree( subtree, order )

    if xpath and topxpath:    # if more than one node is selected
        xpath = '//' + topxpath + ' and ' + xpath + ']'

    elif xpath and not topxpath:
        xpath = '//*[' + xpath + ']'

    elif not xpath and topxpath:
        xpath = '//' + topxpath + ']'    # if only one node is selected

    else:
        print("ERROR: no XPath expression could be generated.\n")

    if 'not' in xpath:                # exclude nodes using not-function
        xpath = re.sub(r'\sand\s\@not=".*?"', '')

    return xpath

def ProcessTree(tree, order):
    xpath = ''
    children = tree.getchildren()
    childxpaths = []; COUNTS = {}; ALREADY = set()
    if len(children) > 0:
        for child in children:
            childxpath = GetXPath(child)

            if childxpath:
                lower = ProcessTree( child, order )
                if lower:
                    childxpath += ' and ' + lower + ']'

                else:
                    childxpath += ']'

                    if 'not' in childxpath:
                        # exclude nodes using not-function
                        childxpath = 'not(' + childxpath + ')'
                        childxpath = re.sub(r'\sand\s\@not=".*?"', '')

                COUNTS[childxpath] = COUNTS.get(childxpath, 0) + 1
                childxpaths.append( childxpath )

        if childxpaths:
            i = 0
            while (i < len(childxpaths)):

                ## ADD COUNT FUNCTION
                if COUNTS[childxpaths[i]] > 1:
                    childxpaths[i] = \
                        'count(' \
                      + childxpaths[i] + ') > ' \
                      + ( COUNTS[childxpaths[i]] - 1 )

                ## REMOVE DOUBLE DAUGHTERS
                if childxpaths[i] in ALREADY:
                    childxpaths = childxpaths[:i] + childxpaths[i+1:]
                    i -= 1

                else:
                    ALREADY.add(childxpaths[i])

                i += 1

            xpath = str.join( ' and ', childxpaths )

        else:
            #die "not implemented yet\n";
            return None

    else:    # no children
        if order:
            xpath = 'number(@begin)'
            next_term, nextpath = FindNextTerminalToCompare(tree)
            if next_term is not None:
                if float(tree.attrib.get('begin', 'nan')) < float(next_term.attrib.get('begin', 'nan')):

                    xpath += " < "

                else:
                    xpath += " > "

                xpath += nextpath

            else:
                return None

    return xpath

def FindNextTerminalToCompare(tree):
    next_sibling = tree.getnext()
    if next_sibling is not None:
        path = "../"
        next_terminal, xpath = FindNextLeafNode(next_sibling)
        path = path + xpath
        if 'begin' in path:

            # $path='number('.$path.')';
            path = re.sub(r'\@begin', 'number(@begin)', path)

    else:
        # go up the tree to find next sibling
        parent = tree.getparent()
        if parent is not None:
            next_terminal, nextpath = FindNextTerminalToCompare(parent)
            if not nextpath:
                return None, None

            path = "../" + nextpath

        else:
            return None, None
        
    return next_terminal, path

def FindNextLeafNode(node):
    children = node.getchildren()
    xpath = GetXPath(node) + ']'

    if len(children) > 0:
        node, childpath = FindNextLeafNode( children[0] )
        xpath += "/" + childpath
        return node, xpath

    else:
        path = xpath + '/@begin'
        return node, path

def GetXPath(tree):
    att = tree.attrib
    atts = []

    for key in att:
        # all attributes are included in the XPath expression...
        if not re.match(r'/postag|begin|end/', key):    # ...except these ones
            atts.append("@" + key + "=\"" + att[key] + "\"")


    if not atts:

        # no matching attributes found
        return ''

    else:
        # one or more attributes found
        string = str.join( " and ", atts )
        xstring = "node[" + string

        return xstring

[inputxml, order] = sys.argv[1:]
twig = etree.fromstring(bytes(inputxml, encoding='utf-8'))
if order in ['false', 'False', '0', 0, False]:
    order = False
else:
    order = True

xpath = generate_xpath(twig, order)
print(xpath)
