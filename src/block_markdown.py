import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    current_lines = []
    inside_code_block = False

    for line in markdown.splitlines():
        if line == "```":
            if inside_code_block:
                current_lines.append(line)
                blocks.append("\n".join(current_lines))
                current_lines = []
                inside_code_block = False

            else:
                if current_lines:
                    blocks.append("\n".join(current_lines).strip())

                current_lines = [line]
                inside_code_block = True

        elif not inside_code_block and not line.strip():
            if current_lines:
                blocks.append("\n".join(current_lines).strip())
                current_lines = []

        else:
            current_lines.append(line)

    if inside_code_block:
        raise ValueError("Unclosed fenced code block")

    if current_lines:
        blocks.append("\n".join(current_lines).strip())

    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.fullmatch(r"#{1,6} .+", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    lines = block.split("\n")
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            break
        if i == len(lines) - 1:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    all_nodes = []
    for block in blocks:
        b_type = block_to_block_type(block)
        if b_type == BlockType.HEADING:
            split_text = block.split(" ", 1)
            tag = f"h{len(split_text[0])}"
            text = split_text[1]
            children = text_to_children(text)
            new_node = ParentNode(tag, children)
            all_nodes.append(new_node)
        elif b_type == BlockType.CODE:
            text = block[4:-3]
            text_node = TextNode(text, TextType.CODE)
            child_node = text_node_to_html_node(text_node)
            all_nodes.append(ParentNode("pre", [child_node]))
        elif b_type == BlockType.QUOTE:
            tag = "blockquote"
            lines = block.split("\n")
            lines_cleaned = []
            for line in lines:
                if len(line) < 2:
                    lines_cleaned.append("")
                elif line[1] == " ":
                    lines_cleaned.append(line[2:])
                else:
                    lines_cleaned.append(line[1:])
            text = " ".join(lines_cleaned)
            children = text_to_children(text)
            new_node = ParentNode(tag, children)
            all_nodes.append(new_node)
        elif b_type == BlockType.UNORDERED_LIST:
            list_items = [line[2:] for line in block.split("\n")]
            nodes = []

            for item in list_items:
                tag = "li"
                children = text_to_children(item)
                new_node = ParentNode(tag, children)
                nodes.append(new_node)

            all_nodes.append(ParentNode("ul", nodes))

        elif b_type == BlockType.ORDERED_LIST:
            list_items = block.split("\n")
            list_items_text = []
            nodes = []

            for item in list_items:
                item_minus_number = item.split(". ", 1)[1]
                list_items_text.append(item_minus_number)

            for item in list_items_text:
                tag = "li"
                children = text_to_children(item)
                new_node = ParentNode(tag, children)
                nodes.append(new_node)

            all_nodes.append(ParentNode("ol", nodes))

        else:
            text = " ".join(block.split("\n"))
            children = text_to_children(text)
            all_nodes.append(ParentNode("p", children))

    return ParentNode("div", all_nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
