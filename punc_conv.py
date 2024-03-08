"""Convert half-width punctuation to full-width punctuation in an HTML file. Add margin
around English characters and numbers when they are preceded and followed by Chinese
characters.

This script reads HTML files, parses its content, and replaces all half-width
punctuation characters with their equivalent full-width punctuation characters in the
text content of HTML elements. It finds all English characters and numbers that preceded
and followed by Chinese characters, adds a html tag to it, then uses css to add margin
around them.

The modified HTML content is then written back to the original file.
"""

import argparse
import html
import re
from pathlib import Path

from bs4 import BeautifulSoup


def half_to_full_width(text):
    half_width_punctuation = {
        "!": "！",
        "$": "＄",
        "&": "＆",
        "(": "（",
        ")": "）",
        "*": "＊",
        "+": "＋",
        ",": "，",
        ":": "：",
        ";": "；",
        "<": "＜",
        "=": "＝",
        ">": "＞",
        "?": "？",
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
        # "·": "・"
        # "@": "＠",
        # "-": "－",
        # "#": "＃",
        # "%": "％",
        # "/": "／",
        # ".": "．",
    }
    for half, full in half_width_punctuation.items():
        if half == ",":
            # Check if comma is inside an English sentence
            if re.search(r"[A-Za-z]+, [A-Za-z]+", text):
                continue
        if half == ":":
            # Check if colon is in an URL
            if re.search(r"[A-Za-z]+:[A-Za-z/]+", text):
                continue
        text = text.replace(half, full)

    text = re.sub(
        r"([\u4e00-\u9fff])([A-Za-z0-9✕%éèàçâêîôûëïüÿœæœÆŒÉÈÀÇÂÊÎÔÛËÏÜŸ]+)(?=[ .,—（），。'“”])",
        r"\1<span class='margin_add_left'>\2</span>",
        text,
    )

    text = re.sub(
        r"([\u4e00-\u9fff])([A-Za-z0-9✕Φ%#-.]+)(?![ ，。）'éèàçâêîôûëïüÿœæœÆŒÉÈÀÇÂÊÎÔÛËÏÜŸ])",
        r"\1<span class='margin_add_both'>\2</span>",
        text,
    )

    text = re.sub(
        r"(^|[ .,，。：；“”‘’——（）［］、？·《》・])([A-Za-z0-9éèàçâêîôûëïüÿœæœÆŒÉÈÀÇÂÊÎÔÛËÏÜŸ✕]+)(?=[\u4e00-\u9fff])",
        r"\1<span class='margin_add_right'>\2</span>",
        text,
    )

    text = html.unescape(text)

    return text


def process_html_file(file_path):
    skipped_line = ""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if lines[0].startswith("<?xml") or lines[0].startswith("<!DOCTYPE"):
            # Store the skipped line
            skipped_line = lines[0]
            lines = lines[1:]

    html_content = "".join(lines)

    soup = BeautifulSoup(html_content, "html.parser")

    for element in soup.find_all(string=True):
        if element.parent.name not in ["script", "style"]:
            if element.parent.name in ["sup", "a"]:
                continue  # Skip processing if within <sup> and <a> tag
            element.replace_with(half_to_full_width(element))

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(skipped_line)
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
        help="path to a single HTML/XHTML file or a directory containing HTML/XHTML files",
    )
    args = parser.parse_args()

    process_html_files(args.directory)
