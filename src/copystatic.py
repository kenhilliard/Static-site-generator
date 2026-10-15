import os
import shutil

def delete_directory(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

def copy_files_recursive(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    entries = os.listdir(source)
    for item in entries:
        source_path = os.path.join(source, item)
        if os.path.isfile(source_path):
            print(f"Copying file from {source_path} to {destination}")
            shutil.copy(source_path, destination)
        else:
            destination_path = os.path.join(destination, item)
            print(f"Entering directory {source_path} -> {destination_path}")
            copy_files_recursive(source_path, destination_path)

