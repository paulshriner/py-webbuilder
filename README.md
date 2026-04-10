# py-webbuilder

A Markdown parser and static website builder using Python

## Overview

The idea of this project is to allow creating a static website through Markdown files, which are more approachable than raw HTML. It is built using Python, without using a library such as [Markdown](https://pypi.org/project/Markdown/) that would do much of the work. I got the idea from using [Hugo](https://gohugo.io/) for static websites in the past, which also generates content through Markdown files. My goal is not to make something as fully-featured and production-ready as Hugo, but rather to use this to gain experience in Python and create a potentially useful project.

## Features

- Parse common Markdown syntax and generate corresponding HTML
- Create HTML documents based on template files from default theme
    - A different theme can be created as long as it uses the same placeholder variables
- Use a configuration Markdown file for site-wide constants like the title in the header
- Sanitize HTML in content files to ensure security
    - No HTML tags are rendered or converted to Markdown. While other Markdown parsers do this, the goal here is to only use Markdown in an input file, not HTML
- Check modified file dates of input files and only rebuild if newer than output
- Has a basic CLI to run the program

## How to Run

You will need Python installed on your computer. You can download Python from [here](https://www.python.org/downloads/).

To run, first download the project (either from releases or cloning the repo). Then open a terminal and navigate to the src folder. Finally, run `python main.py` in the terminal.

## Usage

You will be presented with a menu of options. Option 1 will run the program. If this is your first time running the program, it will generate default files to work off of. The input folder will have Markdown files you can edit, and the output will be the resultant website. A temp folder is created that has intermediate files, these are not needed after the program is ran but are kept to speed up future runs.

Running the program again using option 1 will recreate your website without deleting any input or intermediate files. Option 2 will delete intermediate files, while option 3 will delete everything.

## Development Tools

- [Git](https://git-scm.com/), [GitHub](https://github.com/) - Version Control
- [VS Code](https://code.visualstudio.com/) - Development Environment
