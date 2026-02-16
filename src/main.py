import parser
import os
from create_html import create_html
from gen import generate_html

def main():
    # Change directory to root, thanks https://stackoverflow.com/a/32470697
    os.chdir('../')
    # Save current dir, needed as functions will change the directory
    # Thanks https://www.w3schools.com/python/ref_os_getcwd.asp for getcwd()
    root_path = os.getcwd()
    
    parser.parse_content_file(root_path, './input/index.md')
    generate_html(root_path, './temp/index.tmp')
    create_html(root_path, './themes/default', "", './temp/index.final')

if __name__ == "__main__":
    main()
