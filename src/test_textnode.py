import unittest

from textnode import TextNode
from htmlnode import LeafNode
from blocks import text_node_to_html_node
from textnode import split_nodes_delimiter, extract_markdown_links, extract_markdown_images
from textnode import split_nodes_link
from textnode import text_to_nodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node, node3)

    def test_neq(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")

        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "italic")

        self.assertEqual(
            "TextNode(This is a text node, italic, None)", node.__repr__())

    def test_valid(self):
        node = TextNode("This is a valid type!", "italic")

        with self.assertRaises(ValueError):
            node2 = TextNode("This is an invalid type!", "wrong")

    def test_text_to_html(self):
        text_node = TextNode("This is just some basic text.", "text")
        leaf_node = text_node_to_html_node(text_node)

        self.assertEqual(leaf_node, LeafNode(
            tag=None, value="This is just some basic text.", props=None))


class TextSplits(unittest.TestCase):
    def test_split_italic(self):
        node = TextNode(
            "This is *a* test to split by *the asterisk* delimiter!", "text")
        split_nodes = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(split_nodes, [TextNode("This is ", "text"), TextNode("a", "italic"), TextNode(" test to split by ", "text"),
                                       TextNode("the asterisk", "italic"), TextNode(" delimiter!", "text")])

    def test_split_code(self):
        node = TextNode(
            "This is `a` test to split by `the asterisk` delimiter!", "text")
        split_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(split_nodes, [TextNode("This is ", "text"), TextNode("a", "code"), TextNode(" test to split by ", "text"),
                                       TextNode("the asterisk", "code"), TextNode(" delimiter!", "text")])

    def test_split_bold(self):
        node = TextNode(
            "This is **a** test to split by **the asterisk** delimiter!", "text")
        split_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(split_nodes, [TextNode("This is ", "text"), TextNode("a", "bold"), TextNode(" test to split by ", "text"),
                                       TextNode("the asterisk", "bold"), TextNode(" delimiter!", "text")])

    def test_extract_images(self):
        node = TextNode(
            "Look at ![this!](https://www.imgur.com/wow.png)", "img")
        self.assertEqual(extract_markdown_images(node.text), [
                         ("this!", "https://www.imgur.com/wow.png")])

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [
                         ("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://www.example.com) and ![another](https://www.example.com/another), wow!", "img")
        result = [TextNode("This is text with an ", "text"),
                  TextNode("image", "img", "https://www.example.com"),
                  TextNode(" and ", "text"),
                  TextNode("another", "img",
                           "https://www.example.com/another"),
                  TextNode(", wow!", "text"),
                  ]

        self.assertEqual(split_nodes_link([node], img=True), result)

    def test_split_images_endpoint(self):
        node = TextNode(
            "This is text with an ![image](https://www.example.com) and ![another](https://www.example.com/another)", "img")
        result = [TextNode("This is text with an ", "text"),
                  TextNode("image", "img", "https://www.example.com"),
                  TextNode(" and ", "text"),
                  TextNode("another", "img",
                           "https://www.example.com/another"),
                  ]

        self.assertEqual(split_nodes_link([node], img=True), result)

    def test_split_links(self):
        pass


class Complete(unittest.TestCase):
    def test_full_1(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"

        result = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "img",
                     "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]

        self.assertEqual(text_to_nodes(text), result)


if __name__ == "__main__":
    unittest.main()
