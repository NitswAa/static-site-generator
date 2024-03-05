from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            if not text_node.url:
                raise ValueError("No URL for anchor tag!")
            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case "img":
            if not text_node.url:
                raise ValueError("No image source for img tag!")
            return LeafNode(tag="img", value=text_node.text, props={"src":text_node.url})
        case _:
            raise ValueError("Invalid text type!")

if __name__ == "__main__":
    test_node = TextNode("This is a test!", "normal", "https://www.rev.dev/SSG")

    print(test_node)
