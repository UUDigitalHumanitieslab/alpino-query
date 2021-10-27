#!/usr/bin/env python3
import sys
import re
from lxml import etree

def mark_interesting(twig, tokens, attributes):
    # add info annotation matrix to alpino parse
    for begin, token in enumerate(tokens):
        if (re.match(r"([_<>\.,\?!\(\)\"\'])|(\&quot;)|(\&apos;)", token)):
            xp = twig.xpath(f"//node[@begin='{begin}']")
        else:
            xp = twig.xpath(f"//node[@word='{token}' and @begin='{begin}']")
        if begin < len(attributes):
            attr = attributes[begin]
            for x in xp:
                if attr == 'cs':
                    x.attrib['interesting'] = 'token'
                elif attr == 'token':
                    x.attrib['interesting'] = 'token'
                    x.attrib['caseinsensitive'] = 'yes'
                else:
                    x.attrib['interesting']  = attr

[inputxml, tokens, attributes] = sys.argv[1:]

twig = etree.fromstring(bytes(inputxml, encoding='utf-8'))
mark_interesting(twig, tokens.split(' '), attributes.split(' '))
print(etree.tostring(twig, pretty_print=True).decode())
