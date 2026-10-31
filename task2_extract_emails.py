"""
TASK 2: Email Extractor - Extract all email addresses from a .txt file and save them to another file.
Key Concepts: re (Regular Expressions), file handling (open, read, write), os.
"""

import os
import re
import argparse
from datetime import datetime


# Robust RFC-compliant regex for matching email addresses in unstructured text
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'


def clean_email(email_str):
    """Strip common trailing punctuation that might get captured from sentences."""
    return email_str.rstrip('.,;:!?"\')]}').lower()


def extract_emails(input_filepath, output_filepath):
    """
    Reads an input text file, extracts all valid email addresses using regex,
    deduplicates them, and writes the sorted results to an output file.

    Args:
        input_filepath (str): Path to the source text file.
        output_filepath (str): Path to write the extracted emails.

    Returns:
        dict: Summary statistics including unique emails found.
    """
    print("\n" + "=" * 60)
    print(">> TASK 2: EMAIL ADDRESS EXTRACTOR")
    print("=" * 60)
    print(f" Source File : {os.path.abspath(input_filepath)}")
    print(f" Output File : {os.path.abspath(output_filepath)}")
    print("-" * 60)

    # 1. Validation: Verify input file exists
    if not os.path.exists(input_filepath):
        print(f"[-] Error: Input file not found: {input_filepath}")
        return {"success": False, "error": "Input file not found"}

    if not os.path.isfile(input_filepath):
        print(f"[-] Error: Specified input path is not a file: {input_filepath}")
        return {"success": False, "error": "Input path is not a file"}

    start_time = datetime.now()

    # 2. File Handling: Read source text
    try:
        with open(input_filepath, 'r', encoding='utf-8', errors='ignore') as infile:
            content = infile.read()
    except Exception as e:
        print(f"[-] Error reading file: {e}")
        return {"success": False, "error": str(e)}

    # 3. Regular Expression: Find all email matches
    raw_matches = re.findall(EMAIL_REGEX, content)

    # Clean and deduplicate (preserving unique lowercased emails)
    unique_emails = sorted(list({clean_email(m) for m in raw_matches if clean_email(m)}))

    # 4. File Handling: Write results to output file
    output_dir = os.path.dirname(output_filepath)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write("=" * 60 + "\n")
            outfile.write(" EXTRACTED EMAIL ADDRESSES REPORT\n")
            outfile.write("=" * 60 + "\n")
            outfile.write(f"Source File   : {os.path.basename(input_filepath)}\n")
            outfile.write(f"Extracted On  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write(f"Total Matches : {len(raw_matches)}\n")
            outfile.write(f"Unique Emails : {len(unique_emails)}\n")
            outfile.write("-" * 60 + "\n\n")

            if unique_emails:
                for idx, email in enumerate(unique_emails, 1):
                    outfile.write(f"{idx:3d}. {email}\n")
            else:
                outfile.write("No email addresses were found in the source file.\n")

            outfile.write("\n" + "=" * 60 + "\n")
    except Exception as e:
        print(f"[-] Error writing output file: {e}")
        return {"success": False, "error": str(e)}

    elapsed = (datetime.now() - start_time).total_seconds()

    # 5. Console Summary
    print(f"[*] Total raw matches found : {len(raw_matches)}")
    print(f"[+] Unique emails extracted : {len(unique_emails)}")
    if unique_emails:
        print("\nExtracted Emails:")
        for idx, email in enumerate(unique_emails, 1):
            print(f"   {idx:2d}. {email}")

    print("-" * 60)
    print(f"[SUCCESS] Saved to   : {output_filepath}")
    print(f"[INFO]    Completed in: {elapsed:.3f}s")
    print("=" * 60 + "\n")

    return {
        "success": True,
        "total_raw": len(raw_matches),
        "unique_count": len(unique_emails),
        "emails": unique_emails,
        "output_file": output_filepath,
        "elapsed_seconds": elapsed
    }


def main():
    parser = argparse.ArgumentParser(description="Extract all email addresses from a text file.")
    parser.add_argument("--input", "-i", default="sample_data/sample_text.txt", help="Input text file path")
    parser.add_argument("--output", "-o", default="sample_data/extracted_emails.txt", help="Output text file path")

    args = parser.parse_args()
    extract_emails(args.input, args.output)


if __name__ == "__main__":
    main()
