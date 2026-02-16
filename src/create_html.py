import shutil
import os

def create_html(root_path: str, theme: str, config, content) -> None:
    # Change directory to root, thanks https://stackoverflow.com/a/32470697
    os.chdir(root_path)

    # Copy template file from theme to output dir, thanks https://stackoverflow.com/a/123212
    try:
        # Create output dir if needed, if already exists just continue
        os.mkdir('output')
    except FileExistsError:
        pass
    # TODO: Use dynamic output file name (this will come with having content as file)
    shutil.copyfile(f'{theme}/templates/base.html', f"output/content.html")

    content_file = open(f"{content}", 'r')

    # Thanks https://www.geeksforgeeks.org/python/how-to-search-and-replace-text-in-a-file-in-python/ for reading and writing to portion of file
    # Will replace portions in html file with our content
    # TODO: Need to do all places in HTML
    # TODO: Need to get content from a file
    with open(f"output/content.html", 'r') as output_file:
        data = output_file.read()
        data = data.replace("{{CONTENT}}", content_file.read())

    with open(f"output/content.html", 'w') as output_file:
        output_file.write(data)
    
    content_file.close()
