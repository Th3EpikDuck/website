import os
import shutil

from textnode import TextNode, TextType

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

# Main
def main():
    print("hello world")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    copyStaticToPublic("static", "public")
main()
