#!/usr/bin/env python3
"""Prepara a foto de perfil para conversão ASCII, sem dependências pesadas."""

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageOps

OUTPUT = Path("source-prepped.png")


def main() -> None:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "profile-photo.jpg")
    if not source.is_file():
        raise SystemExit(f"Foto não encontrada: {source}")

    image = ImageOps.exif_transpose(Image.open(source)).convert("L")
    image = ImageOps.fit(
        image,
        (800, 800),
        method=Image.Resampling.LANCZOS,
        centering=(0.50, 0.32),
    )
    image = ImageOps.autocontrast(image, cutoff=1)

    # Mantém o rosto em evidência e reduz o ruído do cenário. Isso é
    # especialmente importante para uma imagem convertida em caracteres.
    focus = Image.new("L", image.size, 0)
    ImageDraw.Draw(focus).ellipse((70, 20, 730, 790), fill=255)
    focus = focus.filter(ImageFilter.GaussianBlur(85))
    image = Image.composite(image, Image.new("L", image.size, 255), focus)
    image.save(OUTPUT, optimize=True)
    print(f"[photo] {source} -> {OUTPUT}")


if __name__ == "__main__":
    main()
