import unittest
import sys

if "src/" not in sys.path:
    sys.path += ["src/"]

from parsemd import split_nodes_image, split_nodes_link
from textnode import TextNode
from textnode import TextType as tt


# TODO More tests!
# TODO Impl these tests
# TODO Fix bug, some reason it adds ) to end of URL. Tests for extractors pass
# must be here
class TestSplitNodesImage(unittest.TestCase):

    def test_split_nodes_image_simple(self):
        print(
            split_nodes_image(
                [
                    TextNode(
                        "This is an image of DS9 ![DS9](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwwwimage-us.pplusstatic.com%2Fthumbnails%2Fphotos%2Fw1920-q80%2Fmarquee%2F1044660%2Fstds9_sp_hero_landscape.jpg&f=1&nofb=1&ipt=a0b997f02a56dd70cf6edb2f29347e009a827443976192974e919f98995155e0)",
                        tt.TEXT,
                    )
                ]
            )
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_simple(self):
        print(
            split_nodes_link(
                [
                    TextNode(
                        "This is an image of DS9 [DS9](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwwwimage-us.pplusstatic.com%2Fthumbnails%2Fphotos%2Fw1920-q80%2Fmarquee%2F1044660%2Fstds9_sp_hero_landscape.jpg&f=1&nofb=1&ipt=a0b997f02a56dd70cf6edb2f29347e009a827443976192974e919f98995155e0)",
                        tt.TEXT,
                    )
                ]
            )
        )
