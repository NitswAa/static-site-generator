from textnode import text_to_nodes
from htmlnode import LeafNode, ParentNode


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
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case "img":
            if not text_node.url:
                raise ValueError("No image source for img tag!")
            return LeafNode(tag="img", value=text_node.text, props={"src": text_node.url})
        case _:
            raise ValueError("Invalid text type!")


def extract_title(title_line):
    if title_line[:2] != '# ':
        raise ValueError("All generated pages must have an h1 title!")

    return title_line.lstrip('# ')


def markdown_to_blocks(markdown):
    return list(filter(lambda x: x != '',
                       map(lambda x: x.strip(), markdown.split('\n\n'))))


def block_to_block_type(block):
    if not block:
        raise ValueError("Empty block")
    if block[0] == '#':
        if '\n' not in block:
            return "heading"

    if len(block) > 5 and block[:3] == "```" and block[-3:] == "```":
        return "code"

    qu_flag = True
    ul_flag = True
    ol_flag = True
    loop_count = 1
    for line in block.split('\n'):
        if line[0] != '>':
            qu_flag = False
        if line[0] != '*' and line[0] != '-':
            ul_flag = False
        if len(line) <= 1 or line[:2] != f"{loop_count}.":
            ol_flag = False
        loop_count += 1
        if not qu_flag and not ul_flag and not ol_flag:
            return "paragraph"
    if qu_flag:
        return "quote"
    elif ul_flag:
        return "ul"
    else:
        return "ol"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    # print(f"BLOCKS: {blocks}")
    children = map(lambda block: block_to_html(block), blocks)
    return ParentNode(tag="div", children=list(children))


# Returns one ParentNode with inline LeafNode children
def block_to_html(block):
    type = block_to_block_type(block)

    match type:
        case "paragraph":
            return paragraph_to_html(block)
        case "heading":
            return header_to_html(block)
        case "code":
            return code_to_html(block)
        case "quote":
            return quote_to_html(block)
        case "ul":
            return ul_to_html(block)
        case "ol":
            return ol_to_html(block)
        case _:
            raise ValueError("Invalid block type")


def paragraph_to_html(block):
    leaf_text_nodes = map(
        lambda node: text_node_to_html_node(node), text_to_nodes(block))
    # print(f"PARAGRAPH BLOCK: {list(leaf_text_nodes)}")
    return ParentNode(tag="p", children=list(leaf_text_nodes))


def header_to_html(block):
    # count header elements
    assert (block[0] == '#')
    pounds = 1
    while block[pounds] == '#':
        pounds += 1

    leaf_text_nodes = map(
        lambda node: text_node_to_html_node(node), text_to_nodes(block.lstrip('# ')))
    return ParentNode(tag=f"h{pounds}", children=list(leaf_text_nodes))


def code_to_html(block):
    child_node = [LeafNode(tag="code", value=block.strip('`'))]
    return ParentNode(tag="pre", children=child_node)


def quote_to_html(block):
    leaf_text_nodes = map(
        lambda node: text_node_to_html_node(node), text_to_nodes(''.join(block.split('> '))))
    return ParentNode(tag="blockquote", children=list(leaf_text_nodes))


def ul_to_html(block):
    subnodes = map(lambda line: ParentNode(
        tag="li", children=list(map(lambda node: text_node_to_html_node(node), text_to_nodes(line.lstrip('*-'))))), block.split('\n'))
    return ParentNode(tag='ul', children=list(subnodes))


def ul_to_html_dep(block):
    leaf_text_nodes = map(lambda node_text: LeafNode(
        tag="li", value=node_text.strip()), block.lstrip('*-'))
    return ParentNode(tag="ul", children=list(leaf_text_nodes))


def ol_to_html(block):
    subnodes = map(lambda line: ParentNode(tag='li', children=list(map(lambda node: text_node_to_html_node(node), text_to_nodes(
        line.lstrip('0123456789.').lstrip(' '))))), block.split('\n'))
    return ParentNode(tag='ol', children=list(subnodes))


def ol_to_html_dep(block):
    leaf_text_nodes = map(lambda node_text: LeafNode(
        tag="li", value=node_text.strip()), block.split('.')[1:])
    return ParentNode(tag="ol", children=list(leaf_text_nodes))


if __name__ == "__main__":
    text = """# The Unparalleled Majesty of "The Lord of the Rings"

[Back Home](/)

![LOTR image artistmonkeys](/images/rivendell.png)

> "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
> I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
> I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."

In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in *The Lord of the Rings*. You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page).

## Introduction

This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its *legendarium*. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world.

## A Rich Tapestry of Lore

One cannot simply discuss *The Lord of the Rings* without acknowledging the bedrock upon which it stands: **The Silmarillion**. This compendium of mythopoeic tales sets the stage for Middle-earth's history, from the creation myth of Eä to the epic sagas of the Elder Days. It is a testament to Tolkien's unparalleled skill as a linguist and myth-maker, crafting:

1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
2. The tragic saga of the Noldor Elves
3. The rise and fall of great kingdoms such as Gondolin and Númenor

```
print("Lord")
print("of")
print("the")
print("Rings")
```

## The Art of **World-Building**"""

    print(markdown_to_html_node(text).to_html())
