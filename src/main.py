from blocks import extract_title, markdown_to_html_node
import os
import shutil


def dir_copy_recurse(from_dir, to_dir):
    if not os.path.exists(from_dir):
        raise ValueError("Path does not exist")

    # Base case, file, already copied so don't act
    if os.path.isfile(from_dir):
        return

    # Recurse case, directory
    names = os.listdir(from_dir)

    for name in names:
        path = os.path.join(from_dir, name)
        to_path = os.path.join(to_dir, name)

        if os.path.isfile(path):
            shutil.copy(path, to_dir)
        else:
            os.mkdir(to_path)
            dir_copy_recurse(path, to_path)


def generate_page(from_path, template_path, dest_path):
    title_template = '{{ Title }}'
    body_template = '{{ Content }}'

    print(f"Generating page with {from_path} using {
          template_path} to {dest_path}...")

    with open(from_path) as f:
        markdown = f.readline()
        title = extract_title(markdown)
        markdown += f.read()

    with open(template_path) as f:
        template_html = f.read()

    markdown_html = markdown_to_html_node(markdown).to_html()
    template_html = template_html.replace(title_template, title)
    template_html = template_html.replace(body_template, markdown_html)

    with open(dest_path, "w") as f:
        f.write(template_html)

    print("Generation complete!")


if __name__ == "__main__":
    which = input("Would you like to [c]opy or [w]rite?")

    if which[0] == 'c':

        from_dir = input("Copy from: ")
        to_dir = input("Copy to: ")

        print("Copying directory...")
        dir_copy_recurse(from_dir, to_dir)
        print("Copy complete!")

    elif which[0] == 'w':
        page_path = input("Enter markdown file path: ")
        dest_path = input(
            "Enter destination file path (include desired filename!): ")
        generate_page(page_path, 'template.html', dest_path)
