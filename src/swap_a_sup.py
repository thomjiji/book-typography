"""
This script moves <a> tags within <sup> tags in HTML/XHTML files to make the footnote
number looks good.
"""

import argparse
from pathlib import Path

from bs4 import BeautifulSoup


def move_a_tag_within_sup_tag(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <a> tags containing <sup> tags
    for a_tag in soup.find_all("a"):
        sup_tag = a_tag.find("sup")
        if sup_tag:
            # Move the content of sup tag inside a tag and wrap it
            a_tag.string = sup_tag.text

            # Clear the content of the outer sup tag
            sup_tag.clear()

            # Now wrap the a_tag with the sup_tag
            a_tag.wrap(sup_tag)

    # Write the modified HTML content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))


def process_html_files(directory_or_file):
    path = Path(directory_or_file).resolve()
    if path.is_file() and path.suffix.lower() in (".html", ".xhtml"):
        move_a_tag_within_sup_tag(path)
    elif path.is_dir():
        for file_path in path.glob("**/*.html"):
            move_a_tag_within_sup_tag(file_path)
        for file_path in path.glob("**/*.xhtml"):
            move_a_tag_within_sup_tag(file_path)
    else:
        print("Invalid path provided.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move <a> tag within <sup> tag in HTML/XHTML files"
    )
    parser.add_argument(
        "path", metavar="PATH", type=str, help="path to HTML/XHTML file or directory"
    )
    args = parser.parse_args()

    process_html_files(args.path)
