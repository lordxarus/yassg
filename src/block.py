from enum import Enum
from re import match


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def md_to_blocks(md: str) -> list[str]:
    out = md.split("\n\n")
    for i in range(len(out)):
        out[i] = out[i].strip()
    return out


"""Takes a markdown string and returns the BlockType it is 
"""


def block_to_block_type(md: str) -> BlockType | None:
    if len(md) == 0:
        return None
    first = md[0]
    ordered_list_count = 1

    # I could do this with regex
    match first:
        case "#":
            return BlockType.HEADING
        case ">":
            return BlockType.QUOTE
        case "-":
            return BlockType.UNORDERED_LIST if md[1] == " " else None
        case "`":
            if len(md) >= 6 and md[1] == "`" and md[2] == "`":
                return (
                    BlockType.CODE
                    if md[-1] == "`" and md[-2] == "`" and md[-3] == "`"
                    else BlockType.PARAGRAPH
                )
        case _:
            if not match(r"\d\.", md):
                return BlockType.PARAGRAPH

            ordered_list_count = int(md[0]) + 1
            lines = md.split("\n")
            lines = lines[1:]

            for ln in lines:
                matched = match(r"(\d)\.", ln)
                if matched != None:
                    if int(matched.group().replace(".", "")) == ordered_list_count:
                        ordered_list_count += 1
                    # else we know we have a digit and that it is not in order
                    else:
                        return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
