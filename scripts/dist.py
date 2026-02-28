import json
import os
import shutil
import markdown

if os.path.exists("./dist/"):
    shutil.rmtree("./dist/")
os.mkdir("dist")

# TODO preprocessor that transforms wikilinks to html paths
# should intelligently handle internal links (within vault) and external ones

# TODO convert obsidian metadata to json and add it to the template.

# TODO nav somehow, maybe something akin to what obsidian publish itself does.

def md_to_html(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    html = markdown.markdown(
        text,
        extensions=[
            "extra",
            "toc",
            "codehilite",
            "mdx_wikilink_plus",
            "pymdownx.arithmatex"
        ]
    )

    return html

DEFAULT_METADATA: dict[str, str] = {
    "title": "Lorem Ipsum",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
}

def apply_template(content: str, metadata: dict[str, str] = DEFAULT_METADATA) -> str:
    title = metadata.get("title", DEFAULT_METADATA["title"])
    description = metadata.get("description", DEFAULT_METADATA["description"])
    return f"""<!--META_START
{json.dumps(metadata)}
META_END-->

<!DOCTYPE html>
<html lang="en">
    <head>
        <!--metadata-->
        <meta charset="utf-8">
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="{description}">

        <!--inline start
            css:theme
            css:default
        inline end-->
        <!--autogen start-->
        <!--autogen end-->
    </head>
    <body>
        <main class="container">
{content}
        </main>
    </body>
</html>
"""

def process_md_file(root: str, file: str):
    path: str = os.path.join(root, file)
    dist_path: str = os.path.join(
        "dist/",
        path.removeprefix("vault/").removesuffix(".md") + ".html"
    )
    dist_dir: str = os.path.dirname(dist_path)

    html: str = md_to_html(path)
    print(f"{path} -> {dist_path}")
    os.makedirs(dist_dir, exist_ok=True)
    with open(dist_path, "w") as f:
        _ = f.write(apply_template(content=html))

def copy_html_directly(root: str, file: str):
    path: str = os.path.join(root, file)
    dist_path: str = os.path.join(
        "dist/",
        path.removeprefix("vault/")
    )
    dist_dir: str = os.path.dirname(dist_path)
    print(f"{path} -> {dist_path}")
    os.makedirs(dist_dir, exist_ok=True)
    _ = shutil.copy(path, dist_path)

if __name__ == "__main__":
    for root, _, files in os.walk("vault/", topdown=True):
        if ".obsidian" in root:
            continue

        for file in files:
            if file.endswith(".html"):
                copy_html_directly(root, file)
            if not file.endswith(".md"):
                continue
            process_md_file(root, file)

