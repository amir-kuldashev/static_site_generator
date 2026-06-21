import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_nodes_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_split_nodes_multiple(self):
        node = TextNode("This has **two** bold **words** inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" bold ", TextType.TEXT),
                TextNode("words", TextType.BOLD),
                TextNode(" inside", TextType.TEXT),
            ]
        )

    def test_split_nodes_no_delimiters(self):
        node = TextNode("Just a normal sentence with no formatting.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Just a normal sentence with no formatting.", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiters_at_edges(self):
        node = TextNode("*Italic at the start* and *italic at the end*", TextType.TEXT)
        # Note: If your implementation skips empty strings, the start/end might just be the italic node.
        # This test assumes empty strings at the edges might be dropped by your implementation.
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Italic at the start", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic at the end", TextType.ITALIC),
            ]
        )

    def test_split_nodes_unmatched_delimiter(self):
        node = TextNode("This is a **broken bold string", TextType.TEXT)
        # We use a context manager to check if the specific Exception is raised
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_ignores_non_text_nodes(self):
        nodes = [
            TextNode("Normal text ", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode(" more text with `code`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Normal text ", TextType.TEXT),
                TextNode("Already bold", TextType.BOLD),  # Should be untouched
                TextNode(" more text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ]
        )

if __name__ == "__main__":
    unittest.main()