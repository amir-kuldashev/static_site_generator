from textnode import TextNode, TextType
import shutil
from pathlib import Path
from generate_site import generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv)>1:
        basepath = sys.argv[1]
    
    
    curr_dir = Path(__file__)
    
    src_dir = curr_dir.parent.parent / "static"
    dst_dir = curr_dir.parent.parent / "docs"
    temp_file = curr_dir.parent.parent / "template.html"
    content = curr_dir.parent.parent / "content"
    
    if dst_dir.is_dir():
        shutil.rmtree(dst_dir)
        
    dst_dir.mkdir(parents=True, exist_ok=True)
    
    shutil.copytree(src=src_dir, dst=dst_dir,dirs_exist_ok=True)
    
    
    
    generate_pages_recursive(content, temp_file, dst_dir, basepath)
    

    
    
if __name__ == "__main__":
    main()