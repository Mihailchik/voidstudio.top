#!/usr/bin/env python3
"""Собирает sitemap.xml из списка страниц. Новая страница — новая строка в PAGES.

Каждая строка: русский адрес, английский адрес. Пара связывается через hreflang.

    python3 tools/build_sitemap.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://voidstudio.top"

PAGES = [
    ("/", "/en/"),
    ("/studio.html", "/en/studio.html"),
    ("/projects.html", "/en/projects.html"),
    ("/websites.html", "/en/websites.html"),
    ("/apps.html", "/en/apps.html"),
    ("/automation.html", "/en/automation.html"),
    ("/ai-visuals.html", "/en/ai-visuals.html"),
    ("/projects/surf.html", "/en/projects/surf.html"),
    ("/projects/inkfall.html", "/en/projects/inkfall.html"),
    ("/projects/glazomer.html", "/en/projects/glazomer.html"),
    ("/projects/argyns.html", "/en/projects/argyns.html"),
    ("/projects/fittimer.html", "/en/projects/fittimer.html"),
    ("/projects/poster.html", "/en/projects/poster.html"),
    ("/projects/podcast.html", "/en/projects/podcast.html"),
    ("/blog/", "/en/blog/"),
    ("/blog/avtoposting-v-socseti.html", "/en/blog/scheduled-social-posting.html"),
    ("/blog/telegram-bot-dlya-biznesa.html", "/en/blog/telegram-bot-for-business.html"),
    ("/blog/mvp-prilozheniya.html", "/en/blog/app-mvp.html"),
    ("/blog/interaktivnyj-sajt.html", "/en/blog/interactive-website.html"),
]


def main():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for ru, en in PAGES:
        for loc in (ru, en):
            assert (ROOT / (loc.lstrip("/") + ("index.html" if loc.endswith("/") else ""))).exists(), loc
            out += ["  <url>", f"    <loc>{SITE}{loc}</loc>",
                    f'    <xhtml:link rel="alternate" hreflang="ru" href="{SITE}{ru}" />',
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}" />',
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{ru}" />',
                    "  </url>"]
    out.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"sitemap.xml: {len(PAGES) * 2} адресов")


if __name__ == "__main__":
    main()
