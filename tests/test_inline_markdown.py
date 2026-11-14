import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)

        result = split_nodes_delimiter([node], "*", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_code(self):
        node = TextNode("Use `print('hello')` here", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("print('hello')", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode(
            "This has **bold one** and **bold two**.",
            TextType.TEXT,
        )

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold two", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_no_delimiters(self):
        node = TextNode("Just plain text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [node])

    def test_preserve_existing_nodes(self):
        nodes = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("This is *italic*", TextType.TEXT),
            TextNode("Existing code", TextType.CODE),
        ]

        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

        expected = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("Existing code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First **bold** section", TextType.TEXT),
            TextNode("Second **bold** section", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" section", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" section", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        node = TextNode("This is **unfinished", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_unmatched_closing_delimiter(self):
        node = TextNode("This is unfinished**", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delimiters_at_boundaries(self):
        node = TextNode("**bold**", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("bold", TextType.BOLD),
        ]

        self.assertEqual(result, expected)

    def test_empty_input(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)

        self.assertEqual(result, [])

    def test_non_text_node_with_delimiters(self):
        node = TextNode("**already bold**", TextType.BOLD)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [node])

    def test_consecutive_delimiters(self):
        node = TextNode("This is **** text", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_adjacent_formatted_sections(self):
        node = TextNode("**first****second**", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("first", TextType.BOLD),
            TextNode("second", TextType.BOLD),
        ]

        self.assertEqual(result, expected)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "Here is ![a cat](https://example.com/cat.png)"
        expected = [("a cat", "https://example.com/cat.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "First ![cat](cat.png) and second ![dog](dog.jpg)"
        expected = [
            ("cat", "cat.png"),
            ("dog", "dog.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This is plain text with no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_ignore_regular_links(self):
        text = "Visit [Google](https://google.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_empty_alt_text(self):
        text = "![](image.png)"
        expected = [("", "image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_special_characters(self):
        text = "![My cool image!](https://example.com/a-b_c.png)"
        expected = [("My cool image!", "https://example.com/a-b_c.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_unclosed_image(self):
        text = "![cat](cat.png"
        self.assertEqual(extract_markdown_images(text), [])

    def test_nested_brackets(self):
        text = "![A [cute] cat](cat.png)"
        self.assertEqual(extract_markdown_images(text), [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "Visit [Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "Visit [Google](https://google.com) or [GitHub](https://github.com)"
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "This is plain text without links."
        self.assertEqual(extract_markdown_links(text), [])

    def test_ignore_images(self):
        text = "Here is ![cat](cat.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_mixed_links_and_images(self):
        text = (
            "Visit [Google](https://google.com), "
            "see ![cat](cat.png), "
            "or visit [GitHub](https://github.com)"
        )
        expected = [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_link_text(self):
        text = "[](https://example.com)"
        expected = [("", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_unclosed_link(self):
        text = "[Google](https://google.com"
        self.assertEqual(extract_markdown_links(text), [])

    def test_nested_brackets(self):
        text = "[A [nested] link](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_parentheses_in_url(self):
        text = "[Docs](https://example.com/a(b))"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "This is an ![image](https://example.com/image.png) in text",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://example.com/image.png",
            ),
            TextNode(" in text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_images(self):
        node = TextNode(
            "First ![cat](cat.png) and second ![dog](dog.png) end",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and second ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
            TextNode(" end", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_no_images(self):
        node = TextNode(
            "Just some regular text.",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        self.assertEqual(result, [node])

    def test_image_at_beginning(self):
        node = TextNode(
            "![cat](cat.png) is a picture of a cat",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" is a picture of a cat", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_image_at_end(self):
        node = TextNode(
            "Here is a cat: ![cat](cat.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        expected = [
            TextNode("Here is a cat: ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ]

        self.assertEqual(result, expected)

    def test_only_image(self):
        node = TextNode(
            "![cat](cat.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ]

        self.assertEqual(result, expected)

    def test_adjacent_images(self):
        node = TextNode(
            "![cat](cat.png)![dog](dog.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode("dog", TextType.IMAGE, "dog.png"),
        ]

        self.assertEqual(result, expected)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First ![cat](cat.png)", TextType.TEXT),
            TextNode("Some regular text", TextType.TEXT),
            TextNode("Second ![dog](dog.png)", TextType.TEXT),
        ]

        result = split_nodes_image(nodes)

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode("Some regular text", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
        ]

        self.assertEqual(result, expected)

    def test_preserve_existing_formatted_nodes(self):
        nodes = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("An ![image](image.png)", TextType.TEXT),
            TextNode("Already italic", TextType.ITALIC),
        ]

        result = split_nodes_image(nodes)

        expected = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("An ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "image.png"),
            TextNode("Already italic", TextType.ITALIC),
        ]

        self.assertEqual(result, expected)

    def test_ignore_regular_links(self):
        node = TextNode(
            "Visit [Google](https://google.com) and see ![cat](cat.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        expected = [
            TextNode(
                "Visit [Google](https://google.com) and see ",
                TextType.TEXT,
            ),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ]

        self.assertEqual(result, expected)

    def test_empty_input(self):
        result = split_nodes_image([])

        self.assertEqual(result, [])


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "This is a [link](https://example.com) in text",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_links(self):
        node = TextNode(
            "Visit [Google](https://google.com) and [GitHub](https://github.com) today",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
            TextNode(" today", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_no_links(self):
        node = TextNode(
            "Just some regular text.",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        self.assertEqual(result, [node])

    def test_link_at_beginning(self):
        node = TextNode(
            "[Google](https://google.com) is a search engine",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" is a search engine", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_link_at_end(self):
        node = TextNode(
            "Visit [Google](https://google.com)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]

        self.assertEqual(result, expected)

    def test_only_link(self):
        node = TextNode(
            "[Google](https://google.com)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]

        self.assertEqual(result, expected)

    def test_adjacent_links(self):
        node = TextNode(
            "[Google](https://google.com)[GitHub](https://github.com)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]

        self.assertEqual(result, expected)

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("First [Google](https://google.com)", TextType.TEXT),
            TextNode("Some regular text", TextType.TEXT),
            TextNode("Second [GitHub](https://github.com)", TextType.TEXT),
        ]

        result = split_nodes_link(nodes)

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode("Some regular text", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]

        self.assertEqual(result, expected)

    def test_preserve_existing_formatted_nodes(self):
        nodes = [
            TextNode("Already bold", TextType.BOLD),
            TextNode(
                "Visit [Google](https://google.com)",
                TextType.TEXT,
            ),
            TextNode("Already italic", TextType.ITALIC),
        ]

        result = split_nodes_link(nodes)

        expected = [
            TextNode("Already bold", TextType.BOLD),
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode("Already italic", TextType.ITALIC),
        ]

        self.assertEqual(result, expected)

    def test_ignore_images(self):
        node = TextNode(
            "See ![cat](cat.png) and visit [Google](https://google.com)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        expected = [
            TextNode(
                "See ![cat](cat.png) and visit ",
                TextType.TEXT,
            ),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]

        self.assertEqual(result, expected)

    def test_empty_input(self):
        result = split_nodes_link([])

        self.assertEqual(result, [])

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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_identical_images(self):
        node = TextNode(
            "![cat](cat.png) and ![cat](cat.png)",
            TextType.TEXT,
        )

        result = split_nodes_image([node])

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ]

        self.assertEqual(result, expected)

    def test_identical_links(self):
        node = TextNode(
            "[Google](https://google.com) and [Google](https://google.com)",
            TextType.TEXT,
        )

        result = split_nodes_link([node])

        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]

        self.assertEqual(result, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text."

        expected = [
            TextNode("This is plain text.", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold(self):
        text = "This is **bold** text."

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic(self):
        text = "This is _italic_ text."

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_code(self):
        text = "Use `print('hello')` to print."

        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("print('hello')", TextType.CODE),
            TextNode(" to print.", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "Here is ![a cat](cat.png) for you."

        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("a cat", TextType.IMAGE, "cat.png"),
            TextNode(" for you.", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "Visit [Google](https://google.com) today."

        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" today.", TextType.TEXT),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_all_types(self):
        text = (
            "This is **text** with an _italic_ word "
            "and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_adjacent_formatted_text(self):
        text = "**bold**_italic_`code`"

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_same_format(self):
        text = "**first** and **second** and **third**"

        expected = [
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("third", TextType.BOLD),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_images_and_links(self):
        text = (
            "![cat](cat.png) and [Google](https://google.com) "
            "and ![dog](dog.png) and [GitHub](https://github.com)"
        )

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "dog.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_repeated_identical_links(self):
        text = "[Google](https://google.com) and [Google](https://google.com)"

        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_repeated_identical_images(self):
        text = "![cat](cat.png) and ![cat](cat.png)"

        expected = [
            TextNode("cat", TextType.IMAGE, "cat.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "cat.png"),
        ]

        self.assertEqual(text_to_textnodes(text), expected)

    def test_unmatched_bold_delimiter(self):
        text = "This is **unfinished bold text"

        with self.assertRaises(ValueError):
            text_to_textnodes(text)
