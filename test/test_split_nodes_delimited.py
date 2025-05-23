import unittest
import sys

if "src/" not in sys.path:
    sys.path += ["src/"]
from textnode import TextNode, split_nodes_delimited
from textnode import TextType as tt


class TestSplitTextDelimited(unittest.TestCase):

    def test_first_char_delim(self):
        test_str = "_Netflix_ used to ship DVDs?"
        truth = [
            TextNode("Netflix", tt.ITALIC),
            TextNode(" used to ship DVDs?", tt.TEXT),
        ]

        self.assertEqual(
            truth, split_nodes_delimited([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )

    def test_last_char_delim(self):
        test_str = "Netflix used to ship _DVDs?_"
        truth = [
            TextNode("Netflix used to ship ", tt.TEXT),
            TextNode("DVDs?", tt.ITALIC),
        ]

        self.assertEqual(
            truth, split_nodes_delimited([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )

    def test_unterminated_delim(self):
        test_str = "Netflix u_sed to ship DVDs?"
        truth = [TextNode(test_str, tt.TEXT)]
        self.assertEqual(truth, split_nodes_delimited(truth, tt.ITALIC))

    def test_entire_str_delimited(self):
        test_str = "_Very italicized_"
        truth = [TextNode(test_str.strip("_"), tt.ITALIC)]
        self.assertEqual(
            truth, split_nodes_delimited([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )


# TODO:
#     - links
#     - images
#     - probably do left char right char tuple. need to support
#       non symmetrical delimiters
TestSplitTextDelimited("test_entire_str_delimited").run()
