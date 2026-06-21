from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "list"
    O_LIST = "ordered_list"

def block_to_block_type(text):
    lines = text.split("\n")
    if text.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    
    if text[:4] == "```\n" and text[-3:] == "```":
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.U_LIST
    
    flag = True
    for i in range(len(lines)):
        if lines[i][:3] != f"{i+1}. ":
            flag = False
            break
    
    if flag:
        return BlockType.O_LIST
    
    return BlockType.PARAGRAPH

