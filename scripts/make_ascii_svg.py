#!/usr/bin/env python3
"""Gera o retrato ASCII animado exibido no README."""

from html import escape
from pathlib import Path

from PIL import Image, ImageEnhance

SOURCE = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")
COLS, ROWS, CELL_W, CELL_H = 92, 50, 8, 15
RAMP = " .`:-=+*cs#%@"
PAD, TITLE_H, STATUS_H = 20, 46, 46
WIDTH = COLS * CELL_W + PAD * 2
HEIGHT = TITLE_H + ROWS * CELL_H + STATUS_H + PAD


def rows() -> list[str]:
    image = Image.open(SOURCE).convert("L")
    image = ImageEnhance.Contrast(image).enhance(1.08).resize((COLS, ROWS), Image.LANCZOS)
    return [
        "".join(
            " " if pixel >= 205 else RAMP[round((1 - pixel / 255) * (len(RAMP) - 1))]
            for pixel in (image.getpixel((x, y)) for x in range(COLS))
        )
        for y in range(ROWS)
    ]


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Execute prep_photo.py antes: {SOURCE} não existe")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="url(#bg)"/><rect x=".5" y=".5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="12" fill="none" stroke="#30363d"/>',
        f'<line x2="{WIDTH}" y1="{TITLE_H}" y2="{TITLE_H}" stroke="#30363d"/>',
    ]
    for index, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        parts.append(f'<circle cx="{PAD + index * 20}" cy="23" r="8" fill="{color}"/>')
    parts.append(f'<text x="{WIDTH/2}" y="30" text-anchor="middle" fill="#7d8590" font-size="20">gabriel@github: ~$ ./portrait.sh</text>')
    for index, line in enumerate(rows()):
        y = TITLE_H + 14 + index * CELL_H
        delay = index * 0.09
        parts.append(
            f'<clipPath id="r{index}"><rect x="{PAD}" y="{y-12}" width="0" height="{CELL_H}"><animate attributeName="width" from="0" to="{COLS*CELL_W}" begin="{delay:.2f}s" dur=".09s" fill="freeze"/></rect></clipPath>'
            f'<text x="{PAD}" y="{y}" fill="#c9d1d9" font-size="13" textLength="{COLS*CELL_W}" lengthAdjust="spacing" xml:space="preserve" clip-path="url(#r{index})">{escape(line)}</text>'
        )
    parts.append(f'<line x2="{WIDTH}" y1="{HEIGHT-STATUS_H}" y2="{HEIGHT-STATUS_H}" stroke="#30363d"/>')
    parts.append(f'<text x="{PAD}" y="{HEIGHT-16}" fill="#7d8590" font-size="18">gabriel@github:~$ whoami <tspan fill="#c9d1d9">Gabriel Gomes</tspan></text>')
    parts.append("</svg>")
    OUTPUT.write_text("".join(parts), encoding="utf-8")
    print(f"[ascii] wrote {OUTPUT}")


if __name__ == "__main__":
    main()
