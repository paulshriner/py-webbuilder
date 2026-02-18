'''
    py-webbuilder
    Author: Paul Shriner

    parser: Converts Markdown into intermediate code
'''

import os
from typing import TextIO
from file import get_file_name, create_dir

# Entry function to parse a Markdown file
# Takes the path to a Markdown file
# Will create tmp file with parsed content
def parse_content_file(file_path: str) -> None:
    # Get name to use for temp file
    file_name = get_file_name(file_path)[0]

    # Create temp dir if needed
    create_dir("temp")

    input_file = open(f"{file_path}", 'r')
    temp_file = open(f"../temp/{file_name}.tmp", 'w')
    for line in input_file:
        cur_line = parse_markdown_block(temp_file, line)
        temp_file.write(cur_line[1])
        temp_file.write("<NEW_LINE>\n")

    # Close files when done
    input_file.close()
    temp_file.close()

# Will parse the block element for a line, this could be heading, blockquote, list, etc.
# https://www.markdownguide.org/basic-syntax/ - Markdown syntax reference
# Takes a file pointer for a temp file and a Markdown line to process
# Outputs a tuple in the format (bool, str) where bool represents if there could be more blocks
# and str is the line with the heading removed
# TODO: Have better documentation, such as by using docstrings
# Thanks https://stackoverflow.com/a/58887007 for type hinting for file pointer
def parse_markdown_block(temp_file: TextIO, line: str) -> tuple[bool, str]:
    # Nothing in line or user skipped lines
    if not line or line == "\n":
        temp_file.write(f"<EMPTY_LINE>")
        return (False, line)
    
    # Check if line represents a heading
    # If we find one #, keep count until space found
    # If we go past 6 headings, or no space is found, it's not a heading
    heading_len = 0
    for i in line:
        if i == '#':
            heading_len += 1
            if heading_len > 6:
                break
        elif i == ' ' and heading_len >= 0:
            temp_file.write(f"<HEADING_{heading_len}>\n")
            return (True, line[heading_len+1:])
        else:
            break

    # TODO: Implement more Markdown syntax
    temp_file.write(f"<TEXT>\n")
    return (False, line)
