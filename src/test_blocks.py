import unittest
from blocks import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    
    # --- Headings ---
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block_h3 = "### This is a heading 3"
        self.assertEqual(block_to_block_type(block_h3), BlockType.HEADING)

    def test_block_to_block_type_invalid_heading(self):
        # Missing the space after the hash
        block = "#This is actually a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Code Blocks ---
    def test_block_to_block_type_code(self):
        block = "```\nprint('Hello World')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    # --- Quote Blocks ---
    def test_block_to_block_type_quote(self):
        block = "> This is a quote\n> spanning multiple lines\n> flawlessly."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_broken_quote(self):
        # The second line forgets the > symbol
        block = "> This quote starts strong\nbut forgets to keep quoting\n> and tries to recover."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Unordered Lists ---
    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.U_LIST)

    def test_block_to_block_type_broken_unordered_list(self):
        # Missing the space after the dash
        block = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Ordered Lists ---
    def test_block_to_block_type_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.O_LIST)

    def test_block_to_block_type_broken_ordered_list(self):
        # Skips the number 2!
        block = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Starts with the wrong number
        block_wrong_start = "2. First item"
        self.assertEqual(block_to_block_type(block_wrong_start), BlockType.PARAGRAPH)

    # --- Paragraphs ---
    def test_block_to_block_type_paragraph(self):
        block = "This is just a standard paragraph of text.\nIt has multiple lines, but no special characters."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()