'''
    py-webbuilder
    Author: Paul Shriner

    file: Contains file related functionality
'''

import os

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
