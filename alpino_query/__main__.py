#!/usr/bin/env python3
import sys

from . import AlpinoQuery


def help():
    print("""
[action]
    parse
    mark
    subtree
    xpath

For parse:
    parse [tokens]

For mark:
    mark [inputxml] [tokens] [attributes]

For subtree:
    subtree [marked xml] [remove=rel/relcat/cat]

For xpath:
    xpath [subtree xml] [order=1/0]
""")


def main():
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        help()
        return

    query = AlpinoQuery()
    if action == "parse":
        sentence = sys.argv[2:]
        if len(sentence) == 0:
            help()
            return
        alpino_xml = query.parse(sentence)
        print(alpino_xml)
    elif action == "mark":
        [inputxml, tokens, attributes] = sys.argv[2:]
        query.mark(inputxml.replace('\\n', '\n'),
                   tokens.split(' '), attributes.split(' '))
        print(query.marked_xml)
    elif action == "subtree":
        [inputxml, remove] = sys.argv[2:]
        query.marked_xml = inputxml.replace('\\n', '\n')
        query.generate_subtree(remove)
        print(query.subtree_xml)
    elif action == "xpath":
        [inputxml, order] = sys.argv[2:]
        query.subtree_xml = inputxml.replace('\\n', '\n')
        query.generate_xpath(order in ['true', 'True', '1', 1, True])
        print(query.xpath)
    else:
        help()


if __name__ == "__main__":
    main()
