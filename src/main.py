'''
    py-webbuilder
    Author: Paul Shriner

    main: Entry point for program
'''

from default import create_index_md, create_global_md, clear_all
from file import file_exists
from parser import parse_content_file
from gen import generate_html
from finalize import create_html

def main():
    clear_all()
    
    # Get global config vars from global.md (if there's content it will be ignored)
    if not file_exists('../input/global.md'):
        create_global_md()
    global_config = parse_content_file('../input/global.md')
    global_config["<CONFIG_HOME_LINK>"] = 'index.html'

    # Create default index page if needed, parse content from it
    if not file_exists('../input/index.md'):
        create_index_md()
    page_config = parse_content_file('../input/index.md')

    # Generate HTML, create an index.html page
    generate_html('../temp/index.tmp')
    create_html('../themes/default', global_config, page_config, '../temp/index.final')

if __name__ == "__main__":
    main()
