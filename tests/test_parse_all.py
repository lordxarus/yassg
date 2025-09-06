import unittest

from yassg.parser import md_to_textnode
from yassg.textnode import TextNode, TextType as tt


class TestParseAll(unittest.TestCase):

    def test_parse_all_simple(self):
        data = [
            TextNode(
                "The latest moves by large AI companies have me wondering...\
are the **MBAs** ok?",
                tt.TEXT,
            ),
            TextNode(
                "For example, [Meta](https://meta.com) just lost 5 out of 13\
 researchers to Mistral",
                tt.TEXT,
            ),
            TextNode(
                "Likely, ![Mark](https://www.horizont.net/news/media/3/Mark-Zuck\
erberg-wird-Media-Person-Of-The-Year-26222-detailpp.jpeg) isn't very happy.",
                tt.TEXT,
            ),
        ]
        truth = [
            TextNode(
                "The latest moves by large AI companies have me wondering...are the ",
                tt.TEXT,
            ),
            TextNode("MBAs", tt.BOLD),
            TextNode(" ok?", tt.TEXT),
            TextNode("For example, ", tt.TEXT),
            TextNode("Meta", tt.LINK, "https://meta.com"),
            TextNode(" just lost 5 out of 13 researchers to Mistral", tt.TEXT),
            TextNode("Likely, ", tt.TEXT),
            TextNode(
                "Mark",
                tt.IMAGE,
                "https://www.horizont.net/news/media/3/M\
ark-Zuckerberg-wird-Media-Person-Of-The-Year-26222-detailpp.jpeg",
            ),
            TextNode(" isn't very happy.", tt.TEXT),
        ]
        self.assertEqual(truth, md_to_textnode(data))

    def test_untermed_then_termed(self):
        test_str = "Netflix u_sed **to** sell DVDs?"
        truth = [
            TextNode("Netflix u_sed ", tt.TEXT),
            TextNode("to", tt.BOLD),
            TextNode(" sell DVDs?", tt.TEXT),
        ]
        self.assertEqual(truth, md_to_textnode([TextNode(test_str, tt.TEXT)]))
