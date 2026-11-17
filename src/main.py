import os
import shutil
import sys

from block_markdown import markdown_to_html_node


def copy_static(src: str, dest: str) -> None:
    if not os.path.isdir(src):
        raise ValueError("Source must be a valid directory")

    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_static(src_path, dest_path)


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# ") and line[2:].strip():
            return line[2:].strip()

    raise ValueError("Markdown must contain h1 header")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html_content = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace("href='/", f"href='{basepath}")
        .replace("src='/", f"src='{basepath}")
    )

    dest_dir = os.path.dirname(dest_path)

    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(html_content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
) -> None:
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path, basepath)

        elif os.path.isfile(src_path) and item.endswith(".md"):
            html_path = os.path.splitext(dest_path)[0] + ".html"
            generate_page(src_path, template_path, html_path, basepath)


def main():
    args = sys.argv
    basepath: str
    if len(args) > 0:
        basepath = sys.argv[0]
    else:
        basepath = "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
