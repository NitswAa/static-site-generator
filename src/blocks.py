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
        if line[0] != '*':
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


def block_to_block_type_complex(block):
    if not block:
        raise ValueError("Empty block")
    if block[0] == '#':
        if '\n' not in block:
            return "heading"

    if len(block) > 5 and block[:3] == "```" and block[-3:] == "```":
        return "code"

    qu_flag = True
    for line in block.split('\n'):
        if line[0] != '>':
            qu_flag = False
    if qu_flag:
        return "quote"

    ul_flag = True
    for line in block.split('\n'):
        if line[0] != '*':
            ul_flag = False
    if ul_flag:
        return "ul"

    ol_flag = True
    count = 1
    for line in block.split('\n'):
        if len(line) <= 1:
            ol_flag = False
            continue
        if line[:2] != f"{count}.":
            ol_flag = False
        count += 1
    if ol_flag:
        return "ol"

    return "paragraph"
