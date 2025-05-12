from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """
    A leaf node must not have any children and the
    value must not be None
    """

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError()
        if self.tag == None:
            return self.value

        return f"<{self.tag}> {self.value} </{self.tag}>"
