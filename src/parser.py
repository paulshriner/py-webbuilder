'''
    py-webbuilder
    Author: Paul Shriner

    parser: Converts Markdown into intermediate code
'''

import re
from pathlib import Path
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
    input_file = open(Path(f"../{file_path}"), 'r')
    temp_file = open(Path("../temp") / f"{file_name}.tmp", 'w')
    # Keep track of if we're in config, as these need to be handled separately
    in_file = False
    in_config = False
    in_code_block = False
    for line in input_file:
        # See if we're in config
        if not in_file:
            in_file = True
            cur_line = parse_config_block(line)
            if cur_line[1] == "<CONFIG_BEGIN>":
                in_config = True
                continue
        
        # If in config, keep going until end bracket found
        # (If <CONFIG_END> is not found it will keep going in config, but this is an invalid input)
        if in_config:
            cur_line = parse_config_block(line)
            if cur_line[1] == "<CONFIG_END>":
                in_config = False
            else:
                if not cur_line[0]:
                    config[cur_line[1]] = parse_line(cur_line[1], sanitize_line(cur_line[2][0:-1]))
                else:
                    config[cur_line[1]] = sanitize_line(cur_line[2][0:-1])
            continue

        # Either we're done with config or user never added one, so proceed with standard markdown
        cur_line = parse_markdown_block(line)
        # If in a code block, add code block tag then set in code block flag
        if cur_line[1] == "<CODE_BLOCK>":
            in_code_block = not in_code_block
            temp_file.write(cur_line[1] + '\n')
            temp_file.write("<NEW_LINE>\n")
            continue

        # While in a code block, do not parse any text, just sanitize as is
        if in_code_block:
            if cur_line[1] == "<EMPTY_LINE>":
                temp_file.write(cur_line[1] + '\n')
            else:
                temp_file.write("<TEXT>\n")
                temp_file.write(sanitize_line(line))
            temp_file.write("<NEW_LINE>\n")
            continue
        
        while not cur_line[0]:
            # Need to reprocess for more block elements, such as a heading in a list
            temp_file.write(cur_line[1] + '\n')
            cur_line = parse_markdown_block(cur_line[2])
        else:
            # Done with block elements, parse inline elements
            temp_file.write(cur_line[1] + '\n')
            temp_file.write(parse_line(cur_line[1], sanitize_line(cur_line[2])))
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
    
    # Home entry (appears in the left corner of page)
    if parts[0] == "Home":
        return (True, "<CONFIG_HOME>", parts[1])
    # Navigation links
    if parts[0] == "Links":
        return (False, "<CONFIG_NAV_LINKS>", parts[1])
    # Footer information
    if parts[0] == "Footer":
        return (False, "<CONFIG_FOOTER>", parts[1])
    # Page title
    if parts[0] == "Title":
        return (False, "<CONFIG_TITLE>", parts[1])
    
    # TODO: Rest of config entries
    return (False, "<ERROR>", line)

# Parses elements within config line
# Currently it parses links using regex
# TODO: Parse other elements
def parse_line(token: str, line: str) -> str:
    # Thanks https://gist.github.com/elfefe/ef08e583e276e7617cd316ba2382fc40 for Markdown regexes
    link_pattern = r'\[(.*?)\]\((.*?)\s?(?:"(.*?)")?\)'
    # Thanks https://www.freecodecamp.org/news/how-to-write-a-regular-expression-for-a-url/ for URL regex
    url_pattern = r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?'
    # Only use astericks not underlines
    bold_pattern = r'\*\*(.+?)\*\*'
    italic_pattern = r'\*(.+?)\*'
    inline_code_pattern = r'`(.+?)`'
    escape_code_pattern = r'``(.+?)``'

    # Hold inline code sections
    code_lines = []
    # NOTE: If the user entered this exact phrase it could cause issues. We will just assume the user won't do this as it's a very specific phrase.
    code_placeholder = "{{CODE_LINE_NUM}}"
    
    # Thanks https://www.geeksforgeeks.org/python/re-matchobject-group-function-in-python-regex/ for match group
    def convert_link(match):
        link = match.group(2)
        preview = match.group(1)

        # First check if link is an external URL
        if not re.search(url_pattern, link):
            # If not, assume we have a file path
            # This may/may not be valid, but this checks for path traversal
            parent_dir = Path.cwd().parent
            full_path = (parent_dir / link).resolve()
            try:
                full_path.relative_to(parent_dir)
            except ValueError:
                link = ""

        return f'<a href="{link}" target="_blank">{preview}</a>'
    
    def convert_bold(match):
        return f'<strong>{match.group(1)}</strong>'
    def convert_italic(match):
        return f'<em>{match.group(1)}</em>'
    def convert_escape_code(match):
        return match.group(1).replace('`', '&#96;')
    def convert_inline_code(match):
        code_lines.append(match.group(1))
        return code_placeholder.replace("NUM", str(len(code_lines) - 1))
    
    # Navigation links should just be links, that's it
    parsed_line = line
    if token == "<CONFIG_NAV_LINKS>":
        matches = re.findall(link_pattern, line)

        parsed_line = ""
        for i in matches:
            parsed_line += f'<li><a href="{i[1]}" target="_blank">{i[0]}</a></li>'
    # Anything else can be text and links, except the home link which is just text (link is always the home page)
    elif token != "<CONFIG_HOME>" and token != "<CONFIG_TITLE>":
        # Convert code lines
        # Inline code will be stored as placeholders so inner elements do not get parsed
        parsed_line = re.sub(escape_code_pattern, convert_escape_code, parsed_line)
        parsed_line = re.sub(inline_code_pattern, convert_inline_code, parsed_line)
        
        # Thanks https://www.geeksforgeeks.org/python/re-sub-python-regex/ for re.sub
        parsed_line = re.sub(link_pattern, convert_link, parsed_line)

        # Convert bold and italic
        parsed_line = re.sub(bold_pattern, convert_bold, parsed_line)
        parsed_line = re.sub(italic_pattern, convert_italic, parsed_line)

    # Replace code line placeholders with actual text
    for i, val in enumerate(code_lines):
        parsed_line = parsed_line.replace(code_placeholder.replace("NUM", str(i)), f'<code>{val}</code>')

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
        return (True, "<EMPTY_LINE>", "")
    
    # Fenced code block
    if line == "```\n":
        return (True, "<CODE_BLOCK>", "")
    
    # Consume starting spaces
    indents = 0
    start_line = 0
    for i, val in enumerate(line):
        if val == ' ':
            if i % 4 == 0:
                indents += 1
            start_line += 1
        else:
            break

    # Remove beginning spaces from line
    stripped_line = line[start_line:]

    # Check for horizontal rule
    hr_patterns = [r'^-{3,}$', r'^\*{3,}$', r'^_{3,}$']
    for r in hr_patterns:
        if re.search(r, stripped_line[0:-1]):
            return (True, "<HORIZONTAL_RULE>", "")
    
    # Check if line represents a heading
    # If we find one #, keep count until space found
    # If we go past 6 headings, or no space is found, it's not a heading
    heading_len = 0
    for i in stripped_line:
        if i == '#':
            heading_len += 1
            if heading_len > 6:
                break
        elif i == ' ' and heading_len >= 0:
            return (True, f"<HEADING_{heading_len}>", f'{'    ' * indents}{stripped_line[heading_len+1:]}')
        else:
            break

    # Check if line represents an unordered list
    # NOTE: Num of indents really does not matter here, it just signifies we start a new list
    if stripped_line.startswith('- ') or stripped_line.startswith('* ') or stripped_line.startswith('+ '):
        return (False, f"<UNORDERED_LIST_{indents}>", stripped_line[2:])
    
    # Check if line represents an ordered list
    list_num = ""
    for i in range(len(stripped_line) - 1):
        if stripped_line[i].isdigit():
            list_num = stripped_line[0:i+1]
        elif list_num and stripped_line[i] == '.' and stripped_line[i + 1] == ' ':
            return (False, f"<ORDERED_LIST_{indents}_{list_num}>", stripped_line[i + 2:])
        else:
            break

    # TODO: Implement more Markdown syntax
    return (True, "<TEXT>", line)

# Sanitize a line to prevent HTML being rendered
# Meant to be run before appending to file
# Thanks https://www.w3schools.com/html/html_entities.asp for list of character entities
# TODO: Convert other character entities to be safe 
def sanitize_line(line: str) -> str:
    return line.replace('<', '&lt;').replace('>', '&gt;').replace("'", '&apos;').replace('"', '&quot;')
