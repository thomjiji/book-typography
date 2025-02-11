import os
import glob
import markdown
import re
from bs4 import BeautifulSoup
import argparse


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


def extract_text_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        markdown_lines = []
        for tag in soup.find_all():
            if tag.name.startswith("h") and tag.name[1:].isdigit():
                markdown_lines.append(
                    f"{'#' * int(tag.name[1])} {add_spacing(tag.get_text(strip=True))}"
                )
            elif tag.name in ["p", "li"]:
                markdown_lines.append(add_spacing(tag.get_text(strip=True)))
                markdown_lines.append("")  # Add a blank line for paragraph separation
            elif tag.name == "ul":
                for li in tag.find_all("li"):
                    markdown_lines.append(f"- {add_spacing(li.get_text(strip=True))}")
                markdown_lines.append("")

        return "\n".join(markdown_lines).strip()


def convert_epub_to_markdown(epub_dir, output_file):
    html_files = sorted(
        glob.glob(os.path.join(epub_dir, "**", "*.html"), recursive=True)
    )

    all_texts = []
    for html_file in html_files:
        text = extract_text_from_html(html_file)
        if text:
            all_texts.append(text)

    markdown_content = "\n\n".join(all_texts)

    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    print(f"Markdown file saved at: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract text from an unzipped EPUB and convert it to Markdown."
    )
    parser.add_argument("epub_dir", help="Path to the unzipped EPUB directory.")
    parser.add_argument("output_file", help="Path to the output Markdown file.")

    args = parser.parse_args()
    convert_epub_to_markdown(args.epub_dir, args.output_file)
