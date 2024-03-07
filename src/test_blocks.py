import unittest
from blocks import markdown_to_blocks
from blocks import block_to_block_type


class TestBlocks(unittest.TestCase):
    def test_split(self):
        markdown = (
            "This is **bolded** paragraph\n\n" +
            "This is another paragraph with *italic* text and `code` here\n" +
            "This is the same paragraph on a new line\n\n" +
            "* This is a list\n" +
            "* with items\n\n\n"
        )
        result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]

        self.assertEqual(markdown_to_blocks(markdown), result)

    def test_block_type(self):
        block = "This is bloded paragraph:"

        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_block_type_2(self):
        block = "1. This is\n2. An ordered\n3. List!"

        self.assertEqual(block_to_block_type(block), "ol")

    def test_block_type_3(self):
        block = "* This is\n* An unordered\n* List!"

        self.assertEqual(block_to_block_type(block), "ul")

    def test_block_type_4(self):
        block = ">This is\n>a block quote\n>which is definitely very big\n>and long"

        self.assertEqual(block_to_block_type(block), "quote")

    def test_block_type_5(self):
        block = "```py print(\"Hello, this is a code block!\")\nprint(\"Hopefully the newline is fine!\")```"

        self.assertEqual(block_to_block_type(block), "code")


if __name__ == "__main__":
    unittest.main()
