#!/usr/bin/env python3
"""Busca o calendário público de contribuições do GitHub e grava JSON local."""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUTPUT = Path("data/contributions.json")


def main() -> None:
    username = os.environ.get("GH_USERNAME", "gabriel-albqr")
    response = requests.get(
        f"https://github.com/users/{username}/contributions",
        headers={"User-Agent": "github-profile-art", "X-Requested-With": "XMLHttpRequest"},
        timeout=30,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    counts = {}
    for tooltip in soup.select("tool-tip[for]"):
        match = re.match(r"(\d+)\s+contribution", tooltip.get_text(strip=True))
        counts[tooltip["for"]] = int(match.group(1)) if match else 0
    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        days.append({"date": cell["data-date"], "count": counts.get(cell.get("id"), 0)})
    days.sort(key=lambda item: item["date"])
    if not days:
        raise SystemExit("Calendário de contribuições não encontrado")
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps({"user": username, "generated_at": datetime.now(timezone.utc).isoformat(), "days": days}, indent=2), encoding="utf-8")
    print(f"[contributions] {len(days)} dias para {username}")


if __name__ == "__main__":
    main()
