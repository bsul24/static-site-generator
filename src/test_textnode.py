import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()
