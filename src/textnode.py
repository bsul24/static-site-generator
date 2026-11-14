import re
from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("invalid URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("invalid URL")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("unknown text type")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("invalid Markdown syntax")

        result_nodes = []
        is_text_node = True

        for text in split_text:
            if text:
                if is_text_node:
                    result_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    result_nodes.append(TextNode(text, text_type))

            is_text_node = not is_text_node

        new_nodes.extend(result_nodes)

    return new_nodes


def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        result_nodes = []
        cur = 0
        for img in images:
            start_index = node.text.find(f"![{img[0]}]({img[1]})", cur)
            if start_index > cur:
                result_nodes.append(TextNode(node.text[cur:start_index], TextType.TEXT))
            result_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))

            cur = start_index + len(img[0]) + len(img[1]) + 5

        if cur < len(node.text):
            result_nodes.append(TextNode(node.text[cur:], TextType.TEXT))

        new_nodes.extend(result_nodes)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        result_nodes = []
        cur = 0
        for link in links:
            start_index = node.text.find(f"[{link[0]}]({link[1]})", cur)
            if start_index > cur:
                result_nodes.append(TextNode(node.text[cur:start_index], TextType.TEXT))
            result_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            cur = start_index + len(link[0]) + len(link[1]) + 4

        if cur < len(node.text):
            result_nodes.append(TextNode(node.text[cur:], TextType.TEXT))

        new_nodes.extend(result_nodes)

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:

    node_list = [TextNode(text, TextType.TEXT)]
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(node_list, "**", TextType.BOLD),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
