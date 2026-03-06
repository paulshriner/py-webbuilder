'''
    py-webbuilder
    Author: Paul Shriner

    default: Create default input files, clear existing files
'''

from file import create_dir, remove_dir

# Each element is a Markdown line in the file
DEFAULT_INDEX = [
    "# Welcome to py-webbuilder!",
    "This is the main page for your website."
]
DEFAULT_GLOBAL_CONFIG = [
    "{",
    "Home: A New Website!",
    "Links: [Posts](posts), [About](about)",
    "Footer: You can add your name or copyright info here!",
    "}"
]

# Creates a index.md file with default content
# WARNING: This will overwrite an existing index.md!
def create_index_md() -> None:
    # Create input dir if needed
    create_dir("input")

    # Create input file
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

    # Create input file
    input_file = open("../input/global.md", 'w')
    for line in DEFAULT_GLOBAL_CONFIG:
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
