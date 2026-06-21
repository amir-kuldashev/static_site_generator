from extract_markdown import split_nodes_image, split_nodes_link
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    
    ready = split_nodes_image([node])
    ready = split_nodes_link(ready)
    ready = split_nodes_delimiter(ready, "**", TextType.BOLD)
    ready = split_nodes_delimiter(ready, "_", TextType.ITALIC)
    ready = split_nodes_delimiter(ready, "`", TextType.CODE)
    
    return ready

