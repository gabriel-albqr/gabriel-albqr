#!/usr/bin/env python3
"""Converte o JSON de contribuições em um heatmap SVG animado para o README."""

import json
from datetime import date
from pathlib import Path

SOURCE = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
MONTHS = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
CELL, GAP, PAD, TITLE = 12, 3, 22, 30


def level(count: int) -> int:
    if count == 0:
        return 0
    if count <= 5:
        return 1
    if count <= 15:
        return 2
    if count <= 30:
        return 3
    if count <= 50:
        return 4
    return 5


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    days = data["days"]
    by_date = {item["date"]: item["count"] for item in days}
    start, end = date.fromisoformat(days[0]["date"]), date.fromisoformat(days[-1]["date"])
    start = start.fromordinal(start.toordinal() - ((start.weekday() + 1) % 7))
    weeks = (end.toordinal() - start.toordinal()) // 7 + 1
    step, grid_left, grid_top = CELL + GAP, PAD + 30, TITLE + 22
    width, height = grid_left + weeks * step + PAD, grid_top + 7 * step + 106
    total = sum(by_date.values())
    longest = run = current = 0
    for item in days:
        run = run + 1 if item["count"] else 0
        longest = max(longest, run)
    for item in reversed(days):
        if not item["count"]:
            break
        current += 1
    best = max(days, key=lambda item: item["count"])
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#0d1420"/><stop offset="1" stop-color="#0a0e14"/></linearGradient></defs>',
        f'<rect width="{width}" height="{height}" rx="12" fill="url(#bg)"/><rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="none" stroke="#1f6feb" stroke-opacity=".55"/>',
        f'<line x2="{width}" y1="{TITLE}" y2="{TITLE}" stroke="#1f6feb" stroke-opacity=".35"/>',
        '<circle cx="22" cy="15" r="5" fill="#ff5f56"/><circle cx="38" cy="15" r="5" fill="#ffbd2e"/><circle cx="54" cy="15" r="5" fill="#27c93f"/>',
        f'<text x="{width/2}" y="19" text-anchor="middle" fill="#7d8590" font-size="12">gabriel@github: ~/contributions --graph</text>',
    ]
    seen = set()
    for week in range(weeks):
        week_start = start.fromordinal(start.toordinal() + week * 7)
        if week_start.month not in seen:
            seen.add(week_start.month)
            svg.append(f'<text x="{grid_left + week*step}" y="44" fill="#7d8590" font-size="10">{MONTHS[week_start.month-1]}</text>')
    for row, label in ((1, "Seg"), (3, "Qua"), (5, "Sex")):
        svg.append(f'<text x="{PAD}" y="{grid_top + row*step + 10}" fill="#7d8590" font-size="9">{label}</text>')
    for week in range(weeks):
        for weekday in range(7):
            day = start.fromordinal(start.toordinal() + week * 7 + weekday)
            count = by_date.get(day.isoformat())
            if count is None:
                continue
            x, y = grid_left + week * step, grid_top + weekday * step
            delay = week * 0.018 + weekday * 0.045
            word = "contribuição" if count == 1 else "contribuições"
            svg.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[level(count)]}" opacity="0"><title>{day}: {count} {word}</title><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur=".12s" fill="freeze"/></rect>')
    legend_y = grid_top + 7 * step + 8
    svg.append(f'<text x="{width-160}" y="{legend_y+10}" fill="#7d8590" font-size="10">Menos</text>')
    for index, color in enumerate(PALETTE):
        svg.append(f'<rect x="{width-120+index*12}" y="{legend_y}" width="10" height="10" rx="2" fill="{color}"/>')
    svg.append(f'<text x="{width-32}" y="{legend_y+10}" fill="#7d8590" font-size="10">Mais</text>')
    stats_y = legend_y + 38
    svg.append(f'<line x2="{width}" y1="{stats_y-14}" y2="{stats_y-14}" stroke="#1f6feb" stroke-opacity=".25"/>')
    svg.append(f'<text x="{PAD}" y="{stats_y}" fill="#39d353" font-size="13"><tspan font-weight="700">{total:,}</tspan><tspan fill="#7d8590"> contribuições no último ano</tspan></text>')
    svg.append(f'<text x="{PAD}" y="{stats_y+24}" fill="#7d8590" font-size="12">streak atual <tspan fill="#58a6ff">{current} dias</tspan> · recorde <tspan fill="#58a6ff">{longest} dias</tspan> · melhor dia <tspan fill="#f2cc60">{best["count"]}</tspan></text>')
    svg.append("</svg>")
    OUTPUT.write_text("".join(svg), encoding="utf-8")
    print(f"[heatmap] wrote {OUTPUT}")


if __name__ == "__main__":
    main()
