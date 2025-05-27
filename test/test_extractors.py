import unittest
import sys

if "src/" not in sys.path:
    sys.path += ["src/"]
from parser import extract_md_imgs, extract_md_links


# TODO: Write more tests!
class TestExtractRegex(unittest.TestCase):

    def test_extract_md_imgs(self):
        truth = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(
            truth,
            extract_md_imgs(
                "![rick roll](https://i.imgur.com/aKaOqIh.gif)\
and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            ),
        )

    def test_extract_md_links(self):
        truth = [
            ("to site", "https://jeremyball.me"),
            ("to cool youtube channel", "https://www.youtube.com/@LGR"),
        ]
        self.assertEqual(
            truth,
            extract_md_links(
                "This is text with a link [to site](https://jeremyball.me)\
and [to cool youtube channel](https://www.youtube.com/@LGR)"
            ),
        )
