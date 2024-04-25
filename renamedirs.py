import os
import re
import argparse

def rename_directories(root_dir):
    # Define mappings of directory names to new names
    mappings = {
        'act 1': 'Disc 1',
        'act 2': 'Disc 2',
        'act 3': 'Disc 3',
        'act one': 'Disc 1',
        'act two': 'Disc 2',
        'act three': 'Disc 3',
        'disc one': 'Disc 1',
        'disc two': 'Disc 2',
        'disc three': 'Disc 3',
        'act i': 'Disc 1',
        'act ii': 'Disc 2',
        'act iii': 'Disc 3'
    }

    # Traverse directories recursively
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            # Check if directory name matches any of the mappings
            for old_name, new_name in mappings.items():
                if re.match(f"^{old_name}$", dir_name, re.IGNORECASE):
                    old_path = os.path.join(root, dir_name)
                    new_path = os.path.join(root, new_name)
                    os.rename(old_path, new_path)
                    print(f"Renamed '{old_path}' to '{new_path}'")

def parse_args():
    parser = argparse.ArgumentParser(description="Recursively rename directories.")
    parser.add_argument("root_dir", nargs='?', default=os.getcwd(), help="Root directory to start renaming from. Defaults to the current directory.")
    return parser.parse_args()

def main():
    args = parse_args()
    rename_directories(args.root_dir)

if __name__ == "__main__":
    main()
