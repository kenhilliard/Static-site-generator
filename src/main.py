from textnode import TextNode, TextType
from copystatic import delete_directory, copy_files_recursive
from gencontent import extract_title, generate_pages_recursive
import sys

def main():
    delete_directory("./docs")
    copy_files_recursive("./static", "./docs")
    # Set basepath default value, incase only 1 argument is provided
    basepath = "/"
    # Check if a command-line argument was provided
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    # Pass basepath to generate_pages_recursive and generate_page functions
    generate_pages_recursive("./content/", "./template.html", "./docs/", basepath)
    # build the site into the docs directory instead of public, and update main.sh to serve docs for local testing.
    
main()
