import unittest
import sys

if "src/" not in sys.path:
    sys.path += ["src/"]

from block import block_to_block_type, BlockType
from block import md_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_md_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = md_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_to_blk_type(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("#Hello World"))
        self.assertEqual(BlockType.CODE, block_to_block_type("```Hello World```"))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("```Hello World``"))
        self.assertEqual(BlockType.CODE, block_to_block_type("```Hello World\n```"))
        self.assertEqual(
            BlockType.ORDERED_LIST, block_to_block_type("1.Hello World\n2.Bye for now!")
        )
        self.assertEqual(
            BlockType.PARAGRAPH, block_to_block_type("2.Hello World\n1.Bye for now!")
        )
