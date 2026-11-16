import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from main import generate_page


class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        root = Path(self.temp_dir.name)

        self.markdown_path = root / "content" / "post.md"
        self.template_path = root / "template.html"
        self.output_path = root / "public" / "blog" / "index.html"

        self.markdown_path.parent.mkdir(parents=True)

    def write_files(self, markdown, template=None):
        if template is None:
            template = (
                "<html>"
                "<head><title>{{ Title }}</title></head>"
                "<body>{{ Content }}</body>"
                "</html>"
            )

        self.markdown_path.write_text(markdown, encoding="utf-8")

        self.template_path.write_text(template, encoding="utf-8")

    def generate(self):
        # Suppress the normal generation log during tests.
        output = StringIO()

        with redirect_stdout(output):
            generate_page(
                str(self.markdown_path),
                str(self.template_path),
                str(self.output_path),
            )

        return output.getvalue()

    def read_output(self):
        return self.output_path.read_text(encoding="utf-8")

    # -------------------------
    # Basic generation
    # -------------------------

    def test_generate_simple_page(self):
        self.write_files("# My Page\n\nHello world.")

        self.generate()

        expected = (
            "<html>"
            "<head><title>My Page</title></head>"
            "<body>"
            "<div>"
            "<h1>My Page</h1>"
            "<p>Hello world.</p>"
            "</div>"
            "</body>"
            "</html>"
        )

        self.assertEqual(self.read_output(), expected)

    # -------------------------
    # Directory creation
    # -------------------------

    def test_creates_missing_directories(self):
        self.write_files("# My Page")

        self.assertFalse(self.output_path.parent.exists())

        self.generate()

        self.assertTrue(self.output_path.is_file())
        self.assertTrue(self.output_path.parent.is_dir())

    # -------------------------
    # Overwriting existing files
    # -------------------------

    def test_overwrites_existing_output(self):
        self.write_files("# New Title")

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.output_path.write_text(
            "This is old content",
            encoding="utf-8",
        )

        self.generate()

        html = self.read_output()

        self.assertIn("<title>New Title</title>", html)
        self.assertNotIn("This is old content", html)

    # -------------------------
    # Placeholder replacement
    # -------------------------

    def test_replaces_all_placeholders(self):
        template = (
            "<title>{{ Title }}</title><h2>{{ Title }}</h2>{{ Content }}{{ Content }}"
        )

        self.write_files("# My Page", template)

        self.generate()

        html = self.read_output()

        self.assertEqual(html.count("My Page"), 4)
        self.assertEqual(html.count("<div>"), 2)
        self.assertNotIn("{{ Title }}", html)
        self.assertNotIn("{{ Content }}", html)

    # -------------------------
    # Markdown conversion
    # -------------------------

    def test_converts_multiple_markdown_types(self):
        markdown = (
            "# My Article\n\n"
            "This has **bold** and _italic_ text.\n\n"
            "- First item\n"
            "- Second item"
        )

        self.write_files(markdown)

        self.generate()

        html = self.read_output()

        self.assertIn("<h1>My Article</h1>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn(
            "<ul><li>First item</li><li>Second item</li></ul>",
            html,
        )

    # -------------------------
    # Correct title selection
    # -------------------------

    def test_uses_first_h1_for_title(self):
        markdown = "## Secondary Heading\n\n# Correct Title\n\n# Another Title"

        self.write_files(markdown)

        self.generate()

        html = self.read_output()

        self.assertIn(
            "<title>Correct Title</title>",
            html,
        )
        self.assertNotIn(
            "<title>Another Title</title>",
            html,
        )

    # -------------------------
    # Missing title
    # -------------------------

    def test_raises_without_h1(self):
        self.write_files("## Only an H2\n\nSome paragraph text.")

        with self.assertRaises(Exception):
            self.generate()

        self.assertFalse(self.output_path.exists())

    # -------------------------
    # Source files remain unchanged
    # -------------------------

    def test_does_not_modify_input_files(self):
        markdown = "# Original Title\n\nSome text."
        template = "<title>{{ Title }}</title>{{ Content }}"

        self.write_files(markdown, template)

        self.generate()

        self.assertEqual(
            self.markdown_path.read_text(encoding="utf-8"),
            markdown,
        )
        self.assertEqual(
            self.template_path.read_text(encoding="utf-8"),
            template,
        )


if __name__ == "__main__":
    unittest.main()
