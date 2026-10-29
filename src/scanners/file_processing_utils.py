import os
import shutil

def get_all_files(directory):
    all_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename[-9:] != '.checksum':
                all_files.append(os.path.join(root, filename))
    return all_files
def copy_file(source_path, destination_path):
    try:
        shutil.copy(source_path, destination_path)
    except Exception as e:
        print(f"Error copying file '{source_path}': {str(e)}\n")
def move_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
    except Exception as e:
        print(f"Error moving file '{source_path}': {str(e)}\n")