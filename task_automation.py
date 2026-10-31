"""
================================================================================
TASK 3: TASK AUTOMATION WITH PYTHON SCRIPTS - MASTER SUITE
================================================================================
Goal: Automate small, real-life repetitive tasks using standard Python tools.

Covered Core Ideas:
  1. Move all .jpg files from a folder to a new folder (os, shutil)
  2. Extract all email addresses from a .txt file and save them (re, file handling)
  3. Scrape the title of a fixed webpage and save it (requests, re, file handling)

Key Concepts Used: os, shutil, re, requests, file handling, argparse, error handling.
================================================================================
"""

import os
import sys
import argparse
from datetime import datetime

# Import sub-modules
from task1_move_jpg import move_jpg_files
from task2_extract_emails import extract_emails
from task3_scrape_title import scrape_webpage_title, DEFAULT_URL
from setup_sample_data import setup_sample_data


BANNER = r"""
======================================================================
  ____        _   _                   _         _                        
 |  _ \ _   _| |_| |__   ___  _ __   / \  _   _| |_ ___  _ __ ___   __ _ 
 | |_) | | | | __| '_ \ / _ \| '_ \ / _ \| | | | __/ _ \| '_ ` _ \ / _` |
 |  __/| |_| | |_| | | | (_) | | | / ___ \ |_| | || (_) | | | | | | (_| |
 |_|    \__, |\__|_| |_|\___/|_| |/_/   \_\__,_|\__\___/|_| |_| |_|\__,_|
        |___/                                                            
                TASK AUTOMATION SUITE - PYTHON
======================================================================
"""


def ensure_sample_environment():
    """Ensure that sample_data directory and test files exist before execution."""
    sample_dir = "sample_data"
    source_folder = os.path.join(sample_dir, "source_folder")
    sample_text = os.path.join(sample_dir, "sample_text.txt")

    if not (os.path.exists(source_folder) and os.path.exists(sample_text)):
        print("[*] Sample data files not detected. Generating test files automatically...")
        setup_sample_data(sample_dir)


def run_task_1(source=None, dest=None, copy_only=False):
    """Executes Task 1: Moving JPG files."""
    source = source or "sample_data/source_folder"
    dest = dest or "sample_data/organized_jpgs"

    # If source doesn't exist or is empty, regenerate sample data
    if not os.path.exists(source) or len(os.listdir(source)) == 0:
        ensure_sample_environment()

    return move_jpg_files(source, dest, copy_only=copy_only)


def run_task_2(input_path=None, output_path=None):
    """Executes Task 2: Extracting email addresses."""
    input_path = input_path or "sample_data/sample_text.txt"
    output_path = output_path or "sample_data/extracted_emails.txt"

    if not os.path.exists(input_path):
        ensure_sample_environment()

    return extract_emails(input_path, output_path)


def run_task_3(url=None, output_path=None):
    """Executes Task 3: Scraping webpage title."""
    target = url or DEFAULT_URL
    output_path = output_path or "sample_data/scraped_title.txt"

    result = scrape_webpage_title(target, output_path)
    
    # Graceful fallback: If network connection fails and sample HTML is present, demonstrate with sample HTML
    if not result.get("success") and os.path.exists("sample_data/sample_webpage.html"):
        print("[INFO] Network is unavailable in current environment.")
        print("[INFO] Demonstrating title extraction using local 'sample_data/sample_webpage.html'...")
        result = scrape_webpage_title("sample_data/sample_webpage.html", output_path)

    return result


def run_all_tasks():
    """Runs all three tasks in sequence to demonstrate complete automation."""
    print("\n" + "#" * 65)
    print(">>> RUNNING ALL AUTOMATION TASKS (FULL SUITE DEMO)")
    print("#" * 65)

    # Reset sample data to ensure fresh files for Task 1 and Task 2
    setup_sample_data("sample_data")

    results = {}
    print("\n>>> STEP 1/3: Organizing Image Files (.jpg / .jpeg)")
    results['task1'] = run_task_1()

    print("\n>>> STEP 2/3: Extracting Emails from Document")
    results['task2'] = run_task_2()

    print("\n>>> STEP 3/3: Scraping Webpage Title & Metadata")
    results['task3'] = run_task_3()

    print("\n" + "=" * 65)
    print("OVERALL AUTOMATION SUITE EXECUTION SUMMARY")
    print("=" * 65)
    t1_status = "[SUCCESS]" if results['task1'].get('success') else "[FAILED]"
    t2_status = "[SUCCESS]" if results['task2'].get('success') else "[FAILED]"
    t3_status = "[SUCCESS]" if results['task3'].get('success') else "[FAILED]"

    print(f" Task 1 (JPG File Mover)   : {t1_status} ({results['task1'].get('moved_count', 0)} files moved)")
    print(f" Task 2 (Email Extractor)  : {t2_status} ({results['task2'].get('unique_count', 0)} unique emails extracted)")
    title_preview = results['task3'].get('title', 'N/A')
    if len(title_preview) > 40:
        title_preview = title_preview[:40] + "..."
    print(f" Task 3 (Web Title Scraper): {t3_status} (Title: {title_preview})")
    print("=" * 65 + "\n")


def interactive_menu():
    """Interactive command-line interface for selecting and running tasks."""
    while True:
        print(BANNER)
        print("Choose an automation option to execute:")
        print("  [1] Task 1: Move all .jpg files from a folder to a new folder (os, shutil)")
        print("  [2] Task 2: Extract all email addresses from a .txt file (re, file handling)")
        print("  [3] Task 3: Scrape the title of a webpage and save it (requests, re)")
        print("  [4] Run All Tasks (Comprehensive Demonstration)")
        print("  [5] Regenerate / Reset Sample Test Data")
        print("  [0] Exit")
        print("-" * 70)

        choice = input("Enter your choice (0-5): ").strip()

        if choice == "1":
            custom = input("Use default sample folder? (Y/n): ").strip().lower()
            if custom == 'n':
                src = input("Enter source folder path: ").strip()
                dst = input("Enter destination folder path: ").strip()
                run_task_1(src, dst)
            else:
                run_task_1()
        elif choice == "2":
            custom = input("Use default sample text file? (Y/n): ").strip().lower()
            if custom == 'n':
                inp = input("Enter input text file path: ").strip()
                out = input("Enter output file path: ").strip()
                run_task_2(inp, out)
            else:
                run_task_2()
        elif choice == "3":
            custom = input("Use default Wikipedia Python URL? (Y/n): ").strip().lower()
            if custom == 'n':
                url = input("Enter webpage URL to scrape: ").strip()
                out = input("Enter output file path: ").strip()
                run_task_3(url, out)
            else:
                run_task_3()
        elif choice == "4":
            run_all_tasks()
        elif choice == "5":
            setup_sample_data("sample_data")
        elif choice in ("0", "exit", "q"):
            print("\nExiting Task Automation Suite. Goodbye!\n")
            break
        else:
            print("[!] Invalid choice. Please enter a number between 0 and 5.")

        input("\nPress Enter to return to main menu...")


def main():
    parser = argparse.ArgumentParser(
        description="Master Task Automation Script covering File Moving, Email Extraction, and Web Scraping."
    )
    parser.add_argument(
        "--task", "-t",
        choices=["1", "2", "3", "all"],
        help="Specify which task to run directly (1, 2, 3, or all)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run comprehensive demo across all 3 tasks"
    )

    args = parser.parse_args()

    # If run with command line flags
    if args.demo or args.task == "all":
        run_all_tasks()
    elif args.task == "1":
        run_task_1()
    elif args.task == "2":
        run_task_2()
    elif args.task == "3":
        run_task_3()
    else:
        # No CLI arguments provided, launch interactive menu
        try:
            interactive_menu()
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user. Exiting.\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
