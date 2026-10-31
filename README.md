# Task Automation with Python Scripts

> **Task 3:** Automate a small, real-life repetitive task using standard Python libraries and best practices.

---

## 📌 Project Overview

This repository provides an automated solution that addresses all three prompt recommendations:
1. **Move all `.jpg` files from a folder to a new folder** (using `os`, `shutil`, collision handling).
2. **Extract all email addresses from a `.txt` file and save them to another file** (using `re`, `file handling`, normalization).
3. **Scrape the title of a fixed webpage and save it** (using `requests`, `re`, `file handling`, with offline fallback).

You can run each task as an **independent standalone script** or run them collectively through the unified **Interactive Master Automation Suite** (`task_automation.py`).

---

## 🛠️ Key Concepts Used

| Module / Concept | Practical Application in Project |
| :--- | :--- |
| **`os`** | Directory existence checks (`os.path.exists`), scanning directories (`os.listdir`), folder creation (`os.makedirs`), path manipulation (`os.path.join`, `os.path.splitext`). |
| **`shutil`** | High-level file management, moving files safely (`shutil.move`), and optional copying (`shutil.copy2`). |
| **`re`** | Regular expressions for RFC-compliant email extraction (`[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+`) and HTML tag parsing (`<title>...</title>`). |
| **`requests`** | HTTP GET requests with custom User-Agent headers, timeout handling, status code validation, and network error handling. |
| **`file handling`** | Safe read/write operations using Python context managers (`with open(..., 'r'/'w', encoding='utf-8')`), generating formatted reports. |
| **`argparse`** | Robust Command-Line Interface (CLI) supporting custom flags, help menus, and automation pipelines. |

---

## 📁 Repository Structure

```text
python project 3/
├── task1_move_jpg.py         # Task 1: Move .jpg files from source to destination
├── task2_extract_emails.py     # Task 2: Extract & deduplicate email addresses from text
├── task3_scrape_title.py       # Task 3: Webpage title and metadata scraper
├── task_automation.py          # Unified Master Suite with interactive CLI & demo modes
├── setup_sample_data.py        # Helper to generate test files (.jpg, .png, .txt, .html)
├── test_automation.py          # Automated unit test suite (unittest)
├── requirements.txt            # Dependency specification (requests)
└── sample_data/                # Working directory containing sample files and outputs
    ├── source_folder/          # Mixed dummy files (.jpg, .jpeg, .png, .txt, .pdf)
    ├── organized_jpgs/         # Destination folder for organized JPG images
    ├── sample_text.txt         # Input text containing email addresses
    ├── extracted_emails.txt    # Generated output report of extracted emails
    ├── sample_webpage.html     # Local HTML file for offline scraper testing
    └── scraped_title.txt       # Generated output report of scraped title & metadata
```

---

## 🚀 Quick Start Guide

### 1. Requirements & Setup
No external installation is required for Tasks 1 and 2 (built-in standard library). For Task 3 (`requests`):

```bash
pip install -r requirements.txt
```

### 2. Run the Interactive Master Suite
Launch the main menu to choose any task or test all features interactively:
```bash
python task_automation.py
```

### 3. Run the One-Command Demo
Executes all 3 tasks in sequence with sample test data and prints a summary:
```bash
python task_automation.py --demo
```

---

## 📖 Individual Task Instructions

### Option 1: Move all `.jpg` files (`task1_move_jpg.py`)
Automatically scans a source folder, filters for `.jpg` and `.jpeg` files (case-insensitive), and moves them into a destination directory.

- **Collision Prevention**: If a file named `photo.jpg` already exists in the destination, it is saved as `photo_1.jpg`, avoiding data loss.
- **Run command**:
  ```bash
  python task1_move_jpg.py
  ```
- **Custom folders**:
  ```bash
  python task1_move_jpg.py --source "path/to/my_photos" --dest "path/to/organized_photos"
  ```
- **Copy mode (instead of moving)**:
  ```bash
  python task1_move_jpg.py --copy
  ```

---

### Option 2: Extract Email Addresses (`task2_extract_emails.py`)
Scans any text document, extracts valid email addresses using regex, strips trailing punctuation, normalizes cases, removes duplicates, and generates an output report.

- **Run command**:
  ```bash
  python task2_extract_emails.py
  ```
- **Custom input/output paths**:
  ```bash
  python task2_extract_emails.py --input "my_notes.txt" --output "cleaned_emails.txt"
  ```
- **Sample Output (`sample_data/extracted_emails.txt`)**:
  ```text
  ============================================================
   EXTRACTED EMAIL ADDRESSES REPORT
  ============================================================
  Source File   : sample_text.txt
  Extracted On  : 2026-10-31 15:39:53
  Total Matches : 8
  Unique Emails : 7
  ------------------------------------------------------------

    1. alex.chen@example.com
    2. billing_dept@finance.io
    3. feedback@service-hub.org
    4. hr.recruitment@careers-portal.com
    5. info@samplecompany.net
    6. sarah_connor99@tech-solutions.co.uk
    7. support-team@service-hub.org

  ============================================================
  ```

---

### Option 3: Scrape Webpage Title (`task3_scrape_title.py`)
Fetches the HTML of a target webpage or local HTML file, parses `<title>` and `<meta name="description">` tags using regular expressions, decodes HTML entities (e.g., `&amp;`), and saves a structured summary report.

- **Run command (Default URL: Wikipedia Python article)**:
  ```bash
  python task3_scrape_title.py
  ```
- **Scrape any custom URL**:
  ```bash
  python task3_scrape_title.py --url "https://httpbin.org" --output "my_title.txt"
  ```
- **Scrape a local HTML file (offline-safe)**:
  ```bash
  python task3_scrape_title.py --url "sample_data/sample_webpage.html"
  ```
- **Sample Output (`sample_data/scraped_title.txt`)**:
  ```text
  ============================================================
   WEBPAGE TITLE SCRAPING REPORT
  ============================================================
  Scraped On       : 2026-10-31 15:40:11
  Target           : sample_data/sample_webpage.html
  Status           : Local File (200 OK)
  Content Size     : 402 bytes
  Execution Time   : 0.021 seconds
  ------------------------------------------------------------
  SCRAPED TITLE    : Python Task Automation - Official Project Hub
  META DESCRIPTION : A demonstration webpage for Python task automation and title scraping.
  ============================================================
  ```

---

## 🧪 Automated Testing

A test suite is included using Python's built-in `unittest` framework:
```bash
python test_automation.py
```

### Verified Test Cases:
1. `test_task1_move_jpg_files`: Asserts only `.jpg`/`.jpeg` files are moved while `.png`, `.txt`, `.pdf` are left intact.
2. `test_task1_duplicate_filename_handling`: Verifies filename collision handling (e.g. `image_1.jpg`).
3. `test_task2_email_extractor`: Verifies regex extraction, case-insensitivity, deduplication, and trailing punctuation cleanup.
4. `test_task3_scrape_title_html`: Verifies HTML regex parsing, entity decoding, and output reporting.

---

## 🛡️ Error Handling & Reliability

- **File / Directory Validation**: Checks `os.path.exists()` and `os.path.isdir()` before attempting filesystem operations.
- **Collision Protection**: Automatically increments filename suffixes to prevent overwriting existing files.
- **Network Resilience**: Uses browser-like `User-Agent` headers and handles `Timeout`, `ConnectionError`, and HTTP error codes gracefully.
- **Encoding Safety**: Uses explicit `encoding="utf-8"` throughout file I/O operations and ASCII-safe console outputs across Windows PowerShell, Command Prompt, macOS, and Linux.
