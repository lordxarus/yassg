from __future__ import annotations
from functools import reduce
from typing import Self, Sequence


class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence[Self] = [],
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children: list[Self] = list(children)
        self.props = props

    def to_html(self: Self) -> str:
        raise NotImplementedError

    def props_to_html(self: Self) -> str:
        if self.props == None:
            return ""

        return str(
            reduce(
                lambda str, prop: f'{str} {prop[0]}="{prop[1]}"', self.props.items(), ""
            )
        )

    def __repr__(self: Self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self: Self, other) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
