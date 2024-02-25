"""Convert half-width punctuation to full-width punctuation in an HTML file.

This script reads an HTML file, parses its content, and replaces all half-width
punctuation characters with their equivalent full-width punctuation characters in the
text content of HTML elements, excluding the first line. The modified HTML content is
then written back to the original file.

Example:
    $ python punc_conv.py example.html

Args:
    FILE (str): The path to the HTML file to be processed.
"""

import argparse
import html
import re
from pathlib import Path

from bs4 import BeautifulSoup


def half_to_full_width(text):
    half_width_punctuation = {
        "!": "！",
        # '"': "“",  # Chinese full-width opening quotation mark
        # "'": "”",  # Chinese full-width closing quotation mark
        # "‘": "“",  # Replace other types of single quotes with Chinese full-width opening quotation mark
        # "’": "”",  # Replace other types of single quotes with Chinese full-width closing quotation mark
        # "#": "＃",
        "$": "＄",
        # "%": "％",
        "&": "＆",
        "(": "（",
        ")": "）",
        "*": "＊",
        "+": "＋",
        ",": "，",
        "-": "－",
        # ".": "．",
        # "/": "／",
        ":": "：",
        ";": "；",
        "<": "＜",
        "=": "＝",
        ">": "＞",
        "?": "？",
        "@": "＠",
        "[": "［",
        "\\": "＼",
        "]": "］",
        "^": "＾",
        "_": "＿",
        "`": "｀",
        "{": "｛",
        "|": "｜",
        "}": "｝",
        "~": "～",
    }
    for half, full in half_width_punctuation.items():
        if half == ",":
            # Check if comma is inside an English sentence
            if re.search(r"[A-Za-z]+, [A-Za-z]+", text):
                continue  # Skip replacement
        if half == ":":
            if re.search(r"[A-Za-z]+:[A-Za-z/]+", text):
                continue
        text = text.replace(half, full)

    text = re.sub(
        r"([\u4e00-\u9fff])([A-Za-z0-9✕%]+)(?=[.,—（），。' ])",
        r"\1<span class='margin_add_left'>\2</span>",
        text,
    )

    text = re.sub(
        r"([\u4e00-\u9fff])([A-Za-z0-9✕Φ%#]+)(?![，。）' ])",
        r"\1<span class='margin_add_both'>\2</span>",
        text,
    )

    text = re.sub(
        r"(^|[ .,，。：；“”‘’——（）［］、？·])([A-Za-z0-9éèàçâêîôûëïüÿœæœÆŒÉÈÀÇÂÊÎÔÛËÏÜŸ.✕]+)(?=[\u4e00-\u9fff])",
        r"\1<span class='margin_add_right'>\2</span>",
        text,
    )

    text = html.unescape(text)

    return text


def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    lines = html_content.split("\n")
    if lines[0].startswith("<!DOCTYPE"):
        # If the first line contains <!DOCTYPE>, skip processing the first line
        first_line_skipped = "\n".join(lines[1:])
    else:
        first_line_skipped = html_content

    soup = BeautifulSoup(first_line_skipped, "html.parser")

    for element in soup.find_all(string=True):
        if element.parent.name not in ["script", "style"]:
            if element.parent.name in ["sup", "a"]:
                continue  # Skip processing if within <sup> and <a> tag
            element.replace_with(half_to_full_width(element))

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html.unescape(str(soup)))


def process_html_files(directory_or_file):
    path = Path(directory_or_file)
    if path.is_dir():
        for file_path in path.glob("**/*.html"):
            process_html_file(str(file_path))
        for file_path in path.glob("**/*.xhtml"):
            process_html_file(str(file_path))
    elif path.is_file():
        if path.suffix.lower() in [".html", ".xhtml"]:
            process_html_file(str(path))
        else:
            print("Invalid file extension. Only .html and .xhtml files are supported.")
    else:
        print("Invalid path provided.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        metavar="DIRECTORY",
        type=str,
        help="path to the directory containing HTML files",
    )
    args = parser.parse_args()

    process_html_files(args.directory)
