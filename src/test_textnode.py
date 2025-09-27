import unittest

from textnode import TextNode, TextType
from text_to_textnode import split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("", TextType.IMAGE, "./image.png")
        node2 = TextNode("", TextType.IMAGE, "./image.png")
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("INeq", TextType.ITALIC_TEXT)
        node2 = TextNode("INeq", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_ineq2(self):
        node = TextNode("INeq", TextType.ITALIC_TEXT, "./y.jpg")
        node2 = TextNode("INeq", TextType.ITALIC_TEXT, "./y.png")
        self.assertNotEqual(node, node2)

    def test_ineq3(self):
        node = TextNode("INeq", TextType.ITALIC_TEXT, "./y.jpg")
        node2 = TextNode("inEQ", TextType.ITALIC_TEXT, "./y.jpg")
        self.assertNotEqual(node, node2)
    
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_link(self):
        node = TextNode(
            "This is a link pointing [to wikipedia](https://wikipedia.org/), then there is this one which leads [to twitch](https://twitch.tv/)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a link pointing ", TextType.PLAIN_TEXT),
                TextNode("to wikipedia", TextType.LINK, "https://wikipedia.org/"),
                TextNode(", then there is this one which leads ", TextType.PLAIN_TEXT),
                TextNode("to twitch", TextType.LINK, "https://twitch.tv/"),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            result, 
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word and a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )


if __name__ == "__main__":
    unittest.main()