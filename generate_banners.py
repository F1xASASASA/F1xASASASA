"""
Генератор анимированных SVG-баннеров для GitHub-профиля.
Запускается через GitHub Action (см. .github/workflows/banners.yml).

Чтобы поменять текст/цвета — правь константы ниже и запусти Action заново
(вручную через Actions -> Generate Profile Banners -> Run workflow,
или просто запушь изменение в этот файл).
"""

import os

OUTPUT_DIR = "assets"

NAME_LINE = "Привет, я Арсений! 👋"
SUBTITLE_LINE = "18 лет · Веб-разработчик · Учусь и пишу код"
# NAME_LINE/SUBTITLE_LINE больше не используются в SVG (текст теперь идёт
# обычным markdown-заголовком в README), но оставлены здесь на случай,
# если решишь вернуть их в баннер.

COLOR_BG_FROM = "#1a1a2e"
COLOR_BG_TO = "#16213e"
COLOR_ACCENT_1 = "#58A6FF"
COLOR_ACCENT_2 = "#8957e5"

HEADER_SVG = f"""<svg width="900" height="160" viewBox="0 0 900 160" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{COLOR_BG_FROM}"/>
      <stop offset="100%" stop-color="{COLOR_BG_TO}"/>
    </linearGradient>
    <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{COLOR_ACCENT_1}">
        <animate attributeName="stop-color" values="{COLOR_ACCENT_1};{COLOR_ACCENT_2};{COLOR_ACCENT_1}" dur="6s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="{COLOR_ACCENT_2}">
        <animate attributeName="stop-color" values="{COLOR_ACCENT_2};{COLOR_ACCENT_1};{COLOR_ACCENT_2}" dur="6s" repeatCount="indefinite" />
      </stop>
    </linearGradient>
  </defs>

  <rect width="900" height="160" fill="url(#bgGrad)"/>

  <g transform="translate(0,160) scale(1,-1)">
    <path d="M-100,110 C50,150 200,70 350,110 C500,150 650,70 800,110 C950,150 1000,110 1000,110 L1000,180 L-100,180 Z" fill="url(#waveGrad)" opacity="0.35">
      <animateTransform attributeName="transform" type="translate" values="0,0; -60,0; 0,0" dur="7s" repeatCount="indefinite" />
    </path>
    <path d="M-100,130 C50,100 200,160 350,130 C500,100 650,160 800,130 C950,100 1000,130 1000,130 L1000,180 L-100,180 Z" fill="url(#waveGrad)" opacity="0.55">
      <animateTransform attributeName="transform" type="translate" values="0,0; 40,0; 0,0" dur="5s" repeatCount="indefinite" />
    </path>
  </g>
</svg>
"""

FOOTER_SVG = f"""<svg width="900" height="100" viewBox="0 0 900 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradF" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{COLOR_BG_FROM}">
        <animate attributeName="stop-color" values="{COLOR_BG_FROM};{COLOR_ACCENT_2};{COLOR_BG_FROM}" dur="8s" repeatCount="indefinite" />
      </stop>
      <stop offset="100%" stop-color="{COLOR_ACCENT_1}">
        <animate attributeName="stop-color" values="{COLOR_ACCENT_1};{COLOR_BG_FROM};{COLOR_ACCENT_1}" dur="8s" repeatCount="indefinite" />
      </stop>
    </linearGradient>
  </defs>
  <path d="M-100,60 C50,20 200,90 350,60 C500,30 650,90 800,60 C950,30 1000,60 1000,60 L1000,100 L-100,100 Z" fill="url(#bgGradF)">
    <animateTransform attributeName="transform" type="translate" values="0,0; -50,0; 0,0" dur="6s" repeatCount="indefinite" />
  </path>
</svg>
"""

DIVIDER_SVG = f"""<svg width="900" height="30" viewBox="0 0 900 30" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="divGrad" gradientUnits="userSpaceOnUse" x1="-300" y1="0" x2="0" y2="0">
      <stop offset="0%" stop-color="{COLOR_BG_FROM}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{COLOR_ACCENT_1}"/>
      <stop offset="100%" stop-color="{COLOR_BG_FROM}" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0,0; 1200,0" dur="3s" repeatCount="indefinite" />
    </linearGradient>
  </defs>
  <rect x="0" y="13" width="900" height="4" rx="2" fill="#30363d"/>
  <rect x="0" y="13" width="900" height="4" rx="2" fill="url(#divGrad)"/>
</svg>
"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = {
        "header.svg": HEADER_SVG,
        "footer.svg": FOOTER_SVG,
        "divider.svg": DIVIDER_SVG,
    }
    for name, content in files.items():
        path = os.path.join(OUTPUT_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Сгенерирован {path}")


if __name__ == "__main__":
    main()
