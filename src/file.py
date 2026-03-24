'''
    py-webbuilder
    Author: Paul Shriner

    file: Contains file related functionality
'''

from shutil import copytree, rmtree
from typing import TextIO
from pathlib import Path

# Helper function that returns the directory to work from
# NOTE: This will throw an exception for path traversals like '../../'.
# This is normal, you should use a path like 'input/index.md' with the assumption you are one dir above src
def get_working_dir(dir_path: str) -> Path:
    # Get parent dir (this would be the project folder)
    # Thanks https://docs.python.org/3/library/pathlib.html for pathlib documentation
    parent_dir = Path.cwd().parent

    # Create the path to dir_path
    full_path = (parent_dir / dir_path).resolve()
    # Make sure we did not go above project folder
    try:
        full_path.relative_to(parent_dir)
    except ValueError:
        raise ValueError(f'Path traversal found: {dir_path}')

    return full_path

# Takes in a file path
# This should be a relative path, like "input/index.md", starting from the repo root
# Returns True if file exists, False if not
def file_exists(path: str) -> bool:
    return get_working_dir(path).exists()

# Takes in a file path
# Returns a tuple of format (filename, ext)
def get_file_name(path: str) -> tuple[str, str]:
    # Don't need to check for invalid dirs as that doesn't matter, we just want the filename
    p = Path(path)
    return (p.stem, p.suffix)

# Takes in a path starting from root to a dir, like "output/posts"
# If dir already exists this does nothing
def create_dir(name: str) -> None:
    get_working_dir(name).mkdir(parents=True, exist_ok=True)

# Copies a directory to another location
# WARNING: Will overwrite existing directory
# Will throw exception if source does not exist
def copy_dir(source: str, dest: str) -> None:
    # Thanks https://stackoverflow.com/a/31039095 for copytree
    copytree(get_working_dir(source), get_working_dir(dest), dirs_exist_ok=True)

# Return list of all files inside a directory
# If dir doesn't exist this will return an empty list
def get_all_dir_files(dir: str) -> list[str]:
    files = []
    
    try:
        # Append every file in dir to files list
        # This will not go into subdirectories
        for e in get_working_dir(dir).iterdir():
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

# Removes an entire directory
# WARNING: All content in directory will be lost!
# If directory not found this will do nothing
def remove_dir(dir_path: str) -> None:
    try:
        rmtree(get_working_dir(dir_path))
    except FileNotFoundError:
        pass
