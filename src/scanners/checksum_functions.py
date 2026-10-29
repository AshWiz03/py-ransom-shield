import hashlib
import os

global checksum_dir
def calculate_checksum(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def write_checksum_file(file_path, checksum):
    try:
        with open(os.path.join(checksum_dir, file_path + ".checksum"), 'w') as f:
            f.write(checksum)
    except Exception as e:
        print(f"Error writing checksum for file '{file_path}': {str(e)}\n")
def read_checksum_file(checksum_file):
    try:
        with open(os.path.join(checksum_dir, checksum_file), 'r') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading checksum file '{checksum_file}': {str(e)}\n")
        return None
    
checksum_dir = r"..\backuplocation\checksum"