from textnode import TextNode, TextType
from copystatic import delete_public, copy_files_recursive
from gencontent import extract_title, generate_page, generate_pages_recursive

def main():
    delete_public("./public")
    copy_files_recursive("./static", "./public")
    generate_pages_recursive("./content/", "./template.html", "./public/")
main()
