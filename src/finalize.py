'''
    py-webbuilder
    Author: Paul Shriner

    finalize: Creates an HTML document using template files and previously generated HTML
'''

import shutil
import os
from file import get_file_name, create_dir

def create_html(theme: str, config_file_path, final_file_path) -> None:
    # Create output dir if needed
    create_dir("output")

    # Get name to use for output file
    output_file_name = get_file_name(final_file_path)[0]
    # Copy template file from theme to output dir, thanks https://stackoverflow.com/a/123212 
    shutil.copyfile(f'{theme}/templates/base.html', f"../output/{output_file_name}.html")

    final_file = open(f"{final_file_path}", 'r')

    # Thanks https://www.geeksforgeeks.org/python/how-to-search-and-replace-text-in-a-file-in-python/ for reading and writing to portion of file
    # Will replace portions in html file with our content
    # TODO: Need to do all places in HTML
    with open(f"../output/{output_file_name}.html", 'r') as output_file:
        data = output_file.read()
        data = data.replace("{{CONTENT}}", final_file.read())

    with open(f"../output/{output_file_name}.html", 'w') as output_file:
        output_file.write(data)
    
    final_file.close()
