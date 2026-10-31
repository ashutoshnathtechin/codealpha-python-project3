"""
TASK 1: File Organizer - Move all .jpg files from a folder to a new folder.
Key Concepts: os, shutil, file handling, error handling.
"""

import os
import shutil
import argparse
from datetime import datetime


def get_unique_destination_path(destination_dir, filename):
    """
    Ensure no file is accidentally overwritten by generating a unique name
    if a file with the same name already exists in destination.
    E.g., 'image.jpg' -> 'image_1.jpg' -> 'image_2.jpg'.
    """
    base_name, ext = os.path.splitext(filename)
    dest_path = os.path.join(destination_dir, filename)
    counter = 1

    while os.path.exists(dest_path):
        new_filename = f"{base_name}_{counter}{ext}"
        dest_path = os.path.join(destination_dir, new_filename)
        counter += 1

    return dest_path


def move_jpg_files(source_dir, destination_dir, extensions=None, copy_only=False):
    """
    Moves (or copies) all .jpg files from source_dir into destination_dir.

    Args:
        source_dir (str): Path to the source directory containing files.
        destination_dir (str): Path to the destination directory.
        extensions (tuple): File extensions to match (default: ('.jpg', '.jpeg')).
        copy_only (bool): If True, copies instead of moving.

    Returns:
        dict: Summary statistics of the operation.
    """
    if extensions is None:
        extensions = ('.jpg', '.jpeg')

    # Normalize extensions to lowercase
    extensions = tuple(ext.lower() for ext in extensions)

    print("\n" + "=" * 60)
    print(">> TASK 1: IMAGE FILE ORGANIZER (.jpg / .jpeg)")
    print("=" * 60)
    print(f" Source Folder     : {os.path.abspath(source_dir)}")
    print(f" Destination Folder: {os.path.abspath(destination_dir)}")
    print(f" Target Extensions : {', '.join(extensions)}")
    print(f" Operation Mode    : {'COPY' if copy_only else 'MOVE'}")
    print("-" * 60)

    # 1. Validation: Verify source directory exists
    if not os.path.exists(source_dir):
        print(f"[-] Error: Source directory does not exist: {source_dir}")
        return {"success": False, "error": "Source directory not found"}

    if not os.path.isdir(source_dir):
        print(f"[-] Error: Source path is not a directory: {source_dir}")
        return {"success": False, "error": "Source path is not a directory"}

    # 2. Setup: Ensure destination directory exists using os.makedirs
    os.makedirs(destination_dir, exist_ok=True)

    # 3. Scanning and Moving Files
    moved_count = 0
    skipped_count = 0
    errors = []
    start_time = datetime.now()

    all_items = os.listdir(source_dir)
    print(f"[*] Scanning {len(all_items)} item(s) in source folder...")

    for item in all_items:
        src_path = os.path.join(source_dir, item)

        # Only process files, skip sub-directories
        if not os.path.isfile(src_path):
            continue

        # Check if file has target extension (case-insensitive)
        _, ext = os.path.splitext(item)
        if ext.lower() in extensions:
            dest_path = get_unique_destination_path(destination_dir, item)
            actual_dest_name = os.path.basename(dest_path)

            try:
                if copy_only:
                    shutil.copy2(src_path, dest_path)
                    print(f"  [COPIED] {item} -> {actual_dest_name}")
                else:
                    shutil.move(src_path, dest_path)
                    print(f"  [MOVED]  {item} -> {actual_dest_name}")
                moved_count += 1
            except Exception as e:
                print(f"  [ERROR]  Could not process {item}: {e}")
                errors.append((item, str(e)))
        else:
            skipped_count += 1

    elapsed = (datetime.now() - start_time).total_seconds()

    # 4. Summary Report
    print("-" * 60)
    print(f"[SUCCESS] Completed in {elapsed:.3f}s")
    print(f"          Files Processed : {moved_count}")
    print(f"          Non-JPG Skipped : {skipped_count}")
    print(f"          Errors          : {len(errors)}")
    print("=" * 60 + "\n")

    return {
        "success": True,
        "moved_count": moved_count,
        "skipped_count": skipped_count,
        "errors": errors,
        "elapsed_seconds": elapsed
    }


def main():
    parser = argparse.ArgumentParser(description="Move all .jpg files from a source folder to a destination folder.")
    parser.add_argument("--source", "-s", default="sample_data/source_folder", help="Path to source folder")
    parser.add_argument("--dest", "-d", default="sample_data/organized_jpgs", help="Path to destination folder")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving them")

    args = parser.parse_args()
    move_jpg_files(args.source, args.dest, copy_only=args.copy)


if __name__ == "__main__":
    main()
