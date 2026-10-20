#!/usr/bin/env python3
"""Gera um cartão profissional no estilo fastfetch para o README."""

from html import escape
from pathlib import Path

OUTPUT = Path("info-card.svg")
WIDTH, HEIGHT = 650, 560
ROWS = [
    ("head", "gabriel@github", ""),
    ("sep", "", ""),
    ("kv", "Função", "Desenvolvedor Full Stack"),
    ("kv", "Empresa", "Usina Petribu S/A"),
    ("kv", "Formação", "Sistemas de Informação · Estácio (6º período)"),
    ("kv", "Local", "Pernambuco, Brasil"),
    ("sec", "Stack", ""),
    ("kv", "Web", "React, TypeScript, JavaScript"),
    ("kv", "Mobile", "Flutter, Dart"),
    ("kv", "Backend", "Python, Django, Django REST"),
    ("kv", "Dados", "PostgreSQL, MySQL, Oracle, Redis"),
    ("kv", "Infra", "Docker, Compose, Nginx"),
    ("sec", "Foco atual", ""),
    ("bullet", "Flutter mobile com arquitetura offline-first", ""),
    ("bullet", "React + TypeScript, PWA e responsividade", ""),
    ("bullet", "Django robusto, APIs REST e testes unitários", ""),
]


def main() -> None:
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="13">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#111722"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="url(#bg)"/><rect x=".5" y=".5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="12" fill="none" stroke="#30363d"/>',
        f'<line x2="{WIDTH}" y1="30" y2="30" stroke="#30363d"/>',
        '<circle cx="20" cy="15" r="5" fill="#ff5f56"/><circle cx="36" cy="15" r="5" fill="#ffbd2e"/><circle cx="52" cy="15" r="5" fill="#27c93f"/>',
        f'<text x="{WIDTH/2}" y="19" text-anchor="middle" fill="#7d8590" font-size="12">gabriel@github: ~$ fastfetch</text>',
    ]
    y, step, delay = 58, 25, 0.12
    for index, (kind, key, value) in enumerate(ROWS):
        animation = f'<animate attributeName="opacity" from="0" to="1" begin="{index*delay:.2f}s" dur=".3s" fill="freeze"/>'
        if kind == "sep":
            svg.append(f'<text x="26" y="{y}" fill="#8b949e" opacity="0">----------------{animation}</text>')
        elif kind == "head":
            svg.append(f'<text x="26" y="{y}" fill="#58a6ff" font-weight="bold" opacity="0">{escape(key)}{animation}</text>')
        elif kind == "sec":
            y += 8
            svg.append(f'<text x="26" y="{y}" fill="#58a6ff" font-weight="bold" opacity="0">~ {escape(key)}{animation}</text>')
        elif kind == "bullet":
            svg.append(f'<text x="26" y="{y}" fill="#39d353" opacity="0">•{animation}</text><text x="42" y="{y}" fill="#c9d1d9" opacity="0">{escape(key)}{animation}</text>')
        else:
            svg.append(f'<text x="26" y="{y}" fill="#39d353" font-weight="bold" opacity="0">{escape(key)}{animation}</text><text x="126" y="{y}" fill="#c9d1d9" opacity="0">{escape(value)}{animation}</text>')
        y += step
    svg.append(f'<line x2="{WIDTH}" y1="{HEIGHT-30}" y2="{HEIGHT-30}" stroke="#30363d"/>')
    svg.append(f'<text x="20" y="{HEIGHT-11}" fill="#7d8590" font-size="13">gabriel@github:~$ <tspan fill="#c9d1d9">fastfetch</tspan></text></svg>')
    OUTPUT.write_text("".join(svg), encoding="utf-8")
    print(f"[card] wrote {OUTPUT}")


if __name__ == "__main__":
    main()
