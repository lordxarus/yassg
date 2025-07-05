import unittest
import sys

import sys

if "src/" not in sys.path:
    sys.path += ["src/"]

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        one = HTMLNode("b", "This is the text", None, {"nuclear": "salad"})
        two = HTMLNode("b", "This is the text", None, {"nuclear": "salad"})
        three = HTMLNode("b", "This is the text", [one, two], {"nuclear": "salad"})

        self.assertEqual(one, two)
        self.assertNotEqual(one, three)

    def test_repr(self):

        truth = "HTMLNode(b, This is the text, [HTMLNode(b, This is the text, None, {'nuclear': 'salad'}), HTMLNode(b, This is the text, None, {'nuclear': 'salad'})], {'nuclear': 'salad'})"

        one = HTMLNode("b", "This is the text", None, {"nuclear": "salad"})
        two = HTMLNode("b", "This is the text", None, {"nuclear": "salad"})
        three = HTMLNode("b", "This is the text", [one, two], {"nuclear": "salad"})

        return self.assertEqual(truth, str(three))

    def test_props_to_html(self):
        truth = ' href="https://www.google.com" target="_blank"'
        one = HTMLNode(
            "a",
            "The link!",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(truth, one.props_to_html())

    def test_empty_children(self):
        one = HTMLNode(
            "a",
            "The link!",
            [],
            {"href": "https://www.google.com", "target": "_blank"},
        )
        truth = "HTMLNode(a, The link!, [], {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(truth, str(one))

    def test_empty_props(self):
        one = HTMLNode("a", "The link!", None, {})
        self.assertEqual("", str(one.props_to_html()))
