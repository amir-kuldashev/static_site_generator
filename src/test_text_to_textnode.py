import unittest
from textnode import TextNode, TextType
from text_to_textnode import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_kitchen_sink(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text with absolutely no formatting."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is just plain text with absolutely no formatting.", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiples(self):
        text = "This has **bold** and **another bold** and _italic_ and _another italic_"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("another italic", TextType.ITALIC),
            ],
            nodes,
        )

    def test_text_to_textnodes_only_formatting(self):
        # A sneaky edge case: no standard text at all
        text = "**bold**_italic_`code`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()