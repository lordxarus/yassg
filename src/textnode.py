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

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.type == other.type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.type.name}, {self.url})"


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
            assert not text_node.url is None
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            assert not text_node.url is None
            return LeafNode("img", "", {"alt": text_node.text, "src": text_node.url})
        case _:
            raise ValueError(f"invalid TextType: {text_node.type.name}")
