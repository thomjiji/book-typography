import os
import argparse
from bs4 import BeautifulSoup
import opencc
from bs4.element import NavigableString


def convert_simplified_to_traditional(text):
    # Using opencc for Simplified to Traditional Chinese conversion
    converter = opencc.OpenCC(
        "s2t.json"
    )  # Simplified to Traditional Chinese conversion
    return converter.convert(text)


def convert_traditional_to_simplified(text):
    # Using opencc for Traditional to Simplified Chinese conversion
    converter = opencc.OpenCC(
        "t2s.json"
    )  # Traditional to Simplified Chinese conversion
    return converter.convert(text)


def process_html_file(file_path, convert_function):
    skipped_line = ""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if lines[0].startswith("<?xml") or lines[0].startswith("<!DOCTYPE"):
            # Store the skipped line (DOCTYPE or XML declaration)
            skipped_line = lines[0]
            lines = lines[1:]

    # Join the remaining lines to form the HTML content
    html_content = "".join(lines)

    # Now, process the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Convert text nodes using the provided conversion function
    for element in soup.find_all(string=True):  # Find all text nodes
        if (
            isinstance(element, NavigableString) and element.strip()
        ):  # Ensure it's a text node
            element.replace_with(convert_function(element))

    # Write the modified HTML content back to the same file
    with open(file_path, "w", encoding="utf-8") as file:
        if skipped_line:
            file.write(f"{skipped_line}")  # Re-add DOCTYPE or XML declaration
        file.write(str(soup))  # Write the modified HTML


def process_epub_directory(input_dir, convert_function):
    # Loop through all the files in the directory and process only HTML or XHTML files
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith((".html", ".xhtml")):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                process_html_file(file_path, convert_function)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert between Simplified and Traditional Chinese in EPUB files."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory containing HTML or XHTML files in the EPUB.",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Perform reverse conversion (Traditional to Simplified Chinese).",
    )
    args = parser.parse_args()

    # Choose the appropriate conversion function based on user input
    if args.reverse:
        convert_function = convert_traditional_to_simplified
    else:
        convert_function = convert_simplified_to_traditional

    process_epub_directory(args.input_dir, convert_function)  # Process the directory
