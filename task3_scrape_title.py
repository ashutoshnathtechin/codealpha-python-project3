"""
TASK 3: Web Scraper - Scrape the title of a fixed webpage and save it.
Key Concepts: requests, re (Regular Expressions), file handling, os, error handling.
"""

import os
import re
import html
import argparse
from datetime import datetime
import requests


# Default target webpage: stable, high-availability, developer-friendly
DEFAULT_URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"

# Standard browser User-Agent header to prevent 403 Forbidden on standard websites
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36 TaskAutomationBot/1.0"
    )
}


def scrape_webpage_title(target=DEFAULT_URL, output_filepath="sample_data/scraped_title.txt", timeout=10):
    """
    Fetches the HTML content of a fixed webpage (or local HTML file), extracts its
    <title> tag using regex, and saves the metadata and title to a designated output file.

    Args:
        target (str): Target webpage URL (http/https) or local HTML file path.
        output_filepath (str): File destination where the scraped title will be saved.
        timeout (int): Request timeout in seconds.

    Returns:
        dict: Scraped title and status details.
    """
    print("\n" + "=" * 60)
    print(">> TASK 3: WEBPAGE TITLE SCRAPER")
    print("=" * 60)
    print(f" Target      : {target}")
    print(f" Output File : {os.path.abspath(output_filepath)}")
    print(f" Timeout     : {timeout} seconds")
    print("-" * 60)

    start_time = datetime.now()
    status_info = "200 OK"
    content_size = 0

    # 1. Fetch Content: via requests for web URLs, or file handling for local HTML
    if target.startswith("http://") or target.startswith("https://"):
        try:
            print("[*] Fetching webpage content via requests...")
            response = requests.get(target, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            html_text = response.text
            status_info = f"{response.status_code} {response.reason}"
            content_size = len(response.content)
        except requests.exceptions.Timeout:
            print(f"[-] Error: Request timed out after {timeout} seconds.")
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.ConnectionError:
            print(f"[-] Error: Network connection failed. Check your internet access.")
            return {"success": False, "error": "Connection error"}
        except requests.exceptions.HTTPError as e:
            print(f"[-] HTTP Error encountered: {e}")
            return {"success": False, "error": f"HTTP error {response.status_code}"}
        except Exception as e:
            print(f"[-] Unexpected request error: {e}")
            return {"success": False, "error": str(e)}
    elif os.path.exists(target) and os.path.isfile(target):
        print("[*] Loading local HTML document...")
        try:
            with open(target, 'r', encoding='utf-8', errors='ignore') as f:
                html_text = f.read()
            status_info = "Local File (200 OK)"
            content_size = os.path.getsize(target)
        except Exception as e:
            print(f"[-] Error reading local HTML file: {e}")
            return {"success": False, "error": str(e)}
    else:
        print(f"[-] Error: Target is neither a valid URL nor an existing local file: {target}")
        return {"success": False, "error": "Target not found"}

    # 2. Extract Title using Regular Expressions (re)
    # Match <title>...</title> across single or multiple lines
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_text, re.IGNORECASE | re.DOTALL)

    if title_match:
        # Clean extracted title: strip whitespace and decode HTML entities like &amp; &#39;
        raw_title = title_match.group(1).strip()
        cleaned_title = html.unescape(re.sub(r'\s+', ' ', raw_title))
    else:
        cleaned_title = "No <title> tag found on this webpage"

    # Optional: Extract meta description if present
    meta_desc_match = re.search(
        r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        html_text,
        re.IGNORECASE
    )
    meta_description = html.unescape(meta_desc_match.group(1).strip()) if meta_desc_match else "N/A"

    elapsed = (datetime.now() - start_time).total_seconds()

    # 3. File Handling: Save scraped data to file
    output_dir = os.path.dirname(output_filepath)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write("=" * 60 + "\n")
            outfile.write(" WEBPAGE TITLE SCRAPING REPORT\n")
            outfile.write("=" * 60 + "\n")
            outfile.write(f"Scraped On       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write(f"Target           : {target}\n")
            outfile.write(f"Status           : {status_info}\n")
            outfile.write(f"Content Size     : {content_size:,} bytes\n")
            outfile.write(f"Execution Time   : {elapsed:.3f} seconds\n")
            outfile.write("-" * 60 + "\n")
            outfile.write(f"SCRAPED TITLE    : {cleaned_title}\n")
            outfile.write(f"META DESCRIPTION : {meta_description}\n")
            outfile.write("=" * 60 + "\n")
    except Exception as e:
        print(f"[-] Error writing output file: {e}")
        return {"success": False, "error": str(e)}

    # 4. Console Output
    print(f"[+] Extracted Title : {cleaned_title}")
    if meta_description != "N/A":
        print(f"[+] Description     : {meta_description[:75]}...")
    print(f"[*] Status          : {status_info} ({content_size:,} bytes)")
    print("-" * 60)
    print(f"[SUCCESS] Saved results to: {output_filepath}")
    print(f"[INFO]    Completed in    : {elapsed:.3f}s")
    print("=" * 60 + "\n")

    return {
        "success": True,
        "title": cleaned_title,
        "meta_description": meta_description,
        "status": status_info,
        "target": target,
        "output_file": output_filepath,
        "elapsed_seconds": elapsed
    }


def main():
    parser = argparse.ArgumentParser(description="Scrape the title of a webpage and save it to a file.")
    parser.add_argument("--url", "-u", default=DEFAULT_URL, help="Target webpage URL or local HTML file to scrape")
    parser.add_argument("--output", "-o", default="sample_data/scraped_title.txt", help="Output file path")
    parser.add_argument("--timeout", "-t", type=int, default=10, help="Request timeout in seconds")

    args = parser.parse_args()
    scrape_webpage_title(args.url, args.output, args.timeout)


if __name__ == "__main__":
    main()
