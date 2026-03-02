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
    # TODO: Refactor this some more
    while next_line:
        line_stripped = next_line[0:-1]

        if next_line.startswith("<UNORDERED_LIST") or next_line.startswith("<ORDERED_LIST"):
            html_line.append(generate_list(temp_ptr, line_stripped))
            index += 1
        else:
            match line_stripped:
                case "<NEW_LINE>":
                    # If new line is found outside of another condition (like list)
                    # Then we're done, print the line and clear it
                    final_ptr.write("".join(html_line) + "\n")
                    html_line = []
                    index = 0
                case "<EMPTY_LINE>":
                    # For now, an empty line is treated as a new line
                    # TODO: Other Markdown parsers use 4 spaces at end of line as new line, so this may be changed
                    final_ptr.write("<br>" + "\n")
                case default:
                    # These are tags like headings where there's no other block elements after them
                    tag = get_html_tag(line_stripped)
                    if tag != line_stripped:
                        html_line.insert(index, f"<{tag}>")
                        index += 1
                        html_line.insert(index, f"</{tag}>")      
                    else:
                        html_line.insert(index, line_stripped)
                        index += 1

        # Read last line, peek at next line
        temp_ptr.readline()
        next_line = peek(temp_ptr, 1)

    # Close files when done
    temp_ptr.close()
    final_ptr.close()

# Generates the HTML for a list
# Takes file pointer, start token, seen tokens
# Returns string with HTML list
# TODO: Need to account for potential other block elements within a list
def generate_list(f: TextIO, start: str, seen: list = []) -> str:
    seen.append(start)

    # Beginning tag of list
    items = []
    if start.startswith("<ORDERED"):
        start_parts = get_start_ol_num(start)
        items.append(f'<ol start="{start_parts[1]}">')
    else:
        items.append("<ul>")

    while peek(f, 1).startswith("<UNORDERED") or peek(f, 1).startswith("<ORDERED") :
        # Read the start line
        f.readline()

        # Peek at content line, add it as list item
        line = peek(f, 1)[0:-1]
        items.append(f'<li>{line}</li>')

        # Check if we are still in a list
        test_token = peek(f, 3)[0:-1]
        if test_token.startswith("<UNORDERED") or test_token.startswith("<ORDERED"):
            # Read up to start line
            f.readline()
            f.readline()

            line_parts = get_start_ol_num(test_token)
            start_parts = get_start_ol_num(start)
            if line_parts[0] != start_parts[0]:
                # If we've already seen this element then we need to go back
                # Else recurse to inner list
                if line_parts[0] in seen:
                    break
                else:
                    items.append(generate_list(f, test_token, seen))

    # Ending tag of list
    if start.startswith("<ORDERED"):
        items.append("</ol>")
    else:
        items.append("</ul>")

    return "".join(items)

# Helper function to get starting num of ordered list
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
