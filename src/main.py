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
    parse_content_file('../input/index.md')
    generate_html('../temp/index.tmp')
    create_html('../themes/default', "", '../temp/index.final')

if __name__ == "__main__":
    main()
