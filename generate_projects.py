"""
Генератор карточек проектов для GitHub-профиля.
Тянет актуальные данные (звёзды, форки, язык, описание) через GitHub API
и рисует SVG-плитки. Запускается через .github/workflows/projects.yml.

Чтобы добавить/убрать проект — просто отредактируй список REPOS ниже.
"""

import json
import os
import textwrap
import urllib.request

USERNAME = "F1xASASASA"

# Список репозиториев для показа (в этом порядке и будут карточки)
REPOS = [
    {"name": "visitka", "emoji": "🌐", "title": "Персональная визитка"},
    {"name": "wb_minecraft", "emoji": "⚔️", "title": "WoolBrawl — Paper-плагин, battlebox-режим"},
    {"name": "cps_limiter", "emoji": "⚡", "title": "Инструмент для работы с кликами"},
    {"name": "typingPro", "emoji": "⌨️", "title": "VK мини-приложение (React + TS)"},
    {"name": "Hg_minecraft", "emoji": "🏹", "title": "HungerGames — Paper-плагин с бордером"},
]

LANG_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Java": "#b07219",
    "C#": "#178600",
    None: "#8b949e",
}

CARD_W = 280
CARD_H = 140
GAP = 20
MAX_COLS = 3

# Сколько символов помещается в одну строку описания при текущей ширине карточки
DESC_CHARS_PER_LINE = 32

COLOR_BG = "#161b22"
COLOR_BORDER = "#30363d"
COLOR_ACCENT = "#58A6FF"
COLOR_TEXT = "#c9d1d9"
COLOR_MUTED = "#8b949e"


def fetch_repo_data(name):
    """Тянет описание/звёзды/форки/язык репозитория через GitHub API."""
    url = f"https://api.github.com/repos/{USERNAME}/{name}"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USERNAME}-profile-readme",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
        return {
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "language": data.get("language"),
        }
    except Exception as e:
        print(f"Не удалось получить данные для {name}: {e}")
        return {"stars": 0, "forks": 0, "language": None}


def wrap_description(text, width=DESC_CHARS_PER_LINE, max_lines=2):
    """Переносит описание максимум на max_lines строк, обрезая с многоточием, если не влезло."""
    lines = textwrap.wrap(text, width=width)
    if len(lines) <= max_lines:
        return lines
    trimmed = lines[:max_lines]
    last = trimmed[-1]
    if len(last) > width - 1:
        last = last[: width - 1].rstrip()
    trimmed[-1] = last + "…"
    return trimmed


def escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def make_card(x, y, index, repo, info):
    lang = info["language"]
    lang_color = LANG_COLORS.get(lang, LANG_COLORS[None])
    delay = 0.15 * index

    desc_lines = wrap_description(repo["title"])
    desc_svg = ""
    for i, line in enumerate(desc_lines):
        desc_svg += f'\n    <text x="{x + 18}" y="{y + 54 + i * 16}" font-family="Verdana, sans-serif" font-size="12" fill="{COLOR_TEXT}">{escape(line)}</text>'

    lang_line = ""
    if lang:
        lang_line = f"""
    <circle cx="{x + 18}" cy="{y + 112}" r="5" fill="{lang_color}" />
    <text x="{x + 30}" y="{y + 116}" font-family="Verdana, sans-serif" font-size="12" fill="{COLOR_MUTED}">{escape(lang)}</text>
"""

    return f"""
  <g opacity="0">
    <animate attributeName="opacity" values="0;1" dur="0.6s" begin="{delay}s" fill="freeze" />

    <rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="10" fill="{COLOR_BG}" stroke="{COLOR_BORDER}" stroke-width="1" />
    <rect x="{x}" y="{y}" width="{CARD_W}" height="3" rx="1.5" fill="{lang_color}" opacity="0.8" />

    <text x="{x + 18}" y="{y + 34}" font-family="Verdana, sans-serif" font-size="16" font-weight="bold" fill="{COLOR_ACCENT}">{repo['emoji']} {escape(repo['name'])}</text>
{desc_svg}
{lang_line}
    <text x="{x + CARD_W - 18}" y="{y + 116}" font-family="Verdana, sans-serif" font-size="12" fill="{COLOR_MUTED}" text-anchor="end">⭐ {info['stars']}  🍴 {info['forks']}</text>
  </g>
"""


def main():
    cols = min(MAX_COLS, len(REPOS))
    rows = (len(REPOS) + cols - 1) // cols
    width = cols * CARD_W + (cols - 1) * GAP
    height = rows * CARD_H + (rows - 1) * GAP

    cards = []
    for i, repo in enumerate(REPOS):
        col = i % cols
        row = i // cols
        x = col * (CARD_W + GAP)
        y = row * (CARD_H + GAP)
        info = fetch_repo_data(repo["name"])
        cards.append(make_card(x, y, i, repo, info))

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
{''.join(cards)}
</svg>
"""

    os.makedirs("assets", exist_ok=True)
    path = "assets/projects.svg"
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Сгенерирован {path}")


if __name__ == "__main__":
    main()
