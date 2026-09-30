from textnode import TextNode, TextType
from copystatic import delete_public, copy_files_recursive

def main():
    delete_public("./public")
    copy_files_recursive("./static", "./public")
main()
