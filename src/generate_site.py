from markdown_to_html_node import markdown_to_html_node
from pathlib import Path

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    
    raise Exception("No h1 header found")



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    from_file = ""
    template_file = ""
    
    with open(from_path, "r") as f:
        from_file = f.read()
    
    with open(template_path, "r") as f:
        template_file = f.read()
    
    html_site = markdown_to_html_node(from_file).to_html()
    
    title = extract_title(from_file)
    print(title)
    final_file = template_file.replace("{{ Title }}", title)
    final_file = final_file.replace("{{ Content }}", html_site)
    print(final_file)
    
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(final_file)
    
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
     
    for md_file in dir_path_content.rglob("*.md"):
        
        relative_path = md_file.relative_to(dir_path_content)
        dest_path = dest_dir_path / relative_path
        
        dest_path = dest_path.with_suffix(".html")
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        generate_page(md_file, template_path, dest_path)
