#!/usr/bin/env python3
"""Rebuild the social preview image, assets/img/og-image.jpg (1200 x 630).

    python3 tools/make-og-image.py

The picture echoes the business card's front and the site's closing card: the
wordmark on an ivory card with the open brass frame (two corners where the
eucalyptus leaves room), on the closing card's oat ground. It is laid out as a
small web page in the site's own fonts and corner paintings, photographed with
headless Chrome (google-chrome-stable) and saved as a JPEG with Pillow.
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img" / "og-image.jpg"
CHROME = "google-chrome-stable"
SIZE = (1200, 630)

# The frame follows the business card: corners set in by 6.2% of the card's
# width (68 of 1090 px), each arm 23% of the card's width or height.
PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><style>
@font-face { font-family: "Cormorant Garamond"; src: url("ROOT/assets/fonts/cormorant-garamond-latin.woff2") format("woff2"); font-weight: 300 700; }
@font-face { font-family: "Cormorant Garamond"; src: url("ROOT/assets/fonts/cormorant-garamond-italic-latin.woff2") format("woff2"); font-weight: 300 700; font-style: italic; }
@font-face { font-family: "Source Sans 3"; src: url("ROOT/assets/fonts/source-sans-3-latin.woff2") format("woff2"); font-weight: 400 700; }
html, body { margin: 0; width: 1200px; height: 630px; overflow: hidden; }
body { display: grid; place-items: center; background: #f2ebdd; font-family: "Source Sans 3", sans-serif; }
.card { position: relative; overflow: hidden; display: grid; place-items: center; width: 1090px; height: 520px;
  background: #fffdf8; box-shadow: 0 30px 60px -45px rgba(58, 66, 53, 0.5); text-align: center; }
.card::before, .card::after { position: absolute; width: 251px; height: 120px; box-sizing: border-box;
  border: 0 solid rgba(176, 141, 87, 0.55); content: ""; }
.card::before { top: 68px; left: 68px; border-top-width: 2px; border-left-width: 2px; }
.card::after { right: 68px; bottom: 68px; border-right-width: 2px; border-bottom-width: 2px; }
.tr { position: absolute; top: 0; right: 0; width: 262px; }
.bl { position: absolute; bottom: 0; left: 0; width: 286px; }
.inner { position: relative; }
.name { color: #9a5b33; font-family: "Cormorant Garamond", serif; font-size: 100px; font-weight: 600; line-height: 1; letter-spacing: 0.01em; }
.by { margin-top: 14px; color: #52664d; font-family: "Cormorant Garamond", serif; font-size: 44px; font-weight: 500; }
.role { margin-top: 30px; color: #52664d; font-size: 22px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; }
.tag { margin-top: 22px; color: #9a5b33; font-family: "Cormorant Garamond", serif; font-size: 36px; font-style: italic; font-weight: 500; }
</style></head><body><div class="card">
<img class="tr" src="ROOT/assets/img/botanical-corner-tr.webp" alt="">
<img class="bl" src="ROOT/assets/img/botanical-corner-bl.webp" alt="">
<div class="inner">
<div class="name">Emboldened Birth</div>
<div class="by">by Tessa Millerick</div>
<div class="role">Birth doula · Lake &amp; Sonoma Counties</div>
<div class="tag">Feel heard. Feel held. Own your birth.</div>
</div></div></body></html>
"""


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        page = tmp / "og-image.html"
        page.write_text(PAGE.replace("ROOT", ROOT.as_uri()), encoding="utf-8")
        shot = tmp / "og-image.png"
        # Headless Chrome keeps part of the window's height for a toolbar it
        # never draws, so use a taller window and keep the top 630 px.
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                        "--no-default-browser-check", f"--user-data-dir={tmp / 'profile'}",
                        "--force-device-scale-factor=1", f"--window-size={SIZE[0]},{SIZE[1] + 300}",
                        "--virtual-time-budget=6000", f"--screenshot={shot}", page.as_uri()],
                       check=True, capture_output=True)
        image = Image.open(shot).convert("RGB").crop((0, 0, *SIZE))
        image.save(OUT, quality=90, optimize=True, progressive=True)
    print(OUT)


if __name__ == "__main__":
    main()
