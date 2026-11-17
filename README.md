# Static Site Generator

A static site generator built from scratch in Python as part of [Boot.dev's Build a Static Site Generator course](https://www.boot.dev/courses/build-static-site-generator-python). It converts Markdown files into HTML, applies a reusable page template, copies static assets, and generates a multi-page website that can be hosted on GitHub Pages.

**[View the live site](https://bsul24.github.io/static-site-generator/)** · **[Source code](https://github.com/bsul24/static-site-generator)**

## Features

- Converts a subset of Markdown into HTML, including headings, paragraphs, bold and italic text, inline code, fenced code blocks, links, images, blockquotes, and ordered/unordered lists.
- Uses custom `TextNode` and `HTMLNode` classes to build and render HTML without a Markdown parsing library.
- Recursively generates HTML pages from Markdown files in `content/`, preserving their directory structure.
- Applies a shared `template.html`, inserting each page's H1 title and generated HTML content.
- Copies files and nested directories from `static/` into the generated site.
- Supports configurable URL base paths for local development and GitHub Pages deployment.
- Includes unit tests for Markdown parsing, HTML nodes, file copying, title extraction, and page generation.

## Project structure

```text
static-site-generator/
├── content/              # Markdown pages (including nested pages)
├── static/               # Images, CSS, and other static assets
├── docs/                 # Generated website; published through GitHub Pages
├── src/
│   ├── main.py           # Site build and file-generation pipeline
│   ├── block_markdown.py # Markdown block parsing and HTML conversion
│   ├── inline_markdown.py # Inline Markdown parsing
│   ├── htmlnode.py       # HTML node classes
│   └── textnode.py       # Text node classes and conversion
├── tests/                # unittest test suite
├── template.html         # Shared HTML template
├── main.sh               # Build and serve locally
├── build.sh              # Build for GitHub Pages
└── test.sh               # Run automated tests
```

## Requirements

- Python 3 (no third-party Python packages required)
- Bash or a compatible shell for the provided scripts
- Git, if you want to clone the repository or deploy changes

## Run locally

Clone the repository and start the development server:

```bash
git clone https://github.com/bsul24/static-site-generator.git
cd static-site-generator
bash main.sh
```

Open **http://localhost:8888** in your browser.

`main.sh` builds the site using `/` as the base path, then serves the generated `docs/` directory using Python's built-in HTTP server. Stop the server with **Ctrl+C**.

## Run tests

```bash
bash test.sh
```

The test script runs Python's built-in `unittest` discovery with `src/` on the Python import path. No additional test framework is needed.

## Build for GitHub Pages

```bash
bash build.sh
```

This generates the site in `docs/` with the base path `/static-site-generator/`, so internal links and asset URLs work when the site is hosted under that repository path.

The repository's GitHub Pages deployment uses the generated `docs/` directory. After building, commit and push the updated files as needed:

```bash
git add docs/ content/ static/ src/ template.html README.md
git commit -m "Update generated site"
git push
```

**Important:** `main.sh` and `build.sh` both regenerate `docs/`. The local build uses `/` for URLs, while the GitHub Pages build uses `/static-site-generator/`. Run `build.sh` **last** before committing a deployment.

## Add a new page

1. Create a Markdown file under `content/`, for example `content/blog/new-post/index.md`.
2. Give it an H1 heading (`# Page Title`); the generator uses the first H1 for the HTML page title.
3. Add the rest of the Markdown content and link to the new page from another page as needed.
4. Run `bash main.sh` to preview locally, or `bash build.sh` to prepare for deployment.

For example:

```markdown
# My New Post

A paragraph with **bold text** and a [link to Boot.dev](https://www.boot.dev/).

- First item
- Second item
```

This file is rendered to `docs/blog/new-post/index.html`. You can link to it from your home page using `[My New Post](/blog/new-post/)`.

## How it works

1. **Copy static assets:** Rebuild the output directory from the files in `static/`.
2. **Discover pages:** Traverse `content/` recursively and find `.md` files.
3. **Parse Markdown:** Convert block-level and inline Markdown into custom HTML nodes.
4. **Render pages:** Generate HTML, extract each page's title, and insert both into `template.html`.
5. **Write output:** Save corresponding `.html` files in `docs/` and adjust root-relative links and assets to the configured base path.

The parser intentionally implements a practical subset of Markdown rather than the full CommonMark specification.

## Acknowledgments

Built as a learning project through [Boot.dev](https://www.boot.dev/), focusing on recursive filesystem operations, parsing, object-oriented design, testing, and static site generation.
