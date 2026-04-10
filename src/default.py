'''
    py-webbuilder
    Author: Paul Shriner

    default: Create default input files, clear existing files
'''

import datetime
from pathlib import Path
from file import create_dir, remove_dir

# Each element is a Markdown line in the file
DEFAULT_GLOBAL_CONFIG = [
    "{",
    "Home: A New Website!",
    "Links: [Posts](posts)",
    "Footer: You can add your name or copyright info here!",
    "}"
]
DEFAULT_INDEX = '''# Welcome to py-webbuilder!
---
This is the landing page for your website. You can edit this page by going to `input/index.md`.

'''
DEFAULT_POST = '''# Welcome to py-webbuilder!
---
This is a post on your website. You can edit this page by going to `input/posts/{{FILE_NAME}}.md`.
You can make a new post by creating a Markdown file in the `input/posts folder.`

'''
DEFAULT_FEATURES = '''## Features
---
### Paragraphs
Paragraphs are written as is without any symbols or formatting.

Markdown:
`You can write a paragraph just by writing it out.`
HTML:
You can write a paragraph just by writing it out.

### Headings
You can have up to 6 levels of headings by adding pound signs and a space before the text.

Markdown:
```
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```
HTML:
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

### Line Breaks
A line break is created by entering empty lines in your file. This is different than other Markdown parsers where you end a line with multiple spaces to create a new line. Here, an empty line is a new line.

Markdown:
```
There are 3 empty lines between here...



...and here!
```
HTML:
There are 3 empty lines between here...



...and here!

### Inline Elements
You can have inline elements including bold and italic. Bold is created by adding 2 asterisks before and after the text. For italic, it is 1.

Markdown:
```
The text **here** is bold and the text *here* is italic.
```

HTML:
The text **here** is bold and the text *here* is italic.

### Lists
Unordered lists are created by having a *, -, or + followed by one space. Ordered lists are created by having a number, a period, then one space.

Markdown:
```
* Here
- is
+ an unordered list

1. And here
2. is
3. an ordered list

* You
&nbsp;&nbsp;&nbsp;&nbsp;* Can
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Even
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Have
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* Nested
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Lists!
```

HTML:
* Here
* is
* an unordered list

1. And here
2. is
3. an ordered list

* You
    * Can
        1. Even
        2. Have
            * Nested
                1. Lists!

### Code
You can write a code line by enclosing it in backticks, or a code block by having a line with three backticks above and below the text.

Markdown:
```
Here is how to print Hello World in Python: `print("Hello World")`.

You can declare a string in Python by doing:
&nbsp;```
read_this = "Pretend there is no space here, otherwise it would end the demonstration code block."
&nbsp;```
```

HTML:
Here is how to print Hello World in Python: `print("Hello World")`.

You can declare a string in Python by doing:
```
read_this = "Pretend there is no space here, otherwise it would end the demonstration code block."
```

### Horizontal Rules
You can create a horizontal rule by adding three asterisks, dashes, or underscores on a single line.

Markdown:
```
This line has a horizontal rule under it.
***
```

HTML:
This line has a horizontal rule under it.
***

### Links
You can create a link to files within the input folder or to external websites. When you link to a file, do `posts/post.md`, not `input/posts/post.md` or similar.

Markdown:
```
[Here](https://duckduckgo.com) is a link to the search engine DuckDuckGo.
```

HTML:
[Here](https://duckduckgo.com) is a link to the search engine DuckDuckGo.

### Images
Images are similar to links, but with an exclamation point(!) preceding the left bracket([), and after the link you can add a title in quotation marks.

Markdown:
```
![Alt Text of Image](/images/image.png "Title of Image")
```

HTML:
(The Markdown code given is an example but if it wasn't you'd see an image here.)
'''

# Creates a index.md file with default content
# WARNING: This will overwrite an existing index.md!
def create_index_md() -> None:
    # Create input dir if needed
    create_dir("input")

    # Create new index file
    input_file = open(Path("../input/index.md"), 'w')

    # Write config section
    input_file.write('{\n')
    input_file.write('Summary: The main page of your website.\n')
    input_file.write('}\n')

    # Write content for the page
    input_file.write(DEFAULT_INDEX)
    input_file.write(DEFAULT_FEATURES)

    # Close file when done
    input_file.close()

# Create a global.md file with default content
# WARNING: This will overwrite an existing global.md!
def create_global_md() -> None:
    # Create input dir if needed
    create_dir("input")

    # Create new global file
    input_file = open(Path("../input/global.md"), 'w')
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
    # Remove colons from time as they can't be in filenames on Windows
    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
    input_file = open(Path(f"../input/posts") / f"{file_name}.md", 'w')

    # Create config section
    input_file.write("{\n")
    input_file.write(f"Title: {file_name}\n")
    input_file.write('Summary: A post on your website.\n')
    input_file.write("}\n")

    # Create post content
    input_file.write(DEFAULT_POST.replace("{{FILE_NAME}}", str(file_name)))
    input_file.write(DEFAULT_FEATURES)

    # Close file when done
    input_file.close()

# Create a final file for the posts page
# Returns path to the file
def create_final_posts(content: list[str]) -> str:
    # Create temp dir if needed
    create_dir("temp")

    # Create new file
    # Remove colons from time as they can't be in filenames on Windows
    input_file = open(Path(f"../temp") / f"posts.final", 'w')

    # Write heading of file
    input_file.write("<h1>Posts</h1>\n")

    # Write lines to file
    for i in content:
        input_file.write(f'{i}\n')
        input_file.write("<br>\n")

    # Close file when done
    input_file.close()

    return f'temp/posts.final'

# Removes all content directories
# WARNING: All content in directory will be lost!
# Default behavior is not to clear input unless True is passed for input
def clear_all(input: bool = False) -> None:
    if input:
        remove_dir("input")
    remove_dir("output")
    remove_dir("temp")
