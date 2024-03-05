import unittest

from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from main import text_node_to_html_node

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

        self.assertEqual("TextNode(This is a text node, italic, None)", node.__repr__())

    def test_valid(self):
        node = TextNode("This is a valid type!", "italic")
        
        with self.assertRaises(ValueError):
            node2 = TextNode("This is an invalid type!", "wrong")

    def test_text_to_html(self):
        text_node = TextNode("This is just some basic text.", "text")
        leaf_node = text_node_to_html_node(text_node)

        self.assertEqual(leaf_node, LeafNode(tag=None, value="This is just some basic text.", props=None))
if __name__ == "__main__":
    unittest.main()
