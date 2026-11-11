#!/usr/bin/env python3
"""Stamp each page's stylesheet link with a version taken from styles.css.

    python3 tools/stamp-css-version.py

Browsers keep a saved copy of assets/css/styles.css for a while, so after a
design change a phone can go on showing the old look. Every page links the
stylesheet as styles.css?v=<version>, where the version is the start of the
file's SHA-256. Run this after changing styles.css and commit the pages with
it: the new address makes browsers fetch the new stylesheet straight away.
Running it again without a change to styles.css changes nothing.
"""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "css" / "styles.css"
LINK = re.compile(r'href="assets/css/styles\.css(?:\?v=[0-9a-f]*)?"')


def main():
    version = hashlib.sha256(CSS.read_bytes()).hexdigest()[:10]
    target = f'href="assets/css/styles.css?v={version}"'
    for page in sorted(ROOT.glob("*.html")):
        text = page.read_bytes().decode("utf-8")
        new, count = LINK.subn(target, text)
        if count != 1:
            raise SystemExit(f"{page.name}: expected one stylesheet link, found {count}")
        if new != text:
            page.write_bytes(new.encode("utf-8"))
            print(f"updated {page.name}")
    print(f"stylesheet version {version}")


if __name__ == "__main__":
    main()
