import os
import shutil


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


def main():
    copy_static("static", "public")


if __name__ == "__main__":
    main()
