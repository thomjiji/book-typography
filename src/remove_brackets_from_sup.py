import argparse
from bs4 import BeautifulSoup
from pathlib import Path


def remove_parentheses_from_span_tags(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <span> tags with class "calibre5"
    span_tags = soup.find_all("sup", class_="calibre5")

    # Loop through each <span> tag
    for span_tag in span_tags:
        # Remove parentheses from the text inside the <span> tag
        cleaned_text = "".join(char for char in span_tag.get_text() if char.isdigit())
        span_tag.string = cleaned_text

    # Write the modified HTML content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(soup))


def process_html_files_in_directory(directory):
    for file_path in directory.glob("**/*.html"):
        remove_parentheses_from_span_tags(file_path)


def main():
    parser = argparse.ArgumentParser(
        description="Remove parentheses from <sup> tags in HTML files within a directory"
    )
    parser.add_argument(
        "directory", type=Path, help="Path to the directory containing HTML files"
    )
    args = parser.parse_args()

    directory = args.directory
    process_html_files_in_directory(directory)


if __name__ == "__main__":
    main()
