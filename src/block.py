from enum import Enum

import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from text_to_textnode import text_to_textnodes
from textnode_to_htmlnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    sections = list(
        filter(
            lambda line: line != "",
            map(
                lambda line: line.strip(),
                markdown.split("\n\n")
            )
        )
    )
    return sections

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.PLAIN_TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

################## <UTILS> ####################

# def get_htmlnode(tag, value, children):
#     if children:
#         return ParentNode(tag, children)
#     else:
#         return LeafNode(tag, value)

# def text_to_children(block, block_type):
#     if block_type == BlockType.CODE:
#         return None 

#     texts = block.split("\n")
#     if block_type == BlockType.QUOTE:
#         texts = [l[2:] for l in texts]
#         children = []
#         for text in texts:
#             text_nodes = text_to_textnodes(text)
#             html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
#             children.extend(html_nodes)
#         return children
#     elif block_type == BlockType.UNORDERED_LIST:
#         texts = [l[2:] for l in texts]
#         children = []
#         for text in texts:
#             text_nodes = text_to_textnodes(text) 
#             html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
#             list_item_parent = ParentNode("li", html_nodes)
#             children.append(list_item_parent)
#         return children
#     elif block_type == BlockType.ORDERED_LIST:
#         texts = [l[3:] for l in texts]
#         children = []
#         for text in texts:
#             text_nodes = text_to_textnodes(text) 
#             html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
#             list_item_parent = ParentNode("li", html_nodes)
#             children.append(list_item_parent)
#         return children
#     elif block_type == BlockType.PARAGRAPH:
#         text = block.lstrip("\n").rstrip("\n")
#         text = text.replace("\n", " ")
#         text_nodes = text_to_textnodes(text)
#         return [text_node_to_html_node(text_node) for text_node in text_nodes]
    
    

# ################## </UTILS> ####################

# def markdown_to_html_node(markdown):
#     blocks = markdown_to_blocks(markdown)
#     document_nodes = []
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         children = text_to_children(block, block_type)
#         block_node = None
#         match block_type:
#             case BlockType.PARAGRAPH:
#                 block_node = get_htmlnode("p", block, children)
#             case BlockType.HEADING: 
#                 hashtags = block.split(" ", 1)[0]
#                 heading_level = f"h{len(hashtags)}"
#                 block_node = get_htmlnode(heading_level, block, children)
#             case BlockType.CODE: 
#                 text = block[3:-3]
#                 text = text.lstrip("\n")
#                 block_node = TextNode(text, TextType.CODE_TEXT)
#                 block_node = text_node_to_html_node(block_node)
#                 block_node = ParentNode("pre", [block_node])
#             case BlockType.QUOTE: 
#                 block_node = ParentNode("blockquote", children)
#             case BlockType.UNORDERED_LIST: 
#                 block_node = ParentNode("ul", children)
#             case BlockType.ORDERED_LIST: 
#                 block_node = ParentNode("ol", children)
#         document_nodes.append(block_node)

#     return ParentNode("div", document_nodes)

