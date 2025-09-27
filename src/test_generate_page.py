import unittest

from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def extract_title_finds_title(self):
        markdown = """
#EE
# Hello
## sad;fojiasdf

random line
"""
        res = extract_title(markdown)
        self.assertEqual(res, "Hello")

    def extract_title_raises_exception(self):
        markdown = """
#EE
#Hello
## sad;fojiasdf

random line
"""
        with self.assertRaises(Exception):
            res = extract_title(markdown)