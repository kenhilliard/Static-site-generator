import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title_single_heading(self):
        md = """
Some text
Another line
# My Title
"""
        markdown = extract_title(md)
        self.assertEqual(markdown, "My Title")

    def test_extract_title_extra_whitespace(self):
        md = "\n#   My Title     \nSome text\n"
        markdown = extract_title(md)
        self.assertEqual(markdown, "My Title")

    def test_extract_title_no_heading(self):
        md = """
Some text
Another line
No heading here
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_h2_heading_no_h1_heading(self):
        md = """
Some text
Another line
## Sub heading
"""
        with self.assertRaises(Exception):
            extract_title(md)
