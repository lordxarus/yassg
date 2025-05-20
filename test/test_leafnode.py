import unittest
import sys

if not "src/" in sys.path:
    sys.path += ["src/"]
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p> Hello, world! </p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a> Hello, world! </a>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b> Hello, world! </b>")

    def test_to_html_a_props(self):
        node = LeafNode(
            "a", "And we goto the Church", {"href": "https://jeremyball.me"}
        )
        self.assertEqual(
            '<a href="https://jeremyball.me"> And we goto the Church </a>',
            node.to_html(),
        )
