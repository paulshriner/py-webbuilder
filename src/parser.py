import os
from typing import TextIO

# Entry function to parse a Markdown file
# Takes the root path and the path to a Markdown file
# Will create tmp file with parsed content
def parse_content_file(root_path: str, file: str) -> None:
    # Change directory to root
    os.chdir(root_path)

    # Get name to use for temp file
    # Use rfind to get last slash in directory
    # If it's -1 then whole name would be used
    slash_index = file.rfind('/')
    file_name = file[slash_index+1:][0:-3]

    try:
        # Create temp dir if needed, if already exists just continue
        os.mkdir('temp')
    except FileExistsError:
        pass

    input_file = open(f"{file}", 'r')
    temp_file = open(f"temp/{file_name}.tmp", 'w')
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
