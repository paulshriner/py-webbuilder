'''
    py-webbuilder
    Author: Paul Shriner

    default: Create default input files, clear existing files
'''

from file import create_dir, remove_dir
import datetime

# Each element is a Markdown line in the file
DEFAULT_GLOBAL_CONFIG = [
    "{",
    "Home: A New Website!",
    "Links: [Posts](posts), [About](about)",
    "Footer: You can add your name or copyright info here!",
    "}"
]
DEFAULT_INDEX = [
    "# Welcome to py-webbuilder!",
    "This is the main page for your website."
]
DEFAULT_POST = [
    "# Welcome to py-webbuilder!",
    "This is a post on your website.",
    "You can add more posts in the 'posts' folder."
]

# Creates a index.md file with default content
# WARNING: This will overwrite an existing index.md!
def create_index_md() -> None:
    # Create input dir if needed
    create_dir("input")

    # Create new index file
    input_file = open("../input/index.md", 'w')
    for line in DEFAULT_INDEX:
        input_file.write(f"{line}\n")

    # Close file when done
    input_file.close()

# Create a global.md file with default content
# WARNING: This will overwrite an existing global.md!
def create_global_md() -> None:
    # Create input dir if needed
    create_dir("input")

    # Create new global file
    input_file = open("../input/global.md", 'w')
    for line in DEFAULT_GLOBAL_CONFIG:
        input_file.write(f"{line}\n")

    # Close file when done
    input_file.close()

# Create a post with default content
# Use datetime stamp for filename, should not overwrite preexisting file
def create_post() -> None:
    # Create input dir if needed
    create_dir("input")

    # Create posts dir if needed
    create_dir("input/posts")

    # Create new post file
    file_name = datetime.datetime.now()
    input_file = open(f"../input/posts/{file_name}.md", 'w')

    # Create config section
    input_file.write("{\n")
    input_file.write(f"Title: {file_name}\n")
    input_file.write("}\n")

    # Create post content
    for line in DEFAULT_POST:
        input_file.write(f"{line}\n")

    # Close file when done
    input_file.close()

# Removes all content directories
# WARNING: All content in directory will be lost!
# Default behavior is not to clear input unless True is passed for input
def clear_all(input: bool = False) -> None:
    if input:
        remove_dir("../input")
    remove_dir("../output")
    remove_dir("../temp")
