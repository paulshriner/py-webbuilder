'''
    py-webbuilder
    Author: Paul Shriner

    finalize: Creates an HTML document using template files and previously generated HTML
'''

import shutil
from file import get_file_name, create_dir

def create_html(theme: str, global_config: dict, page_config: dict, final_file_path: str) -> None:
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
    # TODO: CONFIG_HOME should be a link to index.html
    with open(f"../output/{output_file_name}.html", 'r') as output_file:
        # Replace content with associated data for this page
        data = output_file.read()
        data = data.replace("{{CONTENT}}", final_file.read())

        # Replace values for global config
        for key, val in global_config.items():
            if key == "<CONFIG_HOME>":
                data = data.replace("{{NAV_TITLE}}", val)
            if key == "<CONFIG_HOME_LINK>":
                data = data.replace("{{NAV_TITLE_LINK}}", val)
            if key == '<CONFIG_NAV_LINKS>':
                data = data.replace("{{NAV_LINKS}}", "".join(val))
            if key == "<CONFIG_FOOTER>":
                data = data.replace("{{FOOTER_INFO}}", val)

    with open(f"../output/{output_file_name}.html", 'w') as output_file:
        output_file.write(data)
    
    final_file.close()
