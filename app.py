"""
Web Dashboard Server for Python Task Automation Suite.
Hosts an interactive web GUI on localhost (http://127.0.0.1:5000).
"""

import os
from flask import Flask, render_template, request, jsonify

# Import the core automation task functions
from task1_move_jpg import move_jpg_files
from task2_extract_emails import extract_emails
from task3_scrape_title import scrape_webpage_title, DEFAULT_URL
from setup_sample_data import setup_sample_data

app = Flask(__name__, template_folder="templates")

# Ensure sample files exist on startup
if not os.path.exists("sample_data/source_folder"):
    setup_sample_data("sample_data")


@app.route("/")
def index():
    """Renders the main task automation web dashboard."""
    return render_template("index.html")


@app.route("/api/sample-text", methods=["GET"])
def get_sample_text():
    """Returns sample text content for Task 2 demonstration."""
    sample_path = "sample_data/sample_text.txt"
    if not os.path.exists(sample_path):
        setup_sample_data("sample_data")

    try:
        with open(sample_path, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({"success": True, "content": content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/task1", methods=["POST"])
def api_task1():
    """Endpoint for Task 1: Moving JPG files."""
    data = request.get_json() or {}
    source = data.get("source", "sample_data/source_folder").strip()
    dest = data.get("dest", "sample_data/organized_jpgs").strip()
    copy_only = bool(data.get("copy_only", False))

    if not os.path.exists(source) or len(os.listdir(source)) == 0:
        setup_sample_data("sample_data")

    result = move_jpg_files(source, dest, copy_only=copy_only)
    return jsonify(result)


@app.route("/api/task2", methods=["POST"])
def api_task2():
    """Endpoint for Task 2: Email Extraction."""
    data = request.get_json() or {}
    custom_content = data.get("content")

    input_file = "sample_data/sample_text.txt"
    output_file = "sample_data/extracted_emails.txt"

    # If user provided custom text directly in the web UI, write to a temporary input file
    if custom_content and custom_content.strip():
        input_file = "sample_data/user_input.txt"
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(custom_content)

    result = extract_emails(input_file, output_file)
    return jsonify(result)


@app.route("/api/task3", methods=["POST"])
def api_task3():
    """Endpoint for Task 3: Web Scraping."""
    data = request.get_json() or {}
    target = data.get("url", DEFAULT_URL).strip()
    output_file = "sample_data/scraped_title.txt"

    result = scrape_webpage_title(target, output_file)

    # Fallback to local HTML if network is blocked
    if not result.get("success") and os.path.exists("sample_data/sample_webpage.html"):
        print("[INFO] Network is unavailable. Using local sample HTML as fallback...")
        result = scrape_webpage_title("sample_data/sample_webpage.html", output_file)

    return jsonify(result)


@app.route("/api/reset-data", methods=["POST"])
def api_reset():
    """Resets the sample test folder and files."""
    setup_sample_data("sample_data")
    return jsonify({"success": True, "message": "Sample data reset successfully"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("\n==================================================")
    print(">> TASK AUTOMATION WEB DASHBOARD RUNNING")
    print(f"[*] Localhost URL: http://127.0.0.1:{port}")
    print(f"[*] Alternative  : http://localhost:{port}")
    print("==================================================\n")
    app.run(host="127.0.0.1", port=port, debug=False)
