from textnode import TextNode, TextType


def main():
    node = TextNode("lots of farts", TextType.TEXT, "https://www.farts.com")
    print(node)


if __name__ == "__main__":
    main()
