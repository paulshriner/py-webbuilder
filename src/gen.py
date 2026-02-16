import os

def generate_html(root_path: str, temp_file_path: str) -> None:
    # Change directory to root
    os.chdir(root_path)

    # Get name to use for temp file
    # Use rfind to get last slash in directory
    # If it's -1 then whole name would be used
    slash_index = temp_file_path.rfind('/')
    file_name = temp_file_path[slash_index+1:][0:-4]

    temp_file = open(temp_file_path, 'r')
    final_file = open(f"temp/{file_name}.final", 'w')
    html_line = []
    ending_tags = []
    for line in temp_file:
        # Need this as each line has a newline at the end, we don't want this
        line_stripped = line[0:-1]

        match line_stripped:
            case "<HEADING_1>":
                html_line.append("<h1>")
                ending_tags.append("</h1>")
            case "<HEADING_2>":
                html_line.append("<h2>")
                ending_tags.append("</h2>") 
            case "<HEADING_3>":
                html_line.append("<h3>")
                ending_tags.append("</h3>") 
            case "<HEADING_4>":
                html_line.append("<h4>")
                ending_tags.append("</h4>") 
            case "<HEADING_5>":
                html_line.append("<h5>")
                ending_tags.append("</h5>") 
            case "<HEADING_6>":
                html_line.append("<h6>")
                ending_tags.append("</h6>")
            case "<TEXT>":
                html_line.append("<p>")
                ending_tags.append("</p>")
            case "<NEW_LINE>":
                for i in ending_tags[::-1]:
                    html_line.append(i)
                final_file.write("".join(html_line) + "\n")
                html_line = []
                ending_tags = []                
            case "<EMPTY_LINE>":
                final_file.write("<br>" + "\n")              
            case default:
                html_line.append(line_stripped)

    # Close files when done
    temp_file.close()
    final_file.close()
