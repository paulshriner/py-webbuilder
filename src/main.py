'''
    py-webbuilder
    Author: Paul Shriner

    main: Entry point for program
'''

from default import create_index_md, create_global_md, create_post, clear_all
from file import file_exists, get_all_dir_files, get_file_name, copy_dir
from parser import parse_content_file
from gen import generate_html
from finalize import create_html

def main() -> None:
    clear_all()
    
    # Get global config vars from global.md (if there's content it will be ignored)
    if not file_exists('input/global.md'):
        create_global_md()
    global_config = parse_content_file('input/global.md')
    global_config["<CONFIG_HOME_LINK>"] = 'index.html'

    # Create default index page if needed, parse content from it
    if not file_exists('input/index.md'):
        create_index_md()

    # Generate HTML, create an index.html page
    page_config = parse_content_file('input/index.md')
    page_config["<CONFIG_CSS_PATH>"] = 'styles/styles.css'
    # NOTE: If user specified a custom title for index.md it will get overwritten here
    # This is intentional, the index title should match the overall title
    page_config["<CONFIG_TITLE>"] = global_config["<CONFIG_HOME>"]
    generate_html('temp/index.tmp')
    create_html('themes/default', global_config, page_config, 'temp/index.final', 'output')

    # Get lists of posts, create default post if needed
    posts = get_all_dir_files('input/posts')
    if not posts:
        create_post()
        posts = get_all_dir_files('input/posts')

    # Generate HTML for each post
    for post in posts:
        file_name, file_ext = get_file_name(post)
        if file_ext == ".md":
            page_config = parse_content_file(f'input/posts/{post}')
            page_config["<CONFIG_CSS_PATH>"] = '../styles/styles.css'
            generate_html(f'temp/{file_name}.tmp')
            create_html('themes/default', global_config, page_config, f'temp/{file_name}.final', 'output/posts')

    # Copy styles from theme to output
    copy_dir("themes/default/styles", "output/styles")

if __name__ == "__main__":
    main()
