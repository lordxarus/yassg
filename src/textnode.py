from enum import Enum

import sys

sys.path += ["src"]

from htmlnode import HTMLNode
from leafnode import LeafNode

"""
Represents an "interface," so to speak, between the Markdown and HTML representations 
"""


class TextType(Enum):
    BOLD = 0
    TEXT = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5


class TextNode:
    text: str
    type: TextType
    url: str | None

    def __init__(self, text: str, type: TextType, url: str | None = None):
        self.text = text
        self.type = type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.type == other.type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.type.name}, {self.url})"


# TODO: make this a method on TextNode?
def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            assert text_node.url is not None
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            assert text_node.url is not None
            return LeafNode("img", "", {"alt": text_node.text, "src": text_node.url})
        case _:
            raise ValueError(f"invalid TextType: {text_node.type.name}")


# TODO: nested elements e.g: This is an _italic and **bold** word_.
def split_nodes_delimited(
    old_nodes: list[TextNode], new_type: TextType, delimiter: str | None = None
) -> list[TextNode]:
    # Maybe belongs in TextType? Maybe use __attr__
    default_delims = {
        TextType.BOLD: "*",
        TextType.ITALIC: "_",
        TextType.CODE: "`",
    }
    if new_type == TextType.TEXT:
        return old_nodes
    if delimiter is None:
        try:
            delimiter = default_delims[new_type]
        except KeyError:
            raise ValueError("no delimiter given and no known default")

    out: list[TextNode] = []
    for node in old_nodes:
        if node.type is not TextType.TEXT:
            # TODO: Maybe raise an exception here instead?
            return [node]
        last_slc_end_idx = -1
        is_in_delimiter = False
        for i, c in enumerate(node.text):
            if c == delimiter:
                if is_in_delimiter:
                    slc = node.text[last_slc_end_idx + 1 : i + 1].strip(delimiter)
                    out.append(TextNode(slc, new_type))
                    last_slc_end_idx = i
                    is_in_delimiter = False
                else:
                    if i != 0:
                        slc = node.text[last_slc_end_idx + 1 : i]
                        out.append(TextNode(slc, TextType.TEXT))
                        last_slc_end_idx = i - 1
                    is_in_delimiter = True
            elif i + 1 == len(node.text):
                if is_in_delimiter:
                    out[-1] = TextNode(node.text, TextType.TEXT)
                    print("unterminated delimiter, invalid markdown")
                else:
                    slc = node.text[last_slc_end_idx + 1 : i + 1]
                    out.append(TextNode(slc, TextType.TEXT))
    return out
