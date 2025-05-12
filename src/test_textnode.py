import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "jeremyball.me")
        node2 = TextNode("This is a text node", TextType.BOLD, "jeremyball.me")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is THE text node", TextType.BOLD, "jeremyball.me")
        node2 = TextNode("This is a text node", TextType.BOLD, "jeremyball.me")
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD, "jeremyball.me")
        node2 = TextNode("This is a text node", TextType.CODE, "jeremyball.me")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
