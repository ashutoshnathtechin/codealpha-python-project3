"""
Helper script to generate sample test data for all automation tasks.
Creates:
  - sample_data/source_folder/ with dummy .jpg, .jpeg, .png, and .txt files.
  - sample_data/sample_text.txt with unstructured text containing various email addresses.
  - sample_data/sample_webpage.html with valid HTML structure for offline title scraping.
"""

import os


def setup_sample_data(base_dir="sample_data"):
    """Creates sample files and directories for testing the automation scripts."""
    print(f"[*] Setting up sample test environment in ./{base_dir}...")

    # 1. Setup Source Folder for Task 1 (Moving JPGs)
    source_folder = os.path.join(base_dir, "source_folder")
    os.makedirs(source_folder, exist_ok=True)

    # List of dummy files to create
    test_files = [
        ("vacation_photo.jpg", b"\xFF\xD8\xFF\xE0\x00\x10JFIF"),      # Fake JPEG header
        ("sunset_beach.jpg", b"\xFF\xD8\xFF\xE0\x00\x10JFIF"),
        ("family_portrait.jpeg", b"\xFF\xD8\xFF\xE0\x00\x10JFIF"),
        ("document_scan.JPG", b"\xFF\xD8\xFF\xE0\x00\x10JFIF"),
        ("app_screenshot.png", b"\x89PNG\r\n\x1a\n"),                # PNG (should NOT be moved)
        ("financial_notes.txt", b"Notes: Meeting on Monday morning."), # TXT (should NOT be moved)
        ("report.pdf", b"%PDF-1.4 sample pdf content")                # PDF (should NOT be moved)
    ]

    for filename, content in test_files:
        filepath = os.path.join(source_folder, filename)
        with open(filepath, "wb") as f:
            f.write(content)
        print(f"  + Created: {filepath}")

    # 2. Setup Sample Text File for Task 2 (Email Extraction)
    sample_text_path = os.path.join(base_dir, "sample_text.txt")
    sample_text_content = """Project Team Contact Directory & Inquiries:
--------------------------------------------------
Welcome to the Python Automation Project! For any inquiries, reach out to the project leads:
1. Primary Developer: alex.chen@example.com (Office Hours: 9 AM - 5 PM)
2. Support Team Lead: SUPPORT-TEAM@service-hub.org
3. Project Manager: sarah_connor99@tech-solutions.co.uk.
4. Duplicate check: alex.chen@example.com should be deduplicated properly!

General company contacts:
- General queries: info@samplecompany.net,
- Human Resources: hr.recruitment@careers-portal.com!
- Billing and Accounts: billing_dept@finance.io;
- Feedback box: feedback@service-hub.org (Mon-Fri)

Invalid email strings that regex should ignore:
- plain text words: contact@ and @missingusername.com
- invalid symbols: user@@doubleat.com or user@.missingdomain.org

Thank you for testing the regex email extractor script!
"""

    with open(sample_text_path, "w", encoding="utf-8") as f:
        f.write(sample_text_content)
    print(f"  + Created: {sample_text_path}")

    # 3. Setup Sample HTML Webpage for Task 3 (Web Scraping - Offline Capability)
    sample_html_path = os.path.join(base_dir, "sample_webpage.html")
    sample_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="description" content="A demonstration webpage for Python task automation and title scraping.">
    <title>Python Task Automation - Official Project Hub</title>
</head>
<body>
    <h1>Task 3: Automated Web Scraper</h1>
    <p>This page verifies regex-based title and metadata extraction.</p>
</body>
</html>
"""
    with open(sample_html_path, "w", encoding="utf-8") as f:
        f.write(sample_html_content)
    print(f"  + Created: {sample_html_path}")

    print("[SUCCESS] Sample data generation complete!\n")


if __name__ == "__main__":
    setup_sample_data()
