usage: punc_conv.py [-h] DIRECTORY

Convert half-width punctuation to full-width punctuation in an HTML file. When English
characters are preceded and followed by Chinese characters, add an appropriate amount of
margin before and after them.

This script reads HTML files, parses its content, and replaces all half-width
punctuation characters with their equivalent full-width punctuation characters in the
text content of HTML elements. The modified HTML content is then written back to the
original file.

positional arguments:
  DIRECTORY   path to a single HTML/XHTML file or a directory containing HTML/XHTML files

options:
  -h, --help  show this help message and exit
