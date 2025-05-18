from functools import reduce
from htmlnode import HTMLNode, HTMLNodeType
from leafnode import LeafNode


class InternalNode(HTMLNode):

    __name__ = "InternalNode"

    def __init__(
        self,
        tag: str,
        children: list[HTMLNodeType],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == "":
            raise ValueError(f"{self.__name__} tag must not be empty")
        if self.tag is None:
            raise ValueError(f"{self.__name__} tag must not be None")
        if self.children is None:
            raise ValueError(f"{self.__name__} children must not be None")
        if len(self.children) == 0:
            raise ValueError(f"{self.__name__} children must not be empty")

        self.children: list[HTMLNode]

        def depth(node) -> str:
            if isinstance(node, LeafNode):
                return node.to_html()
            for c in node.children:
                return f"<{node.tag}{node.props_to_html()}> {depth(c)} </{node.tag}>"

        out = str(reduce(lambda acc, child: f"{acc}{depth(child)} ", self.children, ""))

        return f"<{self.tag}{self.props_to_html()}> {out[:-1]} </{self.tag}>"
