import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
