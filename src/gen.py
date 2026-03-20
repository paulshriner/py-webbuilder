'''
    py-webbuilder
    Author: Paul Shriner

    gen: Converts intermediate code into final code
'''

from file import get_file_name, peek
from typing import TextIO

# Generates HTML code from a parsed intermediate file
def generate_html(temp_file_path: str) -> None:
    # Get name to use for temp file
    temp_file_name = get_file_name(temp_file_path)[0]

    temp_ptr = open(temp_file_path, 'r')
    final_ptr = open(f"../temp/{temp_file_name}.final", 'w')

    next_line = peek(temp_ptr, 1)
    html_line = []
    index = 0
    in_code_block = False
    # TODO: Refactor this some more
    while next_line:
        line_stripped = next_line[0:-1]

        if next_line.startswith("<UNORDERED_LIST") or next_line.startswith("<ORDERED_LIST"):
            html_line.append(generate_list(temp_ptr, line_stripped))
            index += 1
        else:
            match line_stripped:
                case "<CODE_BLOCK>":
                    # If code block found, add code tag to final file then continue with other tokens
                    # When second code block token is found that signals the end of the block
                    if not in_code_block:
                        final_ptr.write("<code>\n")
                        in_code_block = True
                    else:
                        final_ptr.write("</code>\n")
                        in_code_block = False
                    temp_ptr.readline()
                case "<HORIZONTAL_RULE>":
                    html_line.append("<hr>\n")
                    index += 1
                case "<NEW_LINE>":
                    # If new line is found outside of another condition (like list)
                    # Then we're done, print the line and clear it
                    final_ptr.write("".join(html_line) + "\n")
                    html_line = []
                    index = 0
                case "<EMPTY_LINE>":
                    # An empty line is treated as a new line, this is intentional
                    html_line.append("<br>\n")
                    index += 1
                case default:
                    html_line.append(generate_line(temp_ptr))
                    index += 1

        # Read last line, peek at next line
        temp_ptr.readline()
        next_line = peek(temp_ptr, 1)

    # Make sure code tag is closed if input file did not have closing code token
    if in_code_block:
        final_ptr.write("</code>\n")

    # Close files when done
    temp_ptr.close()
    final_ptr.close()

# Generates HTML for a one line element like headings or text
# File pointer will be one previous from content line
def generate_line(f: TextIO) -> str:
    # Get token, related tag, then read it in file
    token = peek(f, 1).strip()
    tag = get_html_tag(token)
    f.readline()

    # Get line, then read it in file
    line = peek(f, 1).strip()

    return f'<{tag}>{line}</{tag}>'

# Generates the HTML for a list
# Takes file pointer, start token, seen tokens
# Returns string with HTML list
def generate_list(f: TextIO, start: str, seen: list[str] = []) -> str:
    start_parts = get_start_ol_num(start)
    seen.append(start_parts[0])

    # Beginning tag of list
    items = []
    tag = get_html_tag(start)
    if start.startswith("<ORDERED"):
        items.append(f'<{tag} start="{start_parts[1]}">')
    else:
        items.append(f"<{tag}>")

    continue_list = False
    while peek(f, 1).startswith("<UNORDERED") or peek(f, 1).startswith("<ORDERED") or continue_list:
        if not continue_list:
            # Read the start line
            f.readline()

            # Peek at content line, add it as list item
            # TODO: This only considers one block element, may need to be changed
            line = peek(f, 1)[0:-1]
            tag = get_html_tag(line)
            items.append("<li>")
            if line != tag:
                items.append(f"<{tag}>")
                f.readline()
                line = peek(f, 1)[0:-1]
                items.append(line)
                items.append(f"</{tag}>")
            else:
                items.append(line)
            items.append("</li>")
        continue_list = False

        # Check if we are still in a list
        test_token = peek(f, 3)[0:-1]
        if test_token.startswith("<UNORDERED") or test_token.startswith("<ORDERED"):
            # Read up to start line
            f.readline()
            f.readline()

            line_parts = get_start_ol_num(test_token)
            if line_parts[0] != start_parts[0]:
                # If we've already seen this element then we need to go back
                # Else recurse to inner list
                if line_parts[0] in seen:
                    break
                else:
                    items.append(generate_list(f, test_token, seen))
        elif test_token != "<EMPTY_LINE>":
            # Get content for token
            test_line = peek(f, 4)[0:-1]
            # Use 4 spaces to determine if this line goes in list
            if test_line.startswith("    "):
                continue_list = True

                # Read up to token then generate line for it
                f.readline()
                f.readline()
                items.append(generate_line(f))

    # Ending tag of list
    tag = get_html_tag(start)
    items.append(f"</{tag}>")

    return "".join(items)

# Helper function to get starting num of ordered list
# Can be used for other tokens, it will just return that token
def get_start_ol_num(line: str) -> list[str]:
    # Get rid of new line if present
    if line.endswith('\n'):
        line = line[0:-1]
    
    # Make sure tag is ordered list
    if not line.startswith("<ORDERED_LIST"):
        return [line]
    
    line_parts = line.split('_')
    # Should be 4 parts (ORDERED, LIST, num, indent)
    if len(line_parts) != 4:
        return [line]

    return [f'{line_parts[0]}_{line_parts[1]}_{line_parts[2]}>', line_parts[3][0:-1]]

# Helper function to get matching HTML tag for intermediate tag
def get_html_tag(line: str) -> str:
    match line:
        case "<HEADING_1>":
            return "h1"
        case "<HEADING_2>":
            return "h2"
        case "<HEADING_3>":
            return "h3"
        case "<HEADING_4>":
            return "h4"
        case "<HEADING_5>":
            return "h5"
        case "<HEADING_6>":
            return "h6"
        case "<TEXT>":
            return "p"
    
    # Any nested list would still use <ul> or <ol>
    if line.startswith("<UNORDERED_LIST"):
        return "ul"
    if line.startswith("<ORDERED_LIST"):
        return "ol"
    
    return line
