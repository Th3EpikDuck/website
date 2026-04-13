import os
import shutil

from textnode import TextNode, TextType, markdown_to_html_node
from htmlnode import HTMLNode
from pathlib import Path

def copyStaticToPublic(source, destination):
    # Deletes ALL files in the destination if it exists (pray it does exist)
    if os.path.exists(destination):
        print(f"Cleaning all the files in {destination} rn")
        for item in os.listdir(destination):
            item_path = os.path.join(destination, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    else:
        print("Could be an error but idk")
        print("Wait i forgot, it is an error please forsake me i hate my life")
        print("Nevermind, take this simple os and leave me alone")
        os.makedirs(destination, exist_ok=True)

    # Copies ALl files in the source to the destination
    def copy_recursive(current_source, current_destination):
        if not os.path.exists(current_destination):
            print("Fuck how??? This runs after the deletion. My computer on lsd and amphentamine again")
            print("This drugged computer can still retify the issue lol")
            os.makedirs(current_destination)

        for item in os.listdir(current_source):
            s = os.path.join(current_source, item)
            d = os.path.join(current_destination, item)

            if os.path.isdir(s):
                os.makedirs(d, exist_ok=True)
                copy_recursive(s, d)
            else:
                print(f"Copying: {s} -> {d}")
                shutil.copy2(s, d)

    copy_recursive(source, destination)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()

    raise Exception("Unfortunately, the h1 header has either disappeared or it never existed... probably the second one")

def generate_page(from_path, template_path, destination_path):
    print(f"Generating a path from {from_path} to the damn {destination_path} via the damn {template_path}")
    
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Markdown file has either disappeared or been forsaken: {from_path}")
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file has either disappeared or been forsaken: {template_path}")
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    content_html = html_node.to_html()

    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", content_html)

    dest_dir = os.path.dirname(destination_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(destination_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

def generate_pages_recursive(content_dir, template_path, dest_dir):
    for entry in os.listdir(content_dir):
        entry_path = os.path.join(content_dir, entry)
        dest_path = os.path.join(dest_dir, entry)

        if os.path.isdir(entry_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, dest_path)

        elif os.path.isfile(entry_path) and entry_path.endswith(".md"):
            html_dest = Path(dest_path).with_suffix(".html")
            print(f"Generating {html_dest} from {entry_path}")
            generate_page(entry_path, template_path, html_dest)

# Main
def main():
    print("hello world")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    copyStaticToPublic("static", "public")
    generate_pages_recursive("content", "src/template.html", "public")
main()
