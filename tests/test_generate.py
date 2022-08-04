#!/usr/bin/env python3
"""
Unit test for generating a query
"""
import difflib
import unittest
import glob
from os import path

from alpino_query import AlpinoQuery


class TestConsole(unittest.TestCase):
    datadir = path.join(path.dirname(__file__), "data")

    def test(self):
        input_files = glob.glob(path.join(self.datadir, '*.txt'))
        for input in input_files:
            head, ext = path.splitext(path.basename(input))
            self.assert_sentence(head)

    def assert_sentence(self, basename):
        [tokens, attributes, remove, order] = self.read(
            basename + ".txt").splitlines()

        query = AlpinoQuery()
        alpino_xml = self.read(basename + ".xml")
        query.mark(alpino_xml,
                   tokens.split(' '),
                   attributes.split(' '))

        self.compare_lines(basename + ".marked.xml", query.marked_xml)

        query.generate_subtree(remove.split(','))
        self.compare_lines(basename + ".subtree.xml", query.subtree_xml)

        query.generate_xpath({"0": False, "1": True}[order])
        # add a newline, because the output of the console script ends
        # with a newline
        self.compare_lines(basename + ".xpath", query.xpath + '\n')

    def read(self, filename):
        with open(path.join(self.datadir, filename)) as f:
            return f.read()

    def compare_lines(self, filename_expected, actual):
        expected = self.read(filename_expected).split('\n')

        diff_lines = list(difflib.context_diff(
            expected,
            actual.split('\n'),
            filename_expected + ' (expected)',
            filename_expected + ' (actual)'))

        if len(diff_lines) > 0:
            self.fail('\n'.join(line for line in diff_lines))
