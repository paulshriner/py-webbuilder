'''
    py-webbuilder
    Author: Paul Shriner

    main: Entry point for program
'''

import os
from parser import parse_content_file
from gen import generate_html
from finalize import create_html

def main():
    # Change directory to root, thanks https://stackoverflow.com/a/32470697
    os.chdir('../')
    # Save current dir, needed as functions will change the directory
    # Thanks https://www.w3schools.com/python/ref_os_getcwd.asp for getcwd()
    root_path = os.getcwd()
    
    parse_content_file(root_path, './input/index.md')
    generate_html(root_path, './temp/index.tmp')
    create_html(root_path, './themes/default', "", './temp/index.final')

if __name__ == "__main__":
    main()
