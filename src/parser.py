'''
    py-webbuilder
    Author: Paul Shriner

    parser: Converts Markdown into intermediate code
'''

import re
from file import get_file_name, create_dir

# Entry function to parse a Markdown file
# Takes the path to a Markdown file
# Will create tmp file with parsed content
def parse_content_file(file_path: str) -> dict:
    config = {}
    
    # Get name to use for temp file
    file_name = get_file_name(file_path)[0]

    # Create temp dir if needed
    create_dir("temp")

    input_file = open(f"{file_path}", 'r')
    temp_file = open(f"../temp/{file_name}.tmp", 'w')
    in_file = False
    in_config = False
    for line in input_file:
        if not in_file:
            in_file = True
            cur_line = parse_config_block(line)
            if cur_line[1] == "<CONFIG_BEGIN>":
                in_config = True
                continue
        
        if in_config:
            cur_line = parse_config_block(line)
            if cur_line[1] == "<CONFIG_END>":
                in_config = False
            else:
                config[cur_line[1]] = parse_config_line(sanitize_line(cur_line[2][0:-1]))
            continue

        cur_line = parse_markdown_block(line)
        temp_file.write(cur_line[1] + '\n')
        temp_file.write(sanitize_line(cur_line[2]))
        temp_file.write("<NEW_LINE>\n")

    # Close files when done
    input_file.close()
    temp_file.close()

    return config

# Parses the block elements for configuration items
def parse_config_block(line: str) -> tuple[bool, str, str]:
    # Parse start and end of config
    if line.rstrip() == '{':
        return (True, "<CONFIG_BEGIN>", "")
    if line.rstrip() == '}':
        return (True, "<CONFIG_END>", "")
    
    parts = line.split(": ")
    # Config entries should only have two parts
    if len(parts) != 2:
        return (True, "<ERROR>", "")
    
    # Home entry (appears in tho left corner of page)
    if parts[0] == "Home":
        return (True, "<CONFIG_HOME>", parts[1])
    if parts[0] == "Links":
        return (False, "<CONFIG_LINKS>", parts[1])
    if parts[0] == "Footer":
        return (False, "<CONFIG_FOOTER>", parts[1])
    
    # TODO: Rest of config entries
    return (False, "<TEXT>", line)

# Parses elements within config line
# Currently it parses links using regex
# TODO: Parse other elements
# TODO: Different lines need to be handled differently (title line should not have markdown links)
# TODO: This may get combined with an overall "parse_line" function
def parse_config_line(line: str) -> str:
    # Thanks https://regex101.com/r/6irz8e/2 for Markdown link regex
    pattern = r'\[([^\]]+)\]\(([^)]+())\)'
    
    # Thanks https://www.geeksforgeeks.org/python/re-matchobject-group-function-in-python-regex/ for match group
    def convert_link(match):
        preview = match.group(2)
        link = match.group(1)

        return f'<a href="{preview}" target="_blank">{link}</a>'

    # Thanks https://www.geeksforgeeks.org/python/re-sub-python-regex/ for re.sub
    parsed_line = re.sub(pattern, convert_link, line)

    return parsed_line


# Will parse the block element for a line, this could be heading, blockquote, list, etc.
# https://www.markdownguide.org/basic-syntax/ - Markdown syntax reference
# Takes a Markdown line to process
# Outputs a tuple in the format (bool, str, str) where bool represents if there could be more blocks
# first str is token and second str is the line with the token removed
# TODO: Have better documentation, such as by using docstrings
def parse_markdown_block(line: str) -> tuple[bool, str, str]:
    # Nothing in line or user skipped lines
    if not line or line == "\n":
        return (False, "<EMPTY_LINE>", "")
    
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
            return (True, f"<HEADING_{heading_len}>", line[heading_len+1:])
        else:
            break

    # TODO: Implement more Markdown syntax
    return (False, "<TEXT>", line)

# Sanitize a line to prevent HTML being rendered
# Meant to be run before appending to file
# TODO: Convert other character entities to be safe 
def sanitize_line(line: str) -> str:
    return line.replace('<', '&lt;').replace('>', '&gt;')
