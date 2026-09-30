from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    strip_blocks = []
    for block in blocks:
        stripped = block.strip(" \n")
        if len(stripped) == 0:
            continue
        strip_blocks.append(stripped)
    return strip_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    is_unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    counter = 1
    for line in lines:
        if not line.startswith(f"{counter}. "):
            is_ordered_list = False
            break
        else:
            counter += 1
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

# Helper function for all block types, converting a string of text and returns a list of HTMLNodes
def text_to_children(block):
    leafnode_list = []
    # Normalize the string input, removing newlines and replacing them with spaces
    # This is to create an HTML (web) style of dynamic page formatting
    normalized = " ".join(block.split("\n"))
    # Parses inline markdown into TextNode
    text_nodes = text_to_textnodes(normalized)
    # Loop over text_nodes, convert each to an HTMLNode va text_node_to_html_node, and collect into leafnode_list
    for text_node in text_nodes:
        leafnode = text_node_to_html_node(text_node)
        leafnode_list.append(leafnode)
    return leafnode_list

# Helper function to create the correct heading level tag for ParentNode ( using an F-string)
# And to contain the remaining heading with the leading "#" stripped from it to parse into text_to_children(block)
def heading_level_from_block(block):
    level = 0
    i = 0
    while i < len(block) and block[i] == "#":
        level += 1
        i += 1
    tag = f"h{level}"
    block_text = (block[i:]).strip(" ")
    return tag, block_text

def quote_from_block(block):
    # Remove the leading "> " from each line in the block
    # This is to create an HTML (web) style of dynamic page formatting
    lines = []
    for line in block.split("\n"):
        if line.startswith("> "):
            lines.append(line[2:].strip(" "))
    return "\n".join(lines)

def unordered_list_from_block(block):
    # Remove the leading "- " from each line in the block
    # This is to create an HTML (web) style of dynamic page formatting
    # This function returns a list of ParentNode objects with tag "li" and children as the text_to_children of the line
    lines = []
    for line in block.split("\n"):
        if line.startswith("- "):
            lines.append(ParentNode(tag="li", children=text_to_children(line[2:].strip(" "))))
    return lines

def ordered_list_from_block(block):
    # Remove the leading "1. ", "2. ", etc. from each line in the block
    # This is to create an HTML (web) style of dynamic page formatting
    # This function returns a list of ParentNode objects with tag "li" and children as the text_to_children of the line
    lines = []
    counter = 1
    for line in block.split("\n"):
        if line.startswith(f"{counter}. "):
            lines.append(ParentNode(tag="li", children=text_to_children(line.split(". ", 1)[1].strip(" "))))
            counter += 1
    return lines

def code_from_block(block):
    # Remove the leading and trailing "```" from the block
    # This is to create an HTML (web) style of dynamic page formatting
    # This function returns a ParentNode object with tag "pre" and a child ParentNode object with tag "code" and a child LeafNode object with the text of the code block
    cleaned_text = block.removeprefix("```").removesuffix("```").removeprefix("\n")
    text_node = TextNode(cleaned_text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode(tag="code", children=[html_node])
    pre_node = ParentNode(tag="pre", children=[code_node])
    return pre_node

def markdown_to_html_node(markdown):
    # Splits markdown text into blocks, where there are double newlines.
    # Strips out spaces and single-newlines
    blocks = markdown_to_blocks(markdown)
    parentnode_list = []
    for block in blocks:
        # Determine the type of block (paragraph, heading, code, quote, unordered list, ordered list)
        block_type = block_to_block_type(block)        
        # Uses helper function to pass the heading level tag, and block of text        
        if block_type == BlockType.HEADING:
            # Calls helper function to pass the heading level tag, and block of text with the leading "#" stripped from it to parse into text_to_children(block)
            tag, block_text = heading_level_from_block(block)
            parentnode_list.append(ParentNode(tag=tag, children=text_to_children(block_text)))
        elif block_type == BlockType.QUOTE:
            # Calls helper function to remove the leading "> " from each line in the block
            block_text = quote_from_block(block)
            parentnode_list.append(ParentNode(tag="blockquote", children=text_to_children(block_text)))
        elif block_type == BlockType.UNORDERED_LIST:
            parentnode_list.append(ParentNode(tag="ul", children=unordered_list_from_block(block)))
        elif block_type == BlockType.ORDERED_LIST:
            parentnode_list.append(ParentNode(tag="ol", children=ordered_list_from_block(block)))
        elif block_type == BlockType.CODE:
            parentnode_list.append(code_from_block(block))
        else:
            # block_type == BlockType.PARAGRAPH            
            parentnode_list.append(ParentNode(tag="p", children=text_to_children(block)))
    return ParentNode(tag="div", children=parentnode_list)