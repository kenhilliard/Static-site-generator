import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path

def extract_title(markdown):
    # split a multi-lined markdown text into individual lines
    split_markdown = markdown.split("\n")
    for line in split_markdown:
        # check if each line is prefixed with "# "
        if line.startswith("# "):
            # if so, remove the prefix "# " from the line
            clean_prefix = line.removeprefix("# ")
            # return the line with leading/trailing whitespaces also removed
            return clean_prefix.strip()
    # if no prefix "# " is detected raise exception with an error
    raise Exception("No Heading Markdown Found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # opens the from_path file, and saves the generated path as the variable open_from_path
    # then reads the open file, storing the result in read_from_path
    with open(from_path) as open_from_path:
        read_from_path = open_from_path.read()
    # opens the template_path file, and saves the generated path as the variable open_template_path
    # then reads the open file, storing the result in read_template_path
    with open(template_path) as open_template_path:
        read_template_path = open_template_path.read()
    # convert the markdown text stored in variable read_from_path into an html string
    html_from_path = markdown_to_html_node(read_from_path).to_html()
    # extract the title of the html string, ready to insert into read_template_path
    html_title_from_path = extract_title(read_from_path)
    # replace the title and content placeholders in read_template_path with the converted html string (content), and extracted title (title)
    complete_html_from_path = read_template_path.replace("{{ Title }}", html_title_from_path).replace("{{ Content }}", html_from_path)
    # checks if the destination folder exists
    dest_path_folder = os.path.dirname(dest_path)
    # creates the folder if it doesn't exist, exception error if folder already exists is handled by os.makedirs
    os.makedirs(dest_path_folder, exist_ok=True)
    # write complete_html_from_path to the destination path provided
    with open(dest_path, "w") as dest_path_file:
        dest_path_file.write(complete_html_from_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # list the contents of the current path
    list_dir_path_content = os.listdir(dir_path_content)    
    for item in list_dir_path_content:
        # create the full path for the item in the content directory
        from_path = os.path.join(dir_path_content, item)
        # create the full path for the item in the destination directory
        dest_path = os.path.join(dest_dir_path, item)
        # check each item in the path list to see if it is a file or a folder
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            # if the item is a file, generate a page using the from_path, template_path, and dest_path
            generate_page(from_path, template_path, dest_path)
        else:
            # if the item is a folder, recursively call the function to generate pages for the contents of the folder
            generate_pages_recursive(from_path, template_path, dest_path)
