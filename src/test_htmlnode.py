import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_textnode import split_nodes_image, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode_to_htmlnode import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "Haloka, ez itt a kutya kozpont", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html2(self):
        node = HTMLNode("a", None, None, { "href": "https://www.google.com", "target": "_blank" })
        result = node.props_to_html()
        self.assertEqual(result,  " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html3(self):
        children = [
            HTMLNode("li", "bug", None, None),
            HTMLNode("li", "tr", None, None),
            HTMLNode("li", "task", None, None),
            HTMLNode("li", "documentation", None, None),
        ]
        node = HTMLNode("ul", None, children, None)
        result = node.props_to_html()
        self.assertEqual(result, "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        result = node.to_html()
        self.assertEqual(result, "<p>This is a paragraph of text.</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        result = node.to_html()
        self.assertEqual(result, "<a href=\"https://www.google.com\">Click me!</a>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        node = ParentNode("div", [], {"align": "center"})
        with self.assertRaises(ValueError):
            res = node.to_html()

    def test_to_html_with_no_tag(self):
        leaf_node = LeafNode("p", "Hablatyaham")
        node = ParentNode("", [leaf_node])
        with self.assertRaises(ValueError):
            res = node.to_html()


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text2(self):
        node = TextNode("This is a bold node", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_text3(self):
        node = TextNode("This is an italic node", TextType.ITALIC_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_text4(self):
        node = TextNode("This is a code node", TextType.CODE_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_text5(self):
        node = TextNode("This is a link node", TextType.LINK, "https://boot.dev/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://boot.dev/"})

    def test_text6(self):
        node = TextNode("image about a unicorn", TextType.IMAGE, "./image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "./image.png", "alt": "image about a unicorn"})

class TestSplitNodesDelimeter(unittest.TestCase):
    def test_valid1(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, 
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" word", TextType.PLAIN_TEXT),
            ]
        )

class TestExtractors(unittest.TestCase):
    def test_extract_md_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_md_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(
            text,
        )
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


if __name__ == "__main__":
    unittest.main()