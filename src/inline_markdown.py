import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Invalid Markdown syntax provided")
            for i, part in enumerate(parts):
                if len(part) != 0:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                original_text = node.text
                for image_alt, image_url in images:
                    image_markdown = f"![{image_alt}]({image_url})"
                    sections = original_text.split(image_markdown, 1)
                    if len(sections) != 2:
                        raise Exception("invalid markdown, image section not closed")
                    if len(sections[0]) != 0:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
                    original_text = sections[1]
                if original_text != "":
                    new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                original_text = node.text
                for link_text, link_url in links:
                    link_markdown = f"[{link_text}]({link_url})"
                    sections = original_text.split(link_markdown, 1)
                    if len(sections) != 2:
                        raise Exception("invalid markdown, link section not closed")
                    if len(sections[0]) != 0:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                    original_text = sections[1]
                if original_text != "":
                    new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    new_nodes1 = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    new_nodes2 = split_nodes_delimiter(new_nodes1, "_", TextType.ITALIC)
    new_nodes3 = split_nodes_delimiter(new_nodes2, "`", TextType.CODE)
    new_nodes4 = split_nodes_image(new_nodes3)
    new_nodes5 = split_nodes_link(new_nodes4)
    return new_nodes5
