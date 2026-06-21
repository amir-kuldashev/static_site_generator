from htmlnode import HTMLNode
from extract_markdown import markdown_to_blocks
from blocks import block_to_block_type, BlockType
from textnode import text_node_to_html_node, TextNode, TextType
from text_to_textnode import text_to_textnodes
from htmlnode import ParentNode


def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.U_LIST:
                children.append(ul_to_html_node(block))
            case BlockType.O_LIST:
                children.append(ol_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
    return ParentNode("div", children, None)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    
    children = text_to_children(paragraph)
    
    return ParentNode("p", children)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    
    content = " ".join(new_lines)
    
    children = text_to_children(content)
    
    return ParentNode("blockquote", children)


def heading_to_html_node(block):
    lines = block.split("\n")
    heading = " ".join(lines)

    count = 0
    
    while heading.startswith("#"):
        count += 1
        heading = heading[1:]
    
    heading = heading.strip()
    children = text_to_children(heading)
    
    return ParentNode(f"h{count}",children)        


def ul_to_html_node(block):
    lines = block.split("\n")
    children = []

    for line in lines:
        line = line[2:]
        child = text_to_children(line.strip()) 
        children.append(ParentNode("li", child))
    
    
    return ParentNode("ul", children)
    
    
def ol_to_html_node(block):
    lines = block.split("\n")
    children = []

    for line in lines:
        parts = line.split(" ", 1)
        
        child = text_to_children(parts[1]) 
        children.append(ParentNode("li", child))
    
    
    return ParentNode("ol", children)
    
def code_to_html_node(block):
    clean_code = block[4:-3]
    
    text_node = TextNode(clean_code, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_node])
    
    return ParentNode("pre", [code_node])

    