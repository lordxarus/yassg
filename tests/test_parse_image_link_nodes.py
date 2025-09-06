import unittest

from yassg.parser import parse_image_nodes, parse_link_nodes
from yassg.textnode import TextNode
from yassg.textnode import TextType as tt


# TODO More tests!
# TODO Impl these tests
class TestParseImageNodes(unittest.TestCase):

    def test_image_simple(self):
        truth = [
            TextNode("This is an image of DS9 ", tt.TEXT),
            TextNode(
                "DS9",
                tt.IMAGE,
                "https://external-content.duckduckgo.com/iu/?u=https\
%3A%2F%2Fwwwimage-us.pplusstatic.com%2Fthumbnails%2Fphotos%2Fw1920-q80%2Fmarq\
uee%2F1044660%2Fstds9_sp_hero_landscape.jpg&f=1&nofb=1&ipt=a0b997f02a56dd70cf6\
edb2f29347e009a827443976192974e919f98995155e0",
            ),
        ]
        self.assertEqual(
            truth,
            parse_image_nodes(
                [
                    TextNode(
                        "This is an image of DS9 ![DS9](https://external-conten\
t.duckduckgo.com/iu/?u=https%3A%2F%2Fwwwimage-us.pplusstatic.com%2Fthumbnails%2\
Fphotos%2Fw1920-q80%2Fmarquee%2F1044660%2Fstds9_sp_hero_landscape.jpg&f=1&nofb=\
1&ipt=a0b997f02a56dd70cf6edb2f29347e009a827443976192974e919f98995155e0)",
                        tt.TEXT,
                    )
                ]
            ),
        )


class TestParseLinkNodes(unittest.TestCase):
    def test_link_simple(self):
        truth = [
            TextNode("This is an image of DS9 ", tt.TEXT),
            TextNode(
                "DS9",
                tt.LINK,
                "https://external-content.duckduckgo.com/iu/?u=https\
%3A%2F%2Fwwwimage-us.pplusstatic.com%2Fthumbnails%2Fphotos%2Fw1920-q80%2Fmarq\
uee%2F1044660%2Fstds9_sp_hero_landscape.jpg&f=1&nofb=1&ipt=a0b997f02a56dd70cf6\
edb2f29347e009a827443976192974e919f98995155e0",
            ),
        ]
        self.assertEqual(
            truth,
            parse_link_nodes(
                [
                    TextNode(
                        "This is an image of DS9 [DS9](https://external-conten\
t.duckduckgo.com/iu/?u=https%3A%2F%2Fwwwimage-us.pplusstatic.com%2Fthumbnails%2\
Fphotos%2Fw1920-q80%2Fmarquee%2F1044660%2Fstds9_sp_hero_landscape.jpg&f=1&nofb=\
1&ipt=a0b997f02a56dd70cf6edb2f29347e009a827443976192974e919f98995155e0)",
                        tt.TEXT,
                    )
                ]
            ),
        )
