from __future__ import annotations
from functools import reduce
from typing import Sequence


class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence[HTMLNode] = [],
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children: list[HTMLNode] = list(children)
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props == None:
            return ""

        return str(
            reduce(
                lambda str, prop: f'{str} {prop[0]}="{prop[1]}"', self.props.items(), ""
            )
        )

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
