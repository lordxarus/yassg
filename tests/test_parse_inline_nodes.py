import unittest
import sys

if "src/" not in sys.path:
    sys.path += ["src/"]
from parser import parse_inline_nodes
from textnode import TextNode, TextType as tt


class TestParseNodesInline(unittest.TestCase):

    def test_first_char_delim(self):
        test_str = "_Netflix_ used to ship DVDs?"
        truth = [
            TextNode("Netflix", tt.ITALIC),
            TextNode(" used to ship DVDs?", tt.TEXT),
        ]

        self.assertEqual(
            truth, parse_inline_nodes([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )

    def test_last_char_delim(self):
        test_str = "Netflix used to ship _DVDs?_"
        truth = [
            TextNode("Netflix used to ship ", tt.TEXT),
            TextNode("DVDs?", tt.ITALIC),
        ]

        self.assertEqual(
            truth, parse_inline_nodes([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )

    def test_unterminated_delim(self):
        test_str = "Netflix u_sed to ship DVDs?"
        truth = [TextNode(test_str, tt.TEXT)]
        self.assertEqual(truth, parse_inline_nodes(truth, tt.ITALIC))

    def test_entire_str_delimited(self):
        test_str = "_Very italicized_"
        truth = [TextNode(test_str.strip("_"), tt.ITALIC)]
        self.assertEqual(
            truth, parse_inline_nodes([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )
