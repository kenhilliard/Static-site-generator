import unittest
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, text_to_children, heading_level_from_block, quote_from_block, unordered_list_from_block, ordered_list_from_block, code_from_block, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_excessive_blank_lines(self):
        md = """
This is a test with **three** newlines between blocks



This is another paragraph with _italic_ text and `code` here



This is the same paragraph on a new line


-This is a list

-With items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a test with **three** newlines between blocks",
                "This is another paragraph with _italic_ text and `code` here",
                "This is the same paragraph on a new line",
                "-This is a list",
                "-With items",
            ],
        )

    def test_leading_trailing_whitespace(self):
        md = """

This is a test with leading and trailing whitespace

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a test with leading and trailing whitespace",
            ],
        )

    def test_single_block_only(self):
        md = """
This is a test with no double newlines at all
This is **another** paragraph
and another
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a test with no double newlines at all\nThis is **another** paragraph\nand another",
            ],
        )

    def test_whitespace_only(self):
        md = """


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_block_headings(self):
        self.assertEqual(block_to_block_type("# heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#no space"), BlockType.PARAGRAPH)

    def test_block_to_block_code(self):
        self.assertEqual(block_to_block_type("```\ncode```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```no newline```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```no ending tripple backticks"), BlockType.PARAGRAPH)

    def test_block_to_block_quote(self):
        self.assertEqual(block_to_block_type(">This is a quote\n>On two lines"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> This is also a quote\n> This is the second line"), BlockType.QUOTE)
    
    def test_block_to_block_unordered_list(self):
        self.assertEqual(block_to_block_type("- line one of an unordered_list\n- Line two of an unordered_list"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)

    def test_block_to_block_ordered_list1(self):
        block = "1. Line one of an ordered list.\n2. Line two of an ordered list.\n3. Line three of an ordered list.\n4. Line four of an ordered list."
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1.No space\n2.No space\n3.No space"), BlockType.PARAGRAPH)

    def test_block_to_block_ordered_list2(self):
            block = """1. Line one of an ordered list.
2. Line two of an ordered list.
3. Line three of an ordered list.
4. Line four of an ordered list."""
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
            self.assertEqual(block_to_block_type("1.No space\n2.No space\n3.No space"), BlockType.PARAGRAPH)

def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )


def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

def test_headings(self):
    md = """
# First **Level** Heading

### Third **Level** Heading

###### Sixth **Level** Heading
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><h1>First <b>Level</b> Heading</h1><h3>Third <b>Level</b> Heading</h3><h6>Sixth <b>Level</b> Heading</h6></div>"

    )

def test_quotes(self):
    md = """
> This is a quote
> that spans multiple lines
> and has **inline** stuff
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><blockquote>This is a quote\nthat spans multiple lines\nand has <b>inline</b> stuff</blockquote></div>"
    )
def test_unordered_list(self):
    md = """
- This is an unordered list item
- This is another unordered list item
- This is a third unordered list item
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><ul><li>This is an unordered list item</li><li>This is another unordered list item</li><li>This is a third unordered list item</li></ul></div>"
    )

def test_ordered_list(self):
    md = """
1. This is an ordered list item
2. This is another ordered list item
3. This is a third ordered list item
4. This is a fourth ordered list item
5. This is a fifth ordered list item
6. This is a sixth ordered list item
7. This is a seventh ordered list item
8. This is an eighth ordered list item
9. This is a ninth ordered list item
10. This is a tenth ordered list item
"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><ol><li>This is an ordered list item</li><li>This is another ordered list item</li><li>This is a third ordered list item</li><li>This is a fourth ordered list item</li><li>This is a fifth ordered list item</li><li>This is a sixth ordered list item</li><li>This is a seventh ordered list item</li><li>This is an eighth ordered list item</li><li>This is a ninth ordered list item</li><li>This is a tenth ordered list item</li></ol></div>"
    )
