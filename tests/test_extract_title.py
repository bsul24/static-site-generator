import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        markdown = "# Hello World"

        self.assertEqual(
            extract_title(markdown),
            "Hello World",
        )

    def test_title_with_extra_whitespace(self):
        markdown = "#    My Title    "

        self.assertEqual(
            extract_title(markdown),
            "My Title",
        )

    def test_title_after_other_content(self):
        markdown = "This is an introduction.\n\nSome more content.\n\n# Actual Title"

        self.assertEqual(
            extract_title(markdown),
            "Actual Title",
        )

    def test_title_after_other_headings(self):
        markdown = "## Secondary Heading\n\n### Third Level Heading\n\n# Main Title"

        self.assertEqual(
            extract_title(markdown),
            "Main Title",
        )

    def test_multiple_h1_headings(self):
        markdown = "# First Title\n\nSome content.\n\n# Second Title"

        self.assertEqual(
            extract_title(markdown),
            "First Title",
        )

    def test_title_with_special_characters(self):
        markdown = "# C++, Python & JavaScript: A Guide!"

        self.assertEqual(
            extract_title(markdown),
            "C++, Python & JavaScript: A Guide!",
        )

    def test_title_containing_hash(self):
        markdown = "# Learning C# and #hashtags"

        self.assertEqual(
            extract_title(markdown),
            "Learning C# and #hashtags",
        )

    def test_no_heading(self):
        markdown = "This is a paragraph.\n\nThis is another paragraph."

        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_only_lower_level_headings(self):
        markdown = "## Heading Two\n\n### Heading Three\n\n###### Heading Six"

        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_hash_without_space(self):
        markdown = "#NotAHeading\n\nSome ordinary paragraph text."

        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
