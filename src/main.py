import os
import shutil

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


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html_content = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content
    )

    dest_dir = os.path.dirname(dest_path)

    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(html_content)


def main():
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
