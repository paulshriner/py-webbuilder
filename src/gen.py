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

    line = temp_ptr.readline()
    html_line = []
    index = 0
    # TODO: Refactor this some more
    while line:
        line_stripped = line[0:-1]

        match line_stripped:
            case "<UNORDERED_LIST>":
                html_line.append(generate_list(temp_ptr, line_stripped))
                index += 1
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

        line = temp_ptr.readline()

    # Close files when done
    temp_ptr.close()
    final_ptr.close()

# Generates the HTML for a list
# Takes a file pointer and current line (the intermediate token), returns string with HTML list
# TODO: Only does unordered now, need to do ordered
# TODO: Need to account for potential other block elements within a list
def generate_list(f: TextIO, line: str) -> str:
    seen = [line]
    result = []
    index = 0
    new_list = True
    done = False

    while not done:
        # Create a new outer list
        if new_list:
            tag = get_html_tag(line)
            result.insert(index, f"<{tag}>")
            index += 1
            result.insert(index, f"</{tag}>")
            new_list = False

        line = f.readline()
        if line:
            # Add element to list
            line_stripped = line[0:-1]
            result.insert(index, f"<li>")
            index += 1
            result.insert(index, line_stripped)
            index += 1
            result.insert(index, f"</li>")
            index += 1

            # Part of same list so just read to that token
            if peek(f, 2) == f"{seen[-1]}\n":
                line = f.readline()
                line = f.readline()
            # Still a list but different kind
            elif peek(f, 2).startswith("<UNORDERED_LIST"):
                # New list, set to create a new list
                if peek(f, 2)[0:-1] not in seen:
                    seen.append(peek(f, 2)[0:-1])
                    new_list = True
                # Part of another list, so we need to advance index to that list
                else:
                    seen_index = seen.index(peek(f, 2)[0:-1])
                    skip = len(seen) - (seen_index + 1)
                    while skip >= 0:
                        index = result.index("</ul>", index)
                        seen_index -= 1
                        skip -= 1
                    index += 1
                    del seen[seen_index+1:]

                line = f.readline()
                line = f.readline()
            else:
                done = True
        else:
            done = True

    return "".join(result)

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
    
    # Any nested list would still use <ul>
    if line.startswith("<UNORDERED_LIST"):
        return "ul"
    
    return line
