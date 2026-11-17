"""Copy docs/wiki/*.md into a checkout of the GitHub wiki and rewrite the links.

    python3 tools/wiki_sync.py docs/wiki <wiki checkout> <owner/repo>

docs/wiki stays the only source; the wiki is a mirror. Links between pages lose
".md", images point to raw.githubusercontent.com, other repository files to their
GitHub page.
"""
import os
import re
import sys

src, dst, repo = sys.argv[1:4]
BLOB = f"https://github.com/{repo}/blob/main/"
RAW = f"https://raw.githubusercontent.com/{repo}/main/"
IMG = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp")


def target(path, image):
    """Rewrite one relative link target, as seen from docs/wiki/."""
    if re.match(r"^(https?:|mailto:|#)", path):
        return path
    page, _, anchor = path.partition("#")
    if "/" not in page and page.endswith(".md"):            # another wiki page
        return page[:-3] + (f"#{anchor}" if anchor else "")
    full = os.path.normpath(os.path.join("docs/wiki", page))
    base = RAW if image or full.lower().endswith(IMG) else BLOB
    return base + full + (f"#{anchor}" if anchor else "")


def convert(text):
    text = re.sub(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)",
                  lambda m: f"{m[1]}[{m[2]}]({target(m[3], m[1] == '!')})", text)
    return re.sub(r'(src|href)="([^"]+)"', lambda m: f'{m[1]}="{target(m[2], m[1] == "src")}"', text)


for name in os.listdir(dst):
    if name.endswith(".md"):
        os.remove(os.path.join(dst, name))
for name in sorted(os.listdir(src)):
    if name.endswith(".md"):
        with open(os.path.join(src, name), encoding="utf-8") as f:
            text = f.read()
        with open(os.path.join(dst, name), "w", encoding="utf-8") as f:
            f.write(convert(text))
