import os
import shutil


def copy_contents_of_dir(src: str, dest: str) -> None:
    if not os.path.exists(src) or not os.path.exists(dest):
        raise ValueError("Source and destination must be valid directories")

    shutil.rmtree(dest)

    os.mkdir(dest)
    contents = os.listdir(src)

    for item in contents:
        if os.path.isfile(os.path.join(src, item)):
            shutil.copy(os.path.join(src, item), os.path.join(dest, item))
        else:
            os.mkdir(os.path.join(dest, item))
            copy_contents_of_dir(os.path.join(src, item), os.path.join(dest, item))


def main():
    copy_contents_of_dir("static", "public")


if __name__ == "__main__":
    main()
