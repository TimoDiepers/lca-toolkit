"""Render the shortcut icons (recipe/shortcuts/icons/*.svg) to .icns (macOS) and .ico (Windows).

Run with `pixi run -e build icons` after editing an SVG, and commit the generated files, so
the installer build needs no drawing tools. In each SVG, the element with id="label" (the
"LCA" lettering) is left out at sizes where it would be unreadable. The macOS icon gets the
usual margin around the rounded square, so it lines up with other apps in Launchpad/Dock.
"""

import io
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import cairosvg
from PIL import Image

ICON_DIR = Path(__file__).resolve().parent.parent / "recipe" / "shortcuts" / "icons"
LABEL_MIN_PX = 48  # below this, drop the "LCA" lettering
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]
ICNS_SIZES = [16, 32, 64, 128, 256, 512, 1024]  # iconset: 16, 32, 128, 256, 512 at @1x and @2x
MAC_SCALE = 0.894  # rounded square 90 → ~80.5 % of the canvas (Apple's 824/1024 grid)


def variant(svg: str, size: int, mac: bool) -> str:
    if size < LABEL_MIN_PX:
        svg = re.sub(r'<g id="label".*?</g>', "", svg, flags=re.S)
    if mac:
        svg = re.sub(r"(<svg[^>]*>)", rf'\1<g transform="translate(50 50) scale({MAC_SCALE}) translate(-50 -50)">', svg, count=1)
        svg = svg.replace("</svg>", "</g></svg>")
    return svg


def render(svg: str, size: int) -> Image.Image:
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def write_icns(svg: str, out: Path) -> None:
    icns = {s: render(variant(svg, s, mac=True), s) for s in ICNS_SIZES}
    if not shutil.which("iconutil"):
        # Pillow's writer skips the 16/32 px @1x entries; Finder then scales down a bigger one
        icns[1024].save(out, append_images=list(icns.values())[:-1])
        return
    with tempfile.TemporaryDirectory() as tmp:
        iconset = Path(tmp) / "icon.iconset"
        iconset.mkdir()
        for base in (16, 32, 128, 256, 512):
            icns[base].save(iconset / f"icon_{base}x{base}.png")
            icns[base * 2].save(iconset / f"icon_{base}x{base}@2x.png")
        subprocess.run(["iconutil", "-c", "icns", str(iconset), "-o", str(out)], check=True)


def main() -> None:
    for src in sorted(ICON_DIR.glob("*.svg")):
        svg = src.read_text()
        ico = [render(variant(svg, s, mac=False), s) for s in ICO_SIZES]
        ico[-1].save(src.with_suffix(".ico"), sizes=[(s, s) for s in ICO_SIZES], append_images=ico[:-1])
        write_icns(svg, src.with_suffix(".icns"))
        print(f"{src.name} → {src.stem}.ico, {src.stem}.icns")


if __name__ == "__main__":
    main()
