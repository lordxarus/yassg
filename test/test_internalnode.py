import unittest
import sys


sys.path += ["src/"]
from htmlnode import HTMLNode
from internalnode import InternalNode
from leafnode import LeafNode


class TestInternalNode(unittest.TestCase):

    def test_to_html(self):
        self.assertEqual(
            InternalNode(
                "html", [LeafNode("b", "They're killing us slowly man", None)], None
            ).to_html(),
            "<html> <b> They're killing us slowly man </b> </html>",
        )

        """
        <html>
            <body>
                <ul>
                   <a href="https://oizo3000.com"> And we goto the church </a>
                </ul>
            </body>
           <b> They're killing us slowly man </b>
        </html>  
        """

    def test_to_html_nested_internal(self):
        print(
            InternalNode(
                "html",
                [
                    InternalNode(
                        "body",
                        [
                            InternalNode(
                                "ul",
                                [
                                    LeafNode(
                                        "a",
                                        "And we... goto the Church",
                                        {"href": "https://www.oizo3000.com/"},
                                    ),
                                    LeafNode("h1", "Maybe we stay in?", None),
                                ],
                            )
                        ],
                    ),
                    LeafNode("b", "They're killing us slowly man", None),
                ],
            ).to_html()
        )


TestInternalNode("test_to_html_nested_internal").test_to_html_nested_internal()
