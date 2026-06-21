import unittest
import re
from extract_markdown import extract_markdown_images, extract_markdown_links, \
    split_nodes_image,split_nodes_link 
from textnode import TextNode, TextType
from extract_markdown import markdown_to_blocks

class TestMarkdownExtraction(unittest.TestCase):

    # --- Tests for extract_markdown_images ---

    def test_extract_images_standard(self):
        text = "Here is a picture ![dog](https://example.com/dog.png) for you."
        self.assertEqual(
            extract_markdown_images(text),
            [("dog", "https://example.com/dog.png")]
        )

    def test_extract_images_multiple(self):
        text = "Look at ![cat](cat.jpg) and ![bird](bird.png)!"
        self.assertEqual(
            extract_markdown_images(text),
            [("cat", "cat.jpg"), ("bird", "bird.png")]
        )

    def test_extract_images_no_images(self):
        text = "This text has absolutely no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_images_ignores_links(self):
        text = "This has a [normal link](https://boot.dev), not an image."
        self.assertEqual(extract_markdown_images(text), [])

    # --- Tests for extract_markdown_links ---

    def test_extract_links_standard(self):
        text = "Check out [Boot.dev](https://boot.dev) for python."
        self.assertEqual(
            extract_markdown_links(text),
            [("Boot.dev", "https://boot.dev")]
        )

    def test_extract_links_multiple(self):
        text = "Go to [Google](https://google.com) or [Bing](https://bing.com)."
        self.assertEqual(
            extract_markdown_links(text),
            [("Google", "https://google.com"), ("Bing", "https://bing.com")]
        )

    def test_extract_links_no_links(self):
        text = "This text has absolutely no links."
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_links_ignores_images(self):
        # THIS IS THE BIG ONE! Tests the negative lookbehind.
        text = "This is an ![image](image.jpg), it should NOT be caught as a link."
        self.assertEqual(extract_markdown_links(text), [])

    # --- The Ultimate Combo Test ---

    def test_extract_mixed_content(self):
        text = "Here is a [link](https://url.com) and an ![image](img.png) and another [link2](https://url2.com)."
        
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://url.com"), ("link2", "https://url2.com")]
        )
        
        self.assertEqual(
            extract_markdown_images(text),
            [("image", "img.png")]
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just some plain text without any images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_at_start_and_end(self):
        node = TextNode(
            "![start](https://start.com/img.png) some text ![end](https://end.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://start.com/img.png"),
                TextNode(" some text ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://end.com/img.png"),
            ],
            new_nodes,
        )

    def test_split_images_ignores_links(self):
        node = TextNode("This has a [link](https://boot.dev) not an image.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


    # ---------------------------------------------------------
    # TESTS FOR split_nodes_link
    # ---------------------------------------------------------

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Just some plain text without any links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_at_start_and_end(self):
        node = TextNode(
            "[first](https://first.com) in the middle [last](https://last.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://first.com"),
                TextNode(" in the middle ", TextType.TEXT),
                TextNode("last", TextType.LINK, "https://last.com"),
            ],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        # THIS IS THE MOST IMPORTANT TEST!
        # It ensures your negative lookbehind regex (?<!\!) is working
        node = TextNode("This has an ![image](https://i.imgur.com/zjjcJKZ.png) not a link.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    
    # ---------------------------------------------------------
    # TESTS FOR MULTIPLE/MIXED NODES
    # ---------------------------------------------------------

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("Here is [link1](https://1.com)", TextType.TEXT),
            TextNode("Already a link", TextType.LINK, "https://2.com"),
            TextNode("Here is [link3](https://3.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://1.com"),
                TextNode("Already a link", TextType.LINK, "https://2.com"),
                TextNode("Here is ", TextType.TEXT),
                TextNode("link3", TextType.LINK, "https://3.com"),
            ],
            new_nodes,
        )
    def test_markdown_to_blocks_standard(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        # Testing if it properly drops empty blocks caused by multiple blank lines
        md = """
This is block one.



This is block two after three blank lines.





This is block three.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is block one.",
                "This is block two after three blank lines.",
                "This is block three.",
            ],
        )

    def test_markdown_to_blocks_trailing_whitespace(self):
        # Testing if it correctly strips spaces from the beginning and end of blocks
        md = "   \n  # Heading with spaces  \n\n   Paragraph with spaces   \n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with spaces",
                "Paragraph with spaces",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        # Testing a completely empty string (or just newlines/spaces)
        md = "    \n\n   \n \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    
    
    
if __name__ == "__main__":
    unittest.main()