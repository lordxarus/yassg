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


# class Delimiter:
#     left: str
#     right: str

#     def __init__(self, left: str, right: str = ""):
#         self.left = left
#         self.right = right if right != "" else left

#     def __repr__(self):
#         return f"{self.left}{self.right}


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


def get_inline_delims() -> dict[TextType, str]:
    return {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`",
    }


# TODO: nested elements e.g: This is an _italic and **bold** word_.
def split_nodes_delimited(
    old_nodes: list[TextNode], new_type: TextType, delimiter: str | None = None
) -> list[TextNode]:
    # Maybe belongs in TextType? Maybe use __attr__
    if new_type == TextType.TEXT:
        return old_nodes
    if delimiter is None:
        try:
            delimiter = get_inline_delims()[new_type]
        except KeyError:
            raise ValueError("no delimiter given and no known default")

    def process_node(node: TextNode) -> list[TextNode]:
        if node.type is not TextType.TEXT:
            # TODO: Maybe raise an exception here instead?
            return [node]
        nodes = []
        last_slc_end_idx = -1
        is_in_delimiter = False
        len_delim = len(delimiter)
        for i, c in enumerate(node.text):
            if len_delim > 1:
                c = node.text[i : i + len_delim]
            if c == delimiter:
                if is_in_delimiter:
                    slc = node.text[last_slc_end_idx + 1 : i + len_delim].strip(
                        delimiter
                    )
                    nodes.append(TextNode(slc, new_type))
                    last_slc_end_idx = i
                    is_in_delimiter = False
                else:
                    # This is an _italic_
                    # This ends _without_ an italic
                    # This has _two_ _italics_ look!
                    # This has _one_ italic and one _unterminated delimiter
                    if i != 0:
                        slc = node.text[last_slc_end_idx + 1 : i]
                        nodes.append(TextNode(slc, TextType.TEXT))
                        last_slc_end_idx = i
                    is_in_delimiter = True
            elif i + 1 == len(node.text):
                if is_in_delimiter:
                    nodes[-1] = TextNode(node.text, TextType.TEXT)
                    print("unterminated delimiter, invalid markdown")
                else:
                    slc = node.text[last_slc_end_idx + len_delim : i + 1]
                    nodes.append(TextNode(slc, TextType.TEXT))

        return nodes

    out: list[TextNode] = []
    for node in old_nodes:
        out.extend(process_node(node))
    return out
