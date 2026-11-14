def markdown_to_blocks(markdown: str) -> list[str]:
    return list(filter(lambda x: x, map(lambda x: x.strip(), markdown.split("\n\n"))))
