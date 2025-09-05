import re
from typing import Sequence, Tuple

from yassg.block import md_to_block_types, md_to_blocks, BlockType
from yassg import logger
from yassg.textnode import TextNode, TextType
from yassg.textnode import TextType as tt
from yassg.leafnode import LeafNode
from yassg.internalnode import InternalNode

default_delims = {
    tt.BOLD: "**",
    tt.ITALIC: "_",
    tt.CODE: "`",
}

print_dbg = logger.get_print_dbg()


def extract_md_imgs(md: str) -> list[Tuple]:
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", md)


def extract_md_links(md: str) -> list[Tuple]:
    return re.findall(r"\[([^\]]*)\]\(([^)]*)\)", md)


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
        if node.text[0] == "!":
            continue
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
            # TODO?
            if c == "*" and len(node.text) - 1 < i + 1:
                print_dbg("detected a closing bold asterisk at the end of a node")
                continue
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


def md_to_textnode(nodes: Sequence[TextNode]) -> list[TextNode]:
    out: list[TextNode] = []
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
    return out if len(out) > 0 else list(nodes)


def md_to_html_node(md: str) -> InternalNode:
    block_types = md_to_block_types(md)
    blocks = md_to_blocks(md)
    root = InternalNode("div", [])

    if len(blocks) == 0:
        return root
    for i, blk in enumerate(blocks):
        match block_types[i]:
            case BlockType.PARAGRAPH:
                root.children.append(InternalNode("p", []))
            case BlockType.HEADING:
                blk = blk.replace("#", "")
                blk = blk.lstrip("\n")
                h_cnt = 0
                for c in blk:
                    if c == "#":
                        h_cnt += 1
                    else:
                        break
                root.children.append(InternalNode(f"h{h_cnt}", []))
            case BlockType.CODE:
                blk = blk.replace("`", "")
                blk = blk.lstrip("\n")
                root.children.append(InternalNode("pre", [LeafNode("code", blk)]))
            case BlockType.QUOTE:
                blk = blk.replace(r"^>", "")
                blk = blk.lstrip("\n")
                root.children.append(InternalNode("blockquote", []))
            case BlockType.UNORDERED_LIST:

                items = blk.split(
                    "\n- ",
                )
                items[0] = items[0][2:]

                list_node = InternalNode("ul", [])

                for item in items:
                    nodes = [
                        it.to_html_node()
                        for it in md_to_textnode([TextNode(item, TextType.TEXT)])
                    ]
                    # nodes = md_to_textnode([TextNode(item, TextType.TEXT)])
                    list_item = InternalNode("li", nodes)
                    list_node.children.append(list_item)

                root.children.append(list_node)

                # for ln in lns:
                #     if ln.startswith("-"):
                #         if list_item.value != "" and list_item.value is not None:
                #             txt_nodes = md_to_textnode(
                #                 [TextNode(list_item.value, TextType.TEXT)]
                #             )
                #             if len(txt_nodes) > 0:
                #                 for txt_node in txt_nodes:
                #                     list_item.children.append(txt_node.to_html_node())
                #             list_node.children.append(list_item)
                #             list_item = InternalNode("li", [])
                #             list_item.value = ""
                #         # reset list_item
                #         else:
                #             list_item = InternalNode("li", [])
                #             list_item.value = ln[1:]

                #     else:
                #         if list_item.value is None:
                #             list_item.value = ln
                #         else:
                #             list_item.value += f"\n{ln}"

            case BlockType.ORDERED_LIST:

                items = blk.split(
                    "\n- ",
                )
                items[0] = items[0][2:]

                list_node = InternalNode("ol", [])

                for item in items:
                    nodes = [
                        it.to_html_node()
                        for it in md_to_textnode([TextNode(item, TextType.TEXT)])
                    ]
                    # nodes = md_to_textnode([TextNode(item, TextType.TEXT)])
                    list_item = InternalNode("li", nodes)
                    list_node.children.append(list_item)

                root.children.append(list_node)

                # for ln in lns:
                #     if ln.startswith("-"):
                #         if list_item.value != "" and list_item.value is not None:
                #             txt_nodes = md_to_textnode(
                #                 [TextNode(list_item.value, TextType.TEXT)]
                #             )
                #             if len(txt_nodes) > 0:
                #                 for txt_node in txt_nodes:
                #                     list_item.children.append(txt_node.to_html_node())
                #             list_node.children.append(list_item)
                #             list_item = InternalNode("li", [])
                #             list_item.value = ""
                #         # reset list_item
                #         else:
                #             list_item = InternalNode("li", [])
                #             list_item.value = ln[1:]

                #     else:
                #         if list_item.value is None:
                #             list_item.value = ln
                #         else:
                #             list_item.value += f"\n{ln}"

            case _:
                print(f"error: invalid block\n\n {blk}")
                exit(-1)
        if (
            block_types[i] != BlockType.CODE
            and block_types[i] != BlockType.UNORDERED_LIST
        ):
            for txt_node in md_to_textnode([TextNode(blk, TextType.TEXT)]):
                root.last_child().children.append(txt_node.to_html_node())
    return root


def md_to_html(md: str) -> str:
    node = md_to_html_node(md)
    return node.to_html()
