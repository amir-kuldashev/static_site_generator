import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    answer = re.findall(r"!\[(.*?)]\((.*?)\)", text)
    return answer

def extract_markdown_links(text):
    answer = re.findall(r"(?<!\!)\[(.*?)]\((.*?)\)", text)
    return answer

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:    
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        for name, link in images:
            splitted = original_text.split(f"![{name}]({link})",1)
            
            if len(splitted[0])>0:
                new_node = TextNode(splitted[0], old_node.text_type,old_node.url)
                new_nodes.append(new_node)
            
            new_node = TextNode(name, TextType.IMAGE, link)
            new_nodes.append(new_node)
            original_text = splitted[1]
        
        if len(original_text)>0:
            new_node = TextNode(original_text, old_node.text_type, old_node.url)
            new_nodes.append(new_node)
        
        
    return new_nodes        
    
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        for name, link in links:
            splitted = original_text.split(f"[{name}]({link})",1)
            
            if len(splitted[0])>0:
                new_node = TextNode(splitted[0], old_node.text_type, old_node.url)
                new_nodes.append(new_node)
            
            new_node = TextNode(name, TextType.LINK, link)
            new_nodes.append(new_node)
            original_text = splitted[1]
        
        if len(original_text)>0:
            new_node = TextNode(original_text, old_node.text_type,old_node.url)
            new_nodes.append(new_node)
        
        
    return new_nodes        


def markdown_to_blocks(text):
    splitted = text.split("\n\n")
    splitted_blocks = []
    for spl in splitted:
        spl = spl.strip()
        if spl == "" or spl == "\n":
            continue
        splitted_blocks.append(spl)
    
    return splitted_blocks
