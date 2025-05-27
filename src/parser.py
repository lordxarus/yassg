import re
from typing import Tuple

from textnode import TextNode
from textnode import TextType as tt


def extract_md_imgs(md: str) -> list[Tuple]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", md)


def extract_md_links(md: str) -> list[Tuple]:
    return re.findall(r"\s\[([^\]]*)\]\(([^)]*)\)", md)


def parse_image_nodes(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in nodes:
        if node.type is not tt.TEXT:
            new_nodes.append(node)
            continue
        working_str: str = node.text
        imgs: list[Tuple[str, str]] = extract_md_imgs(working_str)

        for img in imgs:
            splt: list[str] = working_str.split(f"![{img[0]}]({img[1]})")
            new_nodes.append(TextNode(splt[0], tt.TEXT))
            new_nodes.append(TextNode(img[0], tt.IMAGE, img[1]))
            working_str = splt[1]
    return new_nodes


def parse_link_nodes(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in nodes:
        if node.type is not tt.TEXT:
            new_nodes.append(node)
            continue
        working_str: str = node.text
        imgs: list[Tuple[str, str]] = extract_md_links(working_str)

        for img in imgs:
            splt: list[str] = working_str.split(f"[{img[0]}]({img[1]})")
            new_nodes.append(TextNode(splt[0], tt.TEXT))
            new_nodes.append(TextNode(img[0], tt.IMAGE, img[1]))
            working_str = splt[1]
    return new_nodes


# TODO: nested elements e.g: This is an _italic and **bold** word_.
def parse_inline_nodes(
    old_nodes: list[TextNode], new_type: tt, delimiter: str | None = None
) -> list[TextNode]:
    # Maybe belongs in tt? Maybe use __attr__
    default_delims = {
        tt.BOLD: "*",
        tt.ITALIC: "_",
        tt.CODE: "`",
    }
    if new_type == tt.TEXT:
        return old_nodes
    if delimiter is None:
        try:
            delimiter = default_delims[new_type]
        except KeyError:
            raise ValueError("no delimiter given and no known default")

    out: list[TextNode] = []
    for node in old_nodes:
        if node.type is not tt.TEXT:
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
                        out.append(TextNode(slc, tt.TEXT))
                        last_slc_end_idx = i - 1
                    is_in_delimiter = True
            elif i + 1 == len(node.text):
                if is_in_delimiter:
                    out[-1] = TextNode(node.text, tt.TEXT)
                    print("unterminated delimiter, invalid markdown")
                else:
                    slc = node.text[last_slc_end_idx + 1 : i + 1]
                    out.append(TextNode(slc, tt.TEXT))
    return out
