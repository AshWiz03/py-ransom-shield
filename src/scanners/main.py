# Import functions from other files
from scanning_functions import scan

# Directory paths (modify as needed)
backuplocation = r"..\backuplocation"
quarantine_location = r"..\QUARANTINE"
scanned_dir = r"..\scanned"
checksum_dir = r"..\backuplocation\checksum"
mapping_file = r"..\backuplocation\backup_mapping.txt"

# Main program logic
directory = input("Enter the path of the directory to backup: ")

# Get user input for scan type
scan_type = input("Enter 'quick' or 'complete' scan: ").strip().lower()

if scan_type == 'quick':
  scan(directory, 10, backuplocation, quarantine_location, scanned_dir) #10 is the % of files to be scanned
else:
  scan(directory,100, backuplocation, quarantine_location,scanned_dir)
