from yassg.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """
    A leaf node must not have any children and the
    value must not be None
    """

    __name__ = "LeafNode"

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, [], props)

    def to_html(self) -> str:

        # if self.value == "":
            # import pdb
            # pdb.set_trace()
            # raise ValueError(f"{self.__name__} value must not be empty")
        if self.value is None:
            raise ValueError(f"{self.__name__} value must not be None")
        if self.tag == None or self.tag == "":
            return self.value

        return f"<{self.tag}{self.props_to_html()}> {self.value} </{self.tag}>"
