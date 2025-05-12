from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    print("hello world")
    print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
    print(
        HTMLNode(
            "a",
            "Google",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        ).props_to_html()
    )
    print(
        HTMLNode(
            "a",
            "Google",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
    )


main()
