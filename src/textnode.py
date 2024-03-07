import re


class TextNode():
    valid_types = [
        "text",
        "bold",
        "italic",
        "code",
        "link",
        "img",
    ]

    def __init__(self, text, text_type="text", url=None):
        if text_type not in self.valid_types:
            raise ValueError("Invalid Text Type")

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

# TODO
# I wanna extend this to nested possibilities:
# At least in the case of bold and italics...
# My main guess is that I just wanna have bold
# Run first, then italics. However, that means I
# Would need to make a special case for Bold, when
# Contained by italics.


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            split_nodes_text = node.text.split(delimiter)
            split_nodes = []
            if len(split_nodes_text) % 2 == 0:
                raise SyntaxError(
                    "Invalid Markdown Syntax: No matching delimiter")
            # Add text
            for i in range(len(split_nodes_text)):
                if i % 2 == 0:
                    # Add regular text
                    if split_nodes_text[i] == '':
                        raise ValueError(
                            "Unexpected blank space, consider bold > italic")
                    split_nodes.append(TextNode(split_nodes_text[i], "text"))
                else:
                    # Add delimited text
                    split_nodes.append(
                        TextNode(split_nodes_text[i], text_type))
            new_nodes += split_nodes

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_link(old_nodes, img=False):
    # Takes a "link" tuple as returned by regex extraction
    # And formats the string to use for splitting based
    # On if the link is an image or not (img needs "!" preceding)
    if img:
        def splitter_string(link):
            return f"![{link[0]}]({link[1]})"
    else:
        def splitter_string(link):
            return f"[{link[0]}]({link[1]})"
    new_nodes = []

    for node in old_nodes:
        split_nodes = []
        if img:
            links = extract_markdown_images(node.text)
        else:
            links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        original_text = node.text
        for link in links:
            split_nodes_text = original_text.split(splitter_string(link), 1)
            if len(split_nodes_text) < 2:
                raise ValueError("More images found than exist in string")
            original_text = split_nodes_text[1]
            split_nodes.append(TextNode(split_nodes_text[0], "text"))
            if img:
                split_nodes.append(TextNode(link[0], "img", url=link[1]))
            else:
                split_nodes.append(TextNode(link[0], "link", url=link[1]))
        if original_text != '':
            split_nodes.append(TextNode(original_text, "text"))
        new_nodes += split_nodes

    return new_nodes


def text_to_nodes(text):
    nodes = [TextNode(text)]
    # IMPORTANT!  NOTE: While currently, no recursion, bold should come FIRST
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    # IMPORTANT!  NOTE: link regex pattern
    #               is strictly contained by image pattern, images come FIRST
    nodes = split_nodes_link(nodes, img=True)
    nodes = split_nodes_link(nodes)

    return nodes
