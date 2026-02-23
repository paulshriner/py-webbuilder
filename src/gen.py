'''
    py-webbuilder
    Author: Paul Shriner

    gen: Converts intermediate code into final code
'''

from file import get_file_name, peek

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
                # Create outer list
                tag = get_html_tag(line_stripped)
                html_line.insert(index, f"<{tag}>")
                index += 1
                html_line.insert(index, f"</{tag}>")

                # Consume any further list elements and add them to list
                # TODO: This will need changed for nested lists
                line = temp_ptr.readline()
                while line:
                    line_stripped = line[0:-1]
                    html_line.insert(index, f"<li>")
                    index += 1
                    html_line.insert(index, line)
                    index += 1
                    html_line.insert(index, f"</li>")

                    if peek(temp_ptr, 2) == "<UNORDERED_LIST>\n":
                        line = temp_ptr.readline()
                        line = temp_ptr.readline()
                        line = temp_ptr.readline()
                    else:
                        break
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

# Helper function to get matching HTML tag for intermediate tag
def get_html_tag(line):
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
        case "<UNORDERED_LIST>":
            return "ul"
        case "<TEXT>":
            return "p"
    
    return line
