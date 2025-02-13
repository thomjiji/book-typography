import re
import argparse


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
        "\\": "＼",
        "^": "＾",
        "`": "｀",
        "{": "｛",
        "|": "｜",
        "}": "｝",
        "~": "～",
        "·": "・",
    }

    def replacement(match):
        char = match.group(1)
        if char == "," and re.search(r"[A-Za-z]+, [A-Za-z]+", text):
            return char  # Skip English sentence commas
        if char == ":" and re.search(r"[A-Za-z]+:[A-Za-z/]+", text):
            return char  # Skip colons in URLs
        return half_width_punctuation.get(char, char)

    # Split text into lines to preserve line breaks
    lines = text.splitlines()

    for i, line in enumerate(lines):
        # Skip lines starting with Markdown-specific characters (headers, lists, etc.)
        if re.match(
            r"^\s*([#*-])", line
        ):  # Matches lines starting with Markdown list or header
            continue

        # Replace punctuation and remove unnecessary spaces around them, but keep spaces where necessary
        lines[i] = re.sub(
            r"(?<=\S)\s*([!$&()*+,:;<=>?\^`{|}~·])\s*(?=\S)",
            lambda m: replacement(m),
            line,
        )

    # Join the lines back into text with preserved line breaks
    return "\n".join(lines)


def convert_md_punctuation(md_file):
    with open(md_file, "r", encoding="utf-8") as file:
        content = file.read()

    converted_content = half_to_full_width(content)

    with open(md_file, "w", encoding="utf-8") as file:
        file.write(converted_content)

    print(f"Converted punctuation in: {md_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert halfwidth punctuation to fullwidth in a Markdown file."
    )
    parser.add_argument("md_file", help="Path to the Markdown file.")
    args = parser.parse_args()
    convert_md_punctuation(args.md_file)
