'''
    py-webbuilder
    Author: Paul Shriner

    finalize: Creates an HTML document using template files and previously generated HTML
'''

import shutil
import os

def create_html(root_path: str, theme: str, config_file_path, final_file_path) -> None:
    # Change directory to root, thanks https://stackoverflow.com/a/32470697
    os.chdir(root_path)

    # Copy template file from theme to output dir, thanks https://stackoverflow.com/a/123212
    try:
        # Create output dir if needed, if already exists just continue
        os.mkdir('output')
    except FileExistsError:
        pass

    # Get name to use for output file
    # Use rfind to get last slash in directory
    # If it's -1 then whole name would be used
    slash_index = final_file_path.rfind('/')
    output_file_name = final_file_path[slash_index+1:][0:-6]
    shutil.copyfile(f'{theme}/templates/base.html', f"output/{output_file_name}.html")

    final_file = open(f"{final_file_path}", 'r')

    # Thanks https://www.geeksforgeeks.org/python/how-to-search-and-replace-text-in-a-file-in-python/ for reading and writing to portion of file
    # Will replace portions in html file with our content
    # TODO: Need to do all places in HTML
    with open(f"output/{output_file_name}.html", 'r') as output_file:
        data = output_file.read()
        data = data.replace("{{CONTENT}}", final_file.read())

    with open(f"output/{output_file_name}.html", 'w') as output_file:
        output_file.write(data)
    
    final_file.close()
