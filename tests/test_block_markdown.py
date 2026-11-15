import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


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
            """This is the first line.
This is the second line.
This is the third line."""
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


class TestBlockToBlockType(unittest.TestCase):
    # -------------------------
    # Headings
    # -------------------------

    def test_valid_headings(self):
        for level in range(1, 7):
            block = "#" * level + " Heading"

            with self.subTest(level=level):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.HEADING,
                )

    def test_headings_with_different_content(self):
        blocks = [
            "# Hello, world!",
            "## Heading with **bold** text",
            "### Heading with _italic_ text",
            "#### Heading with 123 numbers",
            "##### Heading with [a link](https://boot.dev)",
            "###### Final heading level",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.HEADING,
                )

    def test_invalid_headings(self):
        blocks = [
            "#No space",
            "##No space",
            "####### Too many hashes",
            "######## Even more hashes",
            "Normal text # Heading",
            "##Heading without space",
            "##\tHeading with tab instead of space",
            "# Heading\nAnother line",
            "## Heading\nParagraph below",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    # -------------------------
    # Code blocks
    # -------------------------

    def test_single_line_code_block(self):
        block = "```\nprint('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_multiline_code_block(self):
        block = """```
def hello():
    print("Hello, world!")

hello()
```"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_code_block_with_blank_lines(self):
        block = "```\nx = 10\n\nprint(x)\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_invalid_code_blocks(self):
        blocks = [
            "``print('hello')``",
            "```print('hello')```",
            "```python\nprint('hello')\n```",
            "```\nprint('hello')",
            "```\nprint('hello')\n``",
            "Some text\n```\nprint('hello')\n```",
            "```\nprint('hello')\n```extra",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    # -------------------------
    # Quote blocks
    # -------------------------

    def test_single_line_quote(self):
        block = "> This is a quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_without_space(self):
        block = ">This is a quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_multiline_quote(self):
        block = """> First line
> Second line
> Third line"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_with_mixed_spacing(self):
        block = """> First line
>Second line
> Third line"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quotes(self):
        blocks = [
            "> First line\nSecond line",
            "First line\n> Second line",
            "> First line\n> Second line\nThird line",
            "Not a quote",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    # -------------------------
    # Unordered lists
    # -------------------------

    def test_single_unordered_item(self):
        block = "- First item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_multiline_unordered_list(self):
        block = """- First item
- Second item
- Third item"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_with_formatting(self):
        block = """- **Bold item**
- _Italic item_
- Item with `code`
- [Link](https://boot.dev)"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_lists(self):
        blocks = [
            "-First item",
            "-- First item",
            "* First item\n* Second item",
            "- First item\nSecond item",
            "- First item\n-Second item",
            "- First item\n* Second item",
            "First item\n- Second item",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    # -------------------------
    # Ordered lists
    # -------------------------

    def test_single_ordered_item(self):
        block = "1. First item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_multiline_ordered_list(self):
        block = """1. First item
2. Second item
3. Third item"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_long_ordered_list(self):
        block = "\n".join(f"{i}. Item {i}" for i in range(1, 13))

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_with_formatting(self):
        block = """1. **Bold item**
2. _Italic item_
3. Item with `code`
4. [Link](https://boot.dev)"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_wrong_start(self):
        blocks = [
            "0. First item",
            "2. First item",
            "3. First item\n4. Second item",
            "10. First item",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_ordered_list_wrong_sequence(self):
        blocks = [
            "1. First\n3. Second",
            "1. First\n1. Second",
            "1. First\n2. Second\n4. Fourth",
            "1. First\n2. Second\n2. Third",
            "1. First\n2. Second\n10. Tenth",
            "1. First\n3. Third\n2. Second",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_ordered_list_invalid_format(self):
        blocks = [
            "1.First item",
            "1) First item",
            "1- First item",
            "1 First item",
            "1. First item\n2.Second item",
            "1. First item\n2) Second item",
            "1. First item\nSecond item",
            "1. First item\n- Second item",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    # -------------------------
    # Paragraphs
    # -------------------------

    def test_plain_paragraph(self):
        block = "This is a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_multiline_paragraph(self):
        block = """This is the first line.
This is the second line.
This is the third line."""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraph_with_inline_markdown(self):
        block = (
            "This paragraph has **bold**, _italic_, "
            "`code`, and [a link](https://boot.dev)."
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraph_with_markdown_characters(self):
        blocks = [
            "This is a # character in text",
            "This has `backticks` inside",
            "The price is > $100",
            "Use - for subtraction",
            "A paragraph with **bold** formatting",
        ]

        for block in blocks:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_empty_block(self):
        self.assertEqual(
            block_to_block_type(""),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_double_digit(self):
        block = "\n".join(f"{i}. Item {i}" for i in range(1, 16))

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_invalid_double_digit(self):
        block = "\n".join(f"{i}. Item {i}" for i in range(1, 10))
        block += "\n11. Item 11\n12. Item 12"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
