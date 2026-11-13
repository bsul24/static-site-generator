import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    text_node_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("good", TextType.ITALIC, "www.hi.com")
        node2 = TextNode("bad", TextType.ITALIC, "www.hi.com")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("text node", TextType.TEXT, None)
        node2 = TextNode("text node", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("text node", TextType.TEXT, "www.hello.com")
        node2 = TextNode("text node", TextType.LINK, "www.hello.com")
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


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


if __name__ == "__main__":
    unittest.main()
