import unittest

from block import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockTest(unittest.TestCase):
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
    
    def test_markdown_to_blocks_excess_blanks(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a sample list
- another item in the list

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a sample list\n- another item in the list",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type_paragraph(self):
        text = "helo, this is a normal paragraph\nnothing personal"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_heading(self):
        headings = [
            "# This is a heading",
            "## Another heading",
            "### don't forget about me",
            "#### dw i wont",
            "##### aww u so cutie patotie",
            "###### <3",
        ]
        for heading in headings:
            result = block_to_block_type(heading)
            self.assertEqual(result, BlockType.HEADING)
    
    def test_block_to_block_type_code(self):
        text = "```codeeee;\n#include <iostream>\n\nint main() \{\nstd::cout << \"Hello, world!\";\n\}```"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        text = "> quoting the blocks\n> blocking the quotes"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_block_to_block_type_unordered_list(self):
        text = "- \n- sadlif \n- stalactite\n- skewered"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        text = "1. \n2. sadlif \n3. stalactite\n4. skewered"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.ORDERED_LIST)

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