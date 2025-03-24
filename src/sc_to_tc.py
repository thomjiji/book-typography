import os
import argparse
from bs4 import BeautifulSoup
import opencc
from bs4.element import NavigableString


def convert_text(text, conversion_type):
    """Convert text using OpenCC with the specified conversion type."""
    converter = opencc.OpenCC(conversion_type)
    return converter.convert(text)


def process_html_file(file_path, conversion_type):
    skipped_line = ""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if lines[0].startswith("<?xml") or lines[0].startswith("<!DOCTYPE"):
            # Store the skipped line (DOCTYPE or XML declaration)
            skipped_line = lines[0]
            lines = lines[1:]

    html_content = "".join(lines)

    # Process HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Convert text nodes using OpenCC
    for element in soup.find_all(string=True):
        if isinstance(element, NavigableString) and element.strip():
            element.replace_with(convert_text(element, conversion_type))

    # Write the modified HTML content back to the same file
    with open(file_path, "w", encoding="utf-8") as file:
        if skipped_line:
            file.write(f"{skipped_line}")  # Re-add DOCTYPE or XML declaration
        file.write(str(soup))  # Write the modified HTML


def process_epub_directory(input_dir, conversion_type):
    """Process all HTML/XHTML files in the given directory."""
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith((".html", ".xhtml")):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                process_html_file(file_path, conversion_type)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert between Simplified and Traditional Chinese (TW/HK) in EPUB files."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory containing HTML or XHTML files in the EPUB.",
    )
    parser.add_argument(
        "--tw",
        action="store_true",
        help="Use Traditional Chinese (Taiwan) instead of Hong Kong.",
    )

    args = parser.parse_args()

    if args.tw:
        conversion_type = "s2tw.json"  # 簡體到臺灣正體
    else:
        conversion_type = "s2hk.json"  # 簡體到香港繁體

    process_epub_directory(args.input_dir, conversion_type)
