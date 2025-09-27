from block import markdown_to_html_node
from generate_page import generate_page, generate_page_recursive

from pprint import pprint

import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    
    copy_files_recursive("./static", "./public")
    generate_page_recursive("./content", "template.html", "./public")
    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    # generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    # generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
