# py-webbuilder

A Markdown parser and static website builder using Python

## Overview

The idea of this project is to allow creating a static website through Markdown files, which are more approachable than raw HTML. It is built using Python, without using a library such as [Markdown](https://pypi.org/project/Markdown/) that would do much of the work. I got the idea from using [Hugo](https://gohugo.io/) for static websites in the past, which also generates content through Markdown files. My goal is not to make something as fully-featured and production-ready as Hugo, but rather to use this to gain experience in Python and create a potentially useful project.

## Features

- Parse common Markdown syntax and generate corresponding HTML [In Progress]
- Create HTML documents based on template files from default theme or user-specified theme [In Progress]
- Use a configuration Markdown file for site-wide constants like the title in the header [In Progress]
- Sanitize HTML in content files to ensure security [In Progress]
    - No HTML tags are rendered or converted to Markdown. While other Markdown parsers do this, the goal here is to only use Markdown in an input file, not HTML.
- Check modified file dates of input files and only rebuild if newer than output [Not Started]
- Have a CLI (GUI?) for setting options [Not Started]
- ...more as I develop the project!

## Development Tools

- [Git](https://git-scm.com/), [GitHub](https://github.com/) - Version Control
- [VS Code](https://code.visualstudio.com/) - Development Environment
