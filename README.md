usage: punc_conv.py [-h] DIRECTORY

Convert half-width punctuation to full-width punctuation in an HTML file. Add margin
around English characters and numbers when they are preceded and followed by Chinese
characters.

This script reads HTML files, parses its content, and replaces all half-width
punctuation characters with their equivalent full-width punctuation characters in the
text content of HTML elements. It finds all English characters and numbers that preceded
and followed by Chinese characters, adds a html tag to it, then uses css to add margin
around them.

The modified HTML content is then written back to the original file.

positional arguments:
  DIRECTORY   path to a single HTML/XHTML file or a directory containing HTML/XHTML files

options:
  -h, --help  show this help message and exit
