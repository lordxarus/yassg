import unittest
import sys

if "src/" not in sys.path:
    sys.path += ["src/"]
from textnode import TextNode, get_inline_delims, split_nodes_delimited
from textnode import TextType as tt


class TestSplitTextDelimited(unittest.TestCase):

    def test_first_char_delim_bold(self):
        test_str = "**Netflix** used to ship DVDs?"
        truth = [
            TextNode("Netflix", tt.BOLD),
            TextNode(" used to ship DVDs?", tt.TEXT),
        ]

        self.assertEqual(
            truth, split_nodes_delimited([TextNode(test_str, tt.TEXT)], tt.BOLD)
        )

    def test_middle_bold(self):
        test_str = "This is text with a **bolded phrase** in the middle"
        truth = [
            TextNode("This is text with a ", tt.TEXT),
            TextNode("bolded phrase", tt.BOLD),
            TextNode(" in the middle", tt.TEXT),
        ]

        self.assertEqual(
            truth, split_nodes_delimited([TextNode(test_str, tt.TEXT)], tt.BOLD)
        )

    def test_first_char_delim_italics(self):
        test_str = "_Netflix_ used to ship DVDs?"
        truth = [
            TextNode("Netflix", tt.ITALIC),
            TextNode(" used to ship DVDs?", tt.TEXT),
        ]

        self.assertEqual(
            truth, split_nodes_delimited([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )

    def test_last_char_delim_italics(self):
        test_str = "Netflix used to ship _DVDs?_"
        truth = [
            TextNode("Netflix used to ship ", tt.TEXT),
            TextNode("DVDs?", tt.ITALIC),
        ]

        self.assertEqual(
            truth, split_nodes_delimited([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )

    def test_unterminated_delim_italics(self):
        test_str = "Netflix u_sed to ship DVDs?"
        truth = [TextNode(test_str, tt.TEXT)]
        self.assertEqual(truth, split_nodes_delimited(truth, tt.ITALIC))

    def test_entire_str_delimited_italics(self):
        test_str = "_Very italicized_"
        truth = [TextNode(test_str.strip("_"), tt.ITALIC)]
        self.assertEqual(
            truth, split_nodes_delimited([TextNode(test_str, tt.TEXT)], tt.ITALIC)
        )

    # def test_heterogeneous_pair(self):
    #     test_str = (
    #         "The best search engine in 2025 is [DuckDuckGo](https://duckduckgo.com)"
    #     )
    #     truth = [
    #         TextNode("The best search engine in 2025 is ", tt.TEXT),
    #         TextNode("DuckDuckGo", tt.LINK, "https://duckduckgo.com"),
    #     ]
    #     self.assertEqual
