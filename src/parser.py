import re
from typing import Tuple

from textnode import TextNode
from textnode import TextType as tt

default_delims = {
    tt.BOLD: "**",
    tt.ITALIC: "_",
    tt.CODE: "`",
}


def md_to_blocks(md: str) -> list[str]:
    out = md.split("\n\n")
    for i in range(len(out)):
        out[i] = out[i].strip()
    return out


def extract_md_imgs(md: str) -> list[Tuple]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", md)


def extract_md_links(md: str) -> list[Tuple]:
    return re.findall(r"\s\[([^\]]*)\]\(([^)]*)\)", md)


def parse_image_nodes(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for i, node in enumerate(nodes):
        if node.type is not tt.TEXT:
            new_nodes.append(node)
            continue
        working_str: str = node.text
        imgs: list[Tuple[str, str]] = extract_md_imgs(working_str)

        for img in imgs:
            splt: list[str] = working_str.split(f"![{img[0]}]({img[1]})")
            new_nodes.append(TextNode(splt[0], tt.TEXT))
            new_nodes.append(TextNode(img[0], tt.IMAGE, img[1]))
            if i + 1 == len(nodes) and splt[1] != "":
                new_nodes.append(TextNode(splt[1], tt.TEXT))
            working_str = splt[1]
    return new_nodes


def parse_link_nodes(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for i, node in enumerate(nodes):
        if node.type is not tt.TEXT:
            new_nodes.append(node)
            continue
        working_str: str = node.text
        imgs: list[Tuple[str, str]] = extract_md_links(working_str)

        for img in imgs:
            splt: list[str] = working_str.split(f"[{img[0]}]({img[1]})")
            new_nodes.append(TextNode(splt[0], tt.TEXT))
            new_nodes.append(TextNode(img[0], tt.LINK, img[1]))
            if i + 1 == len(nodes) and splt[1] != "":
                new_nodes.append(TextNode(splt[1], tt.TEXT))
            working_str = splt[1]
    return new_nodes


# TODO: nested elements e.g: This is an _italic and **bold** word_.
def parse_inline_nodes(
    old_nodes: list[TextNode], new_type: tt, delimiter: str | None = None
) -> list[TextNode]:
    # Maybe belongs in tt? Maybe use __attr__

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
            out.append(node)
        last_slc_end_idx = -1
        is_in_delimiter = False
        untermed_idx = -1
        for i, c in enumerate(node.text):
            if c == "*" and node.text[i + 1] != "*" and i + 1 != len(node.text):
                continue
            if c in delimiter:
                if is_in_delimiter:
                    slc = node.text[last_slc_end_idx + 1 : i + 1].strip(delimiter)
                    if c == "*":
                        slc = slc.strip(delimiter)
                        last_slc_end_idx = i + 1
                    else:
                        last_slc_end_idx = i
                    out.append(TextNode(slc, new_type))
                    is_in_delimiter = False
                else:
                    if i != 0:
                        slc = node.text[last_slc_end_idx + 1 : i]
                        untermed_idx = len(out)
                        out.append(TextNode(slc, tt.TEXT))
                        last_slc_end_idx = i - 1
                    is_in_delimiter = True
            elif i + 1 == len(node.text):
                if is_in_delimiter:
                    # TODO: when we know we've hit a delimiter but it is
                    # unterminated we have a sort of dangling entry in out[-1]
                    # that consists of everything before the delimiter. untermed_idx
                    # keeps track of the last dangling entry which we replace here.
                    # Instead of using out[-1] because of the edge case where we have an untermed
                    # delimiter and then a terminated delimiter like 'Netflix u_sed **to** sell DVDs?'
                    out[untermed_idx] = TextNode(node.text, tt.TEXT)
                    print("unterminated delimiter, invalid markdown")
                else:
                    slc = node.text[last_slc_end_idx + 1 : i + 1]
                    out.append(TextNode(slc, tt.TEXT))
    return out


def parse_nodes(nodes: list[TextNode]) -> list[TextNode | None]:
    out: list[TextNode | None] = []
    for node in nodes:
        for type in default_delims:
            parsed: list[TextNode] = parse_inline_nodes([node], type)
            # parsed =
            if len(parsed) > 1:
                for parsed_node in parsed:
                    if parsed_node not in out:
                        out.append(parsed_node)

        parsed = parse_image_nodes([node])
        if len(parsed) > 1:
            for parsed_node in parsed:
                if parsed_node not in out:
                    out.append(parsed_node)

        parsed = parse_link_nodes([node])
        if len(parsed) > 1:
            for parsed_node in parsed:
                if parsed_node not in out:
                    out.append(parsed_node)
    return out
