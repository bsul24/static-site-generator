import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_multiple_blocks(self):
        markdown = """# Heading

This is a paragraph with **bold** text.

- First item
- Second item
- Third item"""

        expected = [
            "# Heading",
            "This is a paragraph with **bold** text.",
            "- First item\n- Second item\n- Third item",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_block(self):
        markdown = "This is just one paragraph."

        expected = [
            "This is just one paragraph.",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        markdown = ""

        self.assertEqual(markdown_to_blocks(markdown), [])

    def test_only_whitespace(self):
        markdown = "   \n\n   \n\n   "

        self.assertEqual(markdown_to_blocks(markdown), [])

    def test_excessive_newlines(self):
        markdown = """First paragraph.



Second paragraph.




Third paragraph."""

        expected = [
            "First paragraph.",
            "Second paragraph.",
            "Third paragraph.",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_and_trailing_newlines(self):
        markdown = "\n\n\nFirst paragraph.\n\nSecond paragraph.\n\n\n"

        expected = [
            "First paragraph.",
            "Second paragraph.",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_strip_whitespace_from_blocks(self):
        markdown = "   First paragraph.   \n\n   Second paragraph.   "

        expected = [
            "First paragraph.",
            "Second paragraph.",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_preserve_single_newlines(self):
        markdown = """This is the first line.
This is the second line.
This is the third line."""

        expected = [
            "This is the first line.\n"
            "This is the second line.\n"
            "This is the third line.",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_mixed_markdown_types(self):
        markdown = """# Main Heading

This is a paragraph with **bold**, _italic_, and `code`.

1. First item
2. Second item
3. Third item

> This is a blockquote."""

        expected = [
            "# Main Heading",
            "This is a paragraph with **bold**, _italic_, and `code`.",
            "1. First item\n2. Second item\n3. Third item",
            "> This is a blockquote.",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_preserve_internal_whitespace(self):
        markdown = """First line
  Indented second line
Third line

Next paragraph"""

        expected = [
            "First line\n  Indented second line\nThird line",
            "Next paragraph",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)
