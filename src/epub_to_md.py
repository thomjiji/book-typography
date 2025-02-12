import argparse
import glob
import os
import re
import tempfile
import zipfile

from bs4 import BeautifulSoup


def add_spacing(text):
    text = re.sub(
        r"([\u4e00-\u9fff])([A-Za-z0-9✕%éèàçâêîôûëïüÿœæœÆŒÉÈÀÇÂÊÎÔÛËÏÜŸ]+)(?=[ .,—（），。'“”？、/])",
        r"\1 \2",
        text,
    )
    text = re.sub(
        r"([\u4e00-\u9fff])([A-Za-z0-9✕Φ%#-.]+)(?![ ，。）'éèàçâêîôûëïüÿœæœÆŒÉÈÀÇÂÊÎÔÛËÏÜŸ/])",
        r"\1 \2 ",
        text,
    )
    text = re.sub(
        r"(^|[ .,，。：；“”‘’——（）［］、？·《》・/])([A-Za-z0-9éèàçâêîôûëïüÿœæœÆŒÉÈÀÇÂÊÎÔÛËÏÜŸ✕]+)(?=[\u4e00-\u9fff])",
        r"\1 \2",
        text,
    )
    return text


def extract_text_from_html(html_path, add_spaces, title_class):
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        markdown_lines = []
        for tag in soup.find_all():
            text = tag.get_text(strip=True)
            if add_spaces:
                text = add_spacing(text)

            if tag.name.startswith("h") and tag.name[1:].isdigit():
                markdown_lines.append(f"{'#' * int(tag.name[1])} {text}")
            elif title_class and tag.has_attr("class") and title_class in tag["class"]:
                markdown_lines.append(f"## {text}")
                markdown_lines.append("")
            elif tag.name == "blockquote":
                markdown_lines.append(f"> {text}")
                markdown_lines.append("")
            elif tag.name in ["p", "li"]:
                markdown_lines.append(text)
                markdown_lines.append("")  # blank line for paragraph separation
            elif tag.name == "ul":
                for li in tag.find_all("li"):
                    markdown_lines.append(f"- {li.get_text(strip=True)}")
                markdown_lines.append("")
        return "\n".join(markdown_lines).strip()


def find_epub_content_dir(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if any(f.endswith((".html", ".xhtml")) for f in files):
            return root
    return base_dir


def convert_epub_to_markdown(epub_file, output_file, add_spaces, title_class):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(epub_file, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        content_dir = find_epub_content_dir(temp_dir)
        html_files = sorted(
            glob.glob(os.path.join(content_dir, "**", "*.html"), recursive=True)
        )
        xhtml_files = sorted(
            glob.glob(os.path.join(content_dir, "**", "*.xhtml"), recursive=True)
        )
        all_files = html_files + xhtml_files

        if not all_files:
            return

        all_texts = []
        for file in all_files:
            text = extract_text_from_html(file, add_spaces, title_class)
            if text:
                all_texts.append(text)

        markdown_content = "\n\n".join(all_texts)

        with open(output_file, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract text from an EPUB file and convert it to Markdown."
    )
    parser.add_argument("epub_file", help="Path to the EPUB file.")
    parser.add_argument("output_file", help="Path to the output Markdown file.")
    parser.add_argument(
        "--add-spaces",
        action="store_true",
        help="Add spaces between Chinese and non-Chinese characters.",
    )
    parser.add_argument(
        "--title-class",
        help="Specify a class name to detect titles (e.g., 'calibre_6').",
        default=None,
    )
    args = parser.parse_args()
    convert_epub_to_markdown(
        args.epub_file, args.output_file, args.add_spaces, args.title_class
    )
