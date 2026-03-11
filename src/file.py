'''
    py-webbuilder
    Author: Paul Shriner

    file: Contains file related functionality
'''

import os, shutil
from typing import TextIO

# Takes in a file path
# Returns a tuple of format (filename, ext)
def get_file_name(file_path: str) -> tuple[str, str]:
    # Use rfind to get last slash in directory
    # If it's -1 then whole name would be used
    slash_index = file_path.rfind('/')
    file_name = file_path[slash_index+1:]
    
    # Split filename and file extension, thanks https://stackoverflow.com/a/541394
    return os.path.splitext(file_name)

# Takes in a dir name
# Will create from root dir
# If dir already exists this does nothing
def create_dir(name: str) -> None:
    try:
        os.mkdir(f'../{name}')
    except FileExistsError:
        pass

# Copies a directory to another location
# WARNING: Will overwrite existing directory
def copy_dir(source: str, dest: str) -> None:
    # Thanks https://stackoverflow.com/a/31039095 for copytree
    shutil.copytree(source, dest, dirs_exist_ok=True)

# Return list of all files inside a directory
# Thanks https://www.geeksforgeeks.org/python/python-loop-through-folders-and-files-in-directory/
# If dir doesn't exist this will return an empty list
def get_all_dir_files(dir: str) -> list[str]:
    files = []
    
    try:
        for e in os.scandir(dir):
            if e.is_file():
                files.append(e.name)
    except FileNotFoundError:
        pass
    
    return files

# Return a line without advancing the file pointer (file peek)
# Specify number of lines to skip using lines
# Thanks https://stackoverflow.com/a/16840747 for file peeking
# Thanks https://stackoverflow.com/a/58887007 for type hinting for file pointer
def peek(f: TextIO, lines: int) -> str:
    pos = f.tell()
    line = ""
    for i in range(0, lines):
        line = f.readline()
    f.seek(pos)

    return line

# Returns if a file exists at a given path
def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

# Removes an entire directory
# WARNING: All content in directory will be lost!
# If directory not found this will do nothing
def remove_dir(dir_path: str) -> None:
    try:
        shutil.rmtree(dir_path)
    except FileNotFoundError:
        pass
