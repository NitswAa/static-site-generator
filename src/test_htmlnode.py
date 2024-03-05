import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_p2h(self):
        node = HTMLNode(props={"test": "first prop", "second": "proper prop"})

        self.assertEqual(" test=\"first prop\" second=\"proper prop\"", node.props_to_html())

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.props)
        
        node2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.rev.dev/test_case"})
        self.assertEqual(node2.tag, "a")
        self.assertEqual(node2.value, "Click me!")
        self.assertEqual(node2.props, {"href": "https://www.rev.dev/test_case"})

        self.assertIsNone(node2.children)

    def test_eq(self):

        node1 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.rev.dev/test_case"})
        node2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.rev.dev/test_case"})

        self.assertEqual(node1, node2)

    def test_to_html(self):
        node1 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.rev.dev/test_case"})
        
        self.assertEqual(node1.to_html(), "<a href=\"https://www.rev.dev/test_case\">Click me!</a>")

        empty_node = LeafNode()
        with self.assertRaises(ValueError):
            empty_node.to_html()

        img_node = LeafNode(tag="img", value="alt text", props={"src":"./image.png", "height": 400, "width": 200})
        self.assertEqual(img_node.to_html(), "<img src=\"./image.png\" height=\"400\" width=\"200\" alt=\"alt text\" />")

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ],
            tag="p",
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_empty_children(self):
        node = ParentNode(
                [],
                tag="p",
                props={
                    "href": "https://www.rev.dev/test_case"
                    }
                )

        self.assertEqual(node.to_html(), "<p href=\"https://www.rev.dev/test_case\"></p>")

    def test_nested_parents(self):
        children = [
                 ParentNode(
                    [
                        LeafNode(tag="a", value="Click Me!", props={"href": "https://www.rev.dev/test_case"}),
                    ],
                    tag="li"
                    ),

                 ParentNode(
                    [
                        LeafNode(tag="a", value="Click Me!", props={"href": "https://www.rev.dev/test_case"}),
                    ],
                    tag="li"
                    ),
                 ParentNode(
                    [
                        LeafNode(tag="a", value="Click Me!", props={"href": "https://www.rev.dev/test_case"}),
                    ],
                    tag="li"
                    ),
                   ]
        
        node = ParentNode(children, tag="ul", props={"class":"basic_list"})

        expected_result = "<ul class=\"basic_list\"><li><a href=\"https://www.rev.dev/test_case\">Click Me!</a></li><li><a href=\"https://www.rev.dev/test_case\">Click Me!</a></li><li><a href=\"https://www.rev.dev/test_case\">Click Me!</a></li></ul>"
        self.assertEqual(node.to_html(), expected_result)

if __name__ == "__main__":
    unittest.main()
