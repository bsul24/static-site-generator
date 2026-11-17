import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

from main import generate_pages_recursive


class TestGeneratePagesRecursive(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        root = Path(self.temp_dir.name)
        self.content = root / "content"
        self.public = root / "public"
        self.template = str(root / "template.html")

        self.content.mkdir()

    def add_file(self, relative_path):
        path = self.content / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Test Page", encoding="utf-8")

    def test_nested_markdown_files(self):
        self.add_file("index.md")
        self.add_file("blog/tom/index.md")
        self.add_file("blog/other/post.md")

        with patch("main.generate_page") as mock_generate:
            generate_pages_recursive(
                str(self.content),
                self.template,
                str(self.public),
            )

        expected = [
            call(
                str(self.content / "index.md"),
                self.template,
                str(self.public / "index.html"),
            ),
            call(
                str(self.content / "blog/tom/index.md"),
                self.template,
                str(self.public / "blog/tom/index.html"),
            ),
            call(
                str(self.content / "blog/other/post.md"),
                self.template,
                str(self.public / "blog/other/post.html"),
            ),
        ]

        self.assertCountEqual(
            mock_generate.call_args_list,
            expected,
        )

    def test_ignores_non_markdown_files(self):
        self.add_file("index.md")
        self.add_file("notes.txt")
        self.add_file("blog/image.png")

        with patch("main.generate_page") as mock_generate:
            generate_pages_recursive(
                str(self.content),
                self.template,
                str(self.public),
            )

        mock_generate.assert_called_once_with(
            str(self.content / "index.md"),
            self.template,
            str(self.public / "index.html"),
        )

    def test_empty_directories(self):
        (self.content / "blog/empty").mkdir(parents=True)

        with patch("main.generate_page") as mock_generate:
            generate_pages_recursive(
                str(self.content),
                self.template,
                str(self.public),
            )

        mock_generate.assert_not_called()

    def test_filename_with_multiple_dots(self):
        self.add_file("blog/my.first.post.md")

        with patch("main.generate_page") as mock_generate:
            generate_pages_recursive(
                str(self.content),
                self.template,
                str(self.public),
            )

        mock_generate.assert_called_once_with(
            str(self.content / "blog/my.first.post.md"),
            self.template,
            str(self.public / "blog/my.first.post.html"),
        )


if __name__ == "__main__":
    unittest.main()
