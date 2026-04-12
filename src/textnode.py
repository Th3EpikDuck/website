import re

from enum import Enum
from htmlnode import LeafNode
from htmlnode import ParentNode
from typing import List, Dict

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

# Stuff below (not connected to any class)
def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: Missing closing delimiter '{delimiter}' in text: {old_node.text}")
            
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
                
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    for node in old_nodes:
        if isinstance(node, dict):
            if node.get("type") != "text":
                new_nodes.append(node)
                continue

            text = node.get("text", "")
            last_index = 0

            for match in image_pattern.finditer(text):
                start, end = match.span()
                alt_text, url = match.groups()

                if start > last_index:
                    new_nodes.append({"type": "text", "text": text[last_index:start]})

                new_nodes.append({"type": "image", "alt": alt_text, "url": url})
                last_index = end

            if last_index < len(text):
                new_nodes.append({"type": "text", "text": text[last_index:]})
        else:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue

            text = node.text
            last_index = 0

            for match in image_pattern.finditer(text):
                start, end = match.span()
                alt_text, url = match.groups()

                if start > last_index:
                    new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                last_index = end

            if last_index < len(text):
                new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for node in old_nodes:
        if isinstance(node, dict):
            if node.get("type") != "text":
                new_nodes.append(node)
                continue

            text = node.get("text", "")
            last_index = 0

            for match in link_pattern.finditer(text):
                start, end = match.span()
                link_text, url = match.groups()

                if start > last_index:
                    new_nodes.append({"type": "text", "text": text[last_index:start]})

                new_nodes.append({"type": "link", "text": link_text, "url": url})
                last_index = end

            if last_index < len(text):
                new_nodes.append({"type": "text", "text": text[last_index:]})

        else:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue

            text = node.text
            last_index = 0

            for match in link_pattern.finditer(text):
                start, end = match.span()
                link_text, url = match.groups()

                if start > last_index:
                    new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))

                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                last_index = end

            if last_index < len(text):
                new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            cleaned_blocks.append(stripped)
    return cleaned_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    # Heading
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and block[count] == " ":
            return BlockType.HEADING

    # Code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote
    if all(line.startswith(">") for line in lines if line):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    is_ordered = True
    for i, line in enumerate(lines):
        expected = f"{i+1}. "
        if not line.startswith(expected):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            content = " ".join(line.strip() for line in block.split("\n"))
            block_nodes.append(ParentNode("p", text_to_children(content)))
            
        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#": level += 1
                else: break
            content = block[level + 1:]
            block_nodes.append(ParentNode(f"h{level}", text_to_children(content)))
            
        elif block_type == BlockType.CODE:
            content = block[3:-3].strip()
            code_node = text_node_to_html_node(TextNode(content, TextType.TEXT))
            block_nodes.append(ParentNode("pre", [ParentNode("code", [code_node])]))
            
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            content = " ".join([line.lstrip("> ").strip() for line in lines])
            block_nodes.append(ParentNode("blockquote", text_to_children(content)))
            
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                content = line[2:]
                items.append(ParentNode("li", text_to_children(content)))
            block_nodes.append(ParentNode("ul", items))
            
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                content = line[line.find(". ") + 2:]
                items.append(ParentNode("li", text_to_children(content)))
            block_nodes.append(ParentNode("ol", items))

    return ParentNode("div", block_nodes)

