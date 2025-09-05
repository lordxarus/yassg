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
            (
                self.text == other.text
                and self.type == other.type
                and self.url == other.url
            )
            if other is not None
            else False
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.type.name}, {self.url})"

    def __hash__(self):
        return hash(f"{self.text}{self.type}{self.url}")

    def to_html_node(self) -> HTMLNode:
        match self.type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                assert self.url is not None
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.IMAGE:
                assert self.url is not None
                return LeafNode("img", "", {"alt": self.text, "src": self.url})
            case _:
                raise ValueError(f"invalid TextType: {self.type.name}")
