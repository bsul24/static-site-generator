import tempfile
import unittest
from pathlib import Path

from main import copy_static


class TestCopyStatic(unittest.TestCase):
    def setUp(self):
        # Each test gets its own temporary filesystem.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        root = Path(self.temp_dir.name)
        self.source = root / "static"
        self.destination = root / "public"

        self.source.mkdir()

    def write_source_file(self, relative_path, content):
        path = self.source / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def run_copy(self):
        copy_static(
            str(self.source),
            str(self.destination),
        )

    def test_copy_single_file(self):
        self.write_source_file(
            "index.css",
            b"body { color: red; }",
        )

        self.run_copy()

        copied = self.destination / "index.css"

        self.assertTrue(copied.is_file())
        self.assertEqual(
            copied.read_bytes(),
            b"body { color: red; }",
        )

    def test_copy_nested_directories(self):
        self.write_source_file(
            "index.css",
            b"body {}",
        )
        self.write_source_file(
            "images/logo.png",
            b"fake image data",
        )
        self.write_source_file(
            "images/icons/icon.svg",
            b"<svg></svg>",
        )

        self.run_copy()

        self.assertTrue((self.destination / "index.css").is_file())
        self.assertTrue((self.destination / "images/logo.png").is_file())
        self.assertTrue((self.destination / "images/icons/icon.svg").is_file())

        self.assertEqual(
            (self.destination / "images/icons/icon.svg").read_bytes(),
            b"<svg></svg>",
        )

    def test_delete_old_destination_contents(self):
        self.destination.mkdir()

        old_file = self.destination / "old.txt"
        old_file.write_text("This should be removed")

        old_directory = self.destination / "old_folder"
        old_directory.mkdir()
        (old_directory / "old_nested.txt").write_text("Old")

        self.write_source_file(
            "new.txt",
            b"This should exist",
        )

        self.run_copy()

        self.assertFalse(old_file.exists())
        self.assertFalse(old_directory.exists())
        self.assertTrue((self.destination / "new.txt").is_file())

    def test_create_destination_if_missing(self):
        self.write_source_file("test.txt", b"Hello")

        self.assertFalse(self.destination.exists())

        self.run_copy()

        self.assertTrue(self.destination.is_dir())
        self.assertEqual(
            (self.destination / "test.txt").read_bytes(),
            b"Hello",
        )

    def test_copy_empty_directories(self):
        empty_dir = self.source / "empty" / "nested"
        empty_dir.mkdir(parents=True)

        self.run_copy()

        self.assertTrue((self.destination / "empty" / "nested").is_dir())

    def test_copy_binary_file(self):
        binary_data = bytes(range(256))

        self.write_source_file(
            "images/test.bin",
            binary_data,
        )

        self.run_copy()

        self.assertEqual(
            (self.destination / "images/test.bin").read_bytes(),
            binary_data,
        )

    def test_running_twice_replaces_old_contents(self):
        self.write_source_file(
            "first.txt",
            b"First version",
        )

        self.run_copy()

        # Modify the source after the first copy.
        (self.source / "first.txt").unlink()

        self.write_source_file(
            "second.txt",
            b"Second version",
        )

        self.run_copy()

        self.assertFalse((self.destination / "first.txt").exists())
        self.assertEqual(
            (self.destination / "second.txt").read_bytes(),
            b"Second version",
        )

    def test_source_remains_unchanged(self):
        self.write_source_file(
            "images/original.png",
            b"original content",
        )

        self.run_copy()

        original = self.source / "images/original.png"

        self.assertTrue(original.is_file())
        self.assertEqual(
            original.read_bytes(),
            b"original content",
        )


if __name__ == "__main__":
    unittest.main()
