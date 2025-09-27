from block import markdown_to_html_node
from htmlnode import HTMLNode

import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    
    raise Exception("did not find h1 header in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
        md_content = from_file.read()
        with open(template_path, "r") as template_file:
            template_content = template_file.read()
            html_content = markdown_to_html_node(md_content).to_html()
            title = extract_title(md_content)
            document = template_content.replace(r"{{ Title }}", title)
            document = document.replace(r"{{ Content }}", html_content)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w") as output_file:
                output_file.write(document)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for d in os.listdir(dir_path_content):
        new_content_path = os.path.join(dir_path_content, d)
        new_path = os.path.join(dest_dir_path, d)
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        if os.path.isfile(new_content_path):
            with open(new_content_path, "r") as from_file:
                md_content = from_file.read()
                with open(template_path, "r") as template_file:
                    template_content = template_file.read()
                    html_content = markdown_to_html_node(md_content).to_html()
                    title = extract_title(md_content)
                    document = template_content.replace(r"{{ Title }}", title)
                    document = document.replace(r"{{ Content }}", html_content)
                    new_html_path = new_path.replace(".md", ".html")
                    with open(new_html_path, "w") as output_file:
                        output_file.write(document)
        else:
            generate_page_recursive(new_content_path, template_path, new_path)
    
