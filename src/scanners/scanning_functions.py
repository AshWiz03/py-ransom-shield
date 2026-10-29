import os
import math
import random
import zipfile

from file_processing_utils import get_all_files, copy_file, move_file
from checksum_functions import calculate_checksum, write_checksum_file, read_checksum_file
from file_encryption_checks import (
  is_pdf_encrypted, check_image_metadata, is_pptx_encrypted, is_docx_encrypted, is_xlsx_encrypted
)

def select_random_files(files_list, percentage):
    x=len(files_list)*percentage
    num_files = int(math.ceil((x/100)))
    return random.sample(files_list, num_files)

def map_directory(directory, depth=0, processed_dirs=set()):
    mapping = ""
    for root, dirs, files in os.walk(directory):
        indent = "  " * depth
        dir_name = os.path.basename(root)
        if dir_name not in processed_dirs:
            mapping += f"{indent}{dir_name}/\n"
            processed_dirs.add(dir_name)
        for filename in files:
            mapping += f"{indent}  {filename}\n"
        for d in dirs:
            sub_dir = os.path.join(root, d)
            mapping += map_directory(sub_dir, depth + 1, processed_dirs)
    return mapping

def get_directory_structure(directory):
    processed_dirs = set()
    return map_directory(directory, processed_dirs=processed_dirs)

def scan(directory, percentage, backuplocation, quarantine_location, scanned_dir):
    # Get all files in the directory
    all_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename[-9:] != '.checksum':
                all_files.append(os.path.join(root, filename))
    
    # Select random files for scanning
    if percentage == 100:
        files_to_scan = all_files
        print("Performing Complete scan")
    else:
        files_to_scan = select_random_files(all_files, percentage)
        print(files_to_scan)
    
    # Ensure scanned directory exists
    if not os.path.exists(scanned_dir):
        os.makedirs(scanned_dir)
    
    # Perform scanning and handling based on file types
    for file_path in files_to_scan:
        filename = os.path.basename(file_path)
        
        if filename.endswith('.pdf'):
            x = is_pdf_encrypted(file_path)
            if x == 1 or x == 0:
                copy_file(file_path, os.path.join(backuplocation, filename))
                checksum = calculate_checksum(file_path)
                write_checksum_file(filename, checksum)
                copy_file(file_path, os.path.join(scanned_dir, filename))
            elif x == 2:
                move_file(file_path, os.path.join(quarantine_location, filename))

        elif filename.endswith(('.jpg', '.png')):
            metadata = check_image_metadata(file_path)
            if metadata:
                copy_file(file_path, os.path.join(backuplocation, filename))
                checksum = calculate_checksum(file_path)
                write_checksum_file(filename, checksum)
                copy_file(file_path, os.path.join(scanned_dir, filename))
            else:
                move_file(file_path, os.path.join(quarantine_location, filename))

        elif filename.endswith('.zip'):
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    pass
                copy_file(file_path, os.path.join(backuplocation, filename))
                checksum = calculate_checksum(file_path)
                write_checksum_file(filename, checksum)
                copy_file(file_path, os.path.join(scanned_dir, filename))
            except Exception as e:
                move_file(file_path, os.path.join(quarantine_location, filename))

        elif filename.endswith('.pptx'):
            if not is_pptx_encrypted(file_path):
                copy_file(file_path, os.path.join(backuplocation, filename))
                checksum = calculate_checksum(file_path)
                write_checksum_file(filename, checksum)
                copy_file(file_path, os.path.join(scanned_dir, filename))
            else:
                move_file(file_path, os.path.join(quarantine_location, filename))

        elif filename.endswith('.docx'):
            if not is_docx_encrypted(file_path):
                copy_file(file_path, os.path.join(backuplocation, filename))
                checksum = calculate_checksum(file_path)
                write_checksum_file(filename, checksum)
                copy_file(file_path, os.path.join(scanned_dir, filename))
            else:
                move_file(file_path, os.path.join(quarantine_location, filename))

        elif filename.endswith('.xlsx'):
            if not is_xlsx_encrypted(file_path):
                copy_file(file_path, os.path.join(backuplocation, filename))
                checksum = calculate_checksum(file_path)
                write_checksum_file(filename, checksum)
                copy_file(file_path, os.path.join(scanned_dir, filename))
            else:
                move_file(file_path, os.path.join(quarantine_location, filename))

    original_filenames = set(os.path.basename(f) for f in get_all_files(directory))
    scanned_filenames = set(os.path.basename(f) for f in get_all_files(scanned_dir))
    print(original_filenames,end="/n")
    print(scanned_filenames)
    if original_filenames == scanned_filenames:
        for file_path in get_all_files(scanned_dir):
            os.remove(file_path)
        print(f"Scanned directory '{scanned_dir}' has been cleared as it matches the original directory.")
