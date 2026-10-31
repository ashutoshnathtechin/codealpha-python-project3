"""
Automated Unit and Integration Tests for Python Task Automation Suite.
Verifies all 3 core tasks:
  1. JPG File Mover (os, shutil)
  2. Email Extractor (re, file handling)
  3. Web Page Title Scraper (requests, re)
"""

import os
import shutil
import tempfile
import unittest
from task1_move_jpg import move_jpg_files
from task2_extract_emails import extract_emails
from task3_scrape_title import scrape_webpage_title


class TestTaskAutomation(unittest.TestCase):

    def setUp(self):
        """Create a clean isolated temporary directory for test executions."""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "dest")
        os.makedirs(self.source_dir, exist_ok=True)

    def tearDown(self):
        """Clean up temporary directory after each test."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_task1_move_jpg_files(self):
        """Test that ONLY .jpg/.jpeg files are moved and others are left untouched."""
        # Create test files
        jpg1 = os.path.join(self.source_dir, "photo1.jpg")
        jpg2 = os.path.join(self.source_dir, "photo2.JPEG")
        png1 = os.path.join(self.source_dir, "diagram.png")
        txt1 = os.path.join(self.source_dir, "notes.txt")

        for f in [jpg1, jpg2, png1, txt1]:
            with open(f, "wb") as fh:
                fh.write(b"dummy content")

        result = move_jpg_files(self.source_dir, self.dest_dir)

        self.assertTrue(result["success"])
        self.assertEqual(result["moved_count"], 2)
        self.assertEqual(result["skipped_count"], 2)

        # JPGs should now be in destination
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "photo1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "photo2.JPEG")))

        # Non-JPGs should still be in source
        self.assertTrue(os.path.exists(png1))
        self.assertTrue(os.path.exists(txt1))

    def test_task1_duplicate_filename_handling(self):
        """Test that existing destination files are not overwritten."""
        os.makedirs(self.dest_dir, exist_ok=True)
        # Pre-create duplicate in dest
        with open(os.path.join(self.dest_dir, "image.jpg"), "w") as f:
            f.write("original file")

        # Create same-named file in source
        with open(os.path.join(self.source_dir, "image.jpg"), "w") as f:
            f.write("new file to move")

        result = move_jpg_files(self.source_dir, self.dest_dir)
        self.assertTrue(result["success"])
        self.assertEqual(result["moved_count"], 1)

        # Dest should have both: 'image.jpg' and 'image_1.jpg'
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "image_1.jpg")))

    def test_task2_email_extractor(self):
        """Test regex extraction, cleaning, deduplication, and file saving."""
        test_txt = os.path.join(self.test_dir, "input.txt")
        out_txt = os.path.join(self.test_dir, "output.txt")

        sample_content = (
            "Contact john.doe@example.com, or support@domain.org! "
            "Duplicate: JOHN.DOE@EXAMPLE.COM. "
            "Another one: alice+work@company.co.in; "
            "Invalid: plain-text and user@invalid."
        )
        with open(test_txt, "w", encoding="utf-8") as f:
            f.write(sample_content)

        result = extract_emails(test_txt, out_txt)

        self.assertTrue(result["success"])
        # Should find john.doe@example.com, support@domain.org, alice+work@company.co.in
        self.assertIn("john.doe@example.com", result["emails"])
        self.assertIn("support@domain.org", result["emails"])
        self.assertIn("alice+work@company.co.in", result["emails"])
        self.assertEqual(result["unique_count"], 3)
        self.assertTrue(os.path.exists(out_txt))

    def test_task3_scrape_title_html(self):
        """Test webpage title scraping from HTML."""
        sample_html = os.path.join(self.test_dir, "test.html")
        out_txt = os.path.join(self.test_dir, "title.txt")

        with open(sample_html, "w", encoding="utf-8") as f:
            f.write("<html><head><title>My Automated Test Page &amp; Guide</title></head><body>Hello</body></html>")

        result = scrape_webpage_title(sample_html, out_txt)
        self.assertTrue(result["success"])
        self.assertEqual(result["title"], "My Automated Test Page & Guide")
        self.assertTrue(os.path.exists(out_txt))


if __name__ == "__main__":
    unittest.main()
