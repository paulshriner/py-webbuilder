'''
    py-webbuilder
    Author: Paul Shriner

    gen: Converts intermediate code into final code
'''

from file import get_file_name

# Generates HTML code from a parsed intermediate file
def generate_html(temp_file_path: str) -> None:
    # Get name to use for temp file
    file_name = get_file_name(temp_file_path)[0]

    temp_file = open(temp_file_path, 'r')
    final_file = open(f"../temp/{file_name}.final", 'w')
    html_line = []
    index = 0
    for line in temp_file:
        # Need this as each line has a newline at the end, we don't want this
        line_stripped = line[0:-1]

        match line_stripped:
            case "<HEADING_1>":
                html_line.insert(index, "<h1>")
                index += 1
                html_line.insert(index, "</h1>")
            case "<HEADING_2>":
                html_line.insert(index, "<h2>")
                index += 1
                html_line.insert(index, "</h2>")
            case "<HEADING_3>":
                html_line.insert(index, "<h3>")
                index += 1
                html_line.insert(index, "</h3>")
            case "<HEADING_4>":
                html_line.insert(index, "<h4>")
                index += 1
                html_line.insert(index, "</h4>")
            case "<HEADING_5>":
                html_line.insert(index, "<h5>")
                index += 1
                html_line.insert(index, "</h5>")
            case "<HEADING_6>":
                html_line.insert(index, "<h6>")
                index += 1
                html_line.insert(index, "</h6>")
            case "<TEXT>":
                html_line.insert(index, "<p>")
                index += 1
                html_line.insert(index, "</p>")
            case "<NEW_LINE>":
                final_file.write("".join(html_line) + "\n")
                html_line = []
                index = 0               
            case "<EMPTY_LINE>":
                final_file.write("<br>" + "\n")              
            case default:
                html_line.insert(index, line_stripped)
                index += 1

    # Close files when done
    temp_file.close()
    final_file.close()
