#!/usr/bin/env python3
"""Собирает блог на двух языках: blog/ на русском и en/blog/ на английском.

Русские тексты лежат в blog_ru.py, английские в blog_en.py.
Для новой статьи добавить словарь в оба файла, собрать и дописать адреса в tools/build_sitemap.py.

    python3 tools/build_blog.py
"""
import json
from html import escape
from pathlib import Path

from blog_en import ARTICLES_EN
from blog_ru import ARTICLES

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://voidstudio.top"
TELEGRAM = "https://t.me/LuchkoOlga"
CSS_VERSION = 3
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля",
          "августа", "сентября", "октября", "ноября", "декабря"]

MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]

UI = {
    "ru": {
        "base": "", "locale": "ru_RU", "in_language": "ru-RU", "blog": "Блог",
        "logo_label": "Void Studio, визуальные работы", "nav_label": "Основная навигация",
        "nav": [("/", "Работы"), ("/projects.html", "Проекты"), ("/blog/", "Блог"), ("/studio.html#about", "О студии")],
        "switch_code": "en", "switch_text": "EN", "switch_label": "Переключить на английский",
        "contact": "Написать ↗", "service_kicker": "Услуга по теме",
        "service_text": "Расскажите о задаче, и мы предложим решение.", "telegram": "Написать в Telegram ↗",
        "more": "Ещё в блоге", "og_alt": "Логотип Void Studio . Lab",
        "footer": [("/studio.html", "О студии"), ("/projects.html", "Проекты"), ("/blog/", "Блог")],
        "index_title": "Блог Void Studio: сайты, приложения, боты и автоматизация",
        "index_description": "Статьи Void Studio о разработке сайтов, приложений, Telegram-ботов и автоматизации. Объясняем на примерах собственных проектов.",
        "index_name": "Блог Void Studio", "index_h1": "Как это устроено.",
        "index_lead": "Пишем о сайтах, приложениях, ботах и автоматизации. Объясняем на своих проектах, которые можно открыть и проверить.",
        "services": {"websites": "Сайты и интерактив", "apps": "Приложения и прототипы", "automation": "Боты и автоматизация"},
    },
    "en": {
        "base": "/en", "locale": "en_US", "in_language": "en", "blog": "Blog",
        "logo_label": "Void Studio, visual work", "nav_label": "Main navigation",
        "nav": [("/en/", "Work"), ("/en/projects.html", "Projects"), ("/en/blog/", "Blog"), ("/en/studio.html#about", "Studio")],
        "switch_code": "ru", "switch_text": "RU", "switch_label": "Switch to Russian",
        "contact": "Contact ↗", "service_kicker": "Related service",
        "service_text": "Tell us about your task and we will suggest a solution.", "telegram": "Message us on Telegram ↗",
        "more": "More from the blog", "og_alt": "Void Studio . Lab logo",
        "footer": [("/en/studio.html", "Studio"), ("/en/projects.html", "Projects"), ("/en/blog/", "Blog")],
        "index_title": "Void Studio blog: websites, apps, bots and automation",
        "index_description": "Void Studio articles on building websites, apps, Telegram bots and automation. Explained through our own projects.",
        "index_name": "Void Studio blog", "index_h1": "How it works.",
        "index_lead": "We write about websites, apps, bots and automation, and explain them through our own projects that you can open and check.",
        "services": {"websites": "Websites and interactive work", "apps": "Apps and prototypes", "automation": "Bots and automation"},
    },
}

def localized(article, lang):
    """Статья на нужном языке: русский словарь или он же с английскими полями поверх."""
    if lang == "ru":
        return article
    return {**article, **ARTICLES_EN[article["slug"]]}


def human_date(iso, lang):
    year, month, day = (int(x) for x in iso.split("-"))
    if lang == "ru":
        return f"{day} {MONTHS[month - 1]} {year} года"
    return f"{day} {MONTHS_EN[month - 1]} {year}"


def article_path(article, lang):
    return f"{UI[lang]['base']}/blog/{localized(article, lang)['slug']}.html"


def index_path(lang):
    return f"{UI[lang]['base']}/blog/"


def language_script(ru_path, en_path):
    pair = {"ru": ru_path, "en": en_path}
    routes = {ru_path: pair, en_path: pair}
    table = json.dumps(routes, separators=(",", ":"))
    return (
        "<script>(()=>{const current=document.documentElement.lang==='ru'?'ru':'en';let saved='';"
        "try{saved=localStorage.getItem('voidstudio-language')||''}catch{}"
        "const browser=(navigator.languages?.[0]||navigator.language||'en').toLowerCase();"
        "const wanted=saved||(browser.startsWith('ru')?'ru':'en');"
        f"const routes={table};"
        "const target=routes[location.pathname]?.[wanted];"
        "if(target&&wanted!==current){location.replace(target+location.search+location.hash);return}"
        "addEventListener('DOMContentLoaded',()=>document.querySelectorAll('.nav-language[hreflang]')"
        ".forEach(link=>link.addEventListener('click',()=>{try{localStorage.setItem('voidstudio-language',link.hreflang)}catch{}})))})();</script>"
    )


def head(lang, title, description, paths, og_type, ld):
    e, ui, other = escape, UI[lang], UI[lang]["switch_code"]
    url = SITE + paths[lang]
    nav = "".join(f'<a href="{href}">{label}</a>' for href, label in ui["nav"])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{language_script(paths['ru'], paths['en'])}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-E9G3NGMQ6F"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-E9G3NGMQ6F');</script>
<meta name="theme-color" content="#f4f4f0">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ru" href="{SITE + paths['ru']}">
<link rel="alternate" hreflang="en" href="{SITE + paths['en']}">
<link rel="alternate" hreflang="x-default" href="{SITE + paths['ru']}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{ui['locale']}">
<meta property="og:site_name" content="Void Studio">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ui['og_alt']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon-64.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/site.css?v=9">
<link rel="stylesheet" href="/assets/blog.css?v={CSS_VERSION}">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script>
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body><header class="site-header"><a class="site-logo" href="{ui['nav'][0][0]}" aria-label="{ui['logo_label']}"></a><nav aria-label="{ui['nav_label']}">{nav}<a class="nav-language" href="{paths[other]}" lang="{other}" hreflang="{other}" aria-label="{ui['switch_label']}">{ui['switch_text']}</a><a class="nav-contact" href="{TELEGRAM}" target="_blank" rel="noopener">{ui['contact']}</a></nav></header>
"""


def foot(lang):
    links = "".join(f'<a href="{href}">{label}</a>' for href, label in UI[lang]["footer"])
    return f"""<footer><span>© 2026 Void Studio . Lab</span><div>{links}<a href="https://github.com/Mihailchik" target="_blank" rel="noopener">GitHub ↗</a></div></footer>
<script src="/assets/track.js" defer></script>
<script>window.shareConfig={{position:"bottom-right"}};</script>
<script src="/assets/share.js" defer></script>
</body></html>
"""


def render_article(source, lang):
    e, ui = escape, UI[lang]
    article = localized(source, lang)
    paths = {code: article_path(source, code) for code in ("ru", "en")}
    url = SITE + paths[lang]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting", "@id": url + "#article", "url": url,
                "mainEntityOfPage": url, "headline": article["title"],
                "description": article["description"], "inLanguage": ui["in_language"],
                "datePublished": article["date"], "dateModified": article["date"],
                "image": SITE + "/assets/img/og.png",
                "author": {"@id": SITE + "/#organization"},
                "publisher": {"@id": SITE + "/#organization"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Void Studio", "item": SITE + ui["nav"][0][0]},
                    {"@type": "ListItem", "position": 2, "name": ui["blog"], "item": SITE + index_path(lang)},
                    {"@type": "ListItem", "position": 3, "name": article["short"], "item": url},
                ],
            },
        ],
    }
    service = article["service"]
    others = "".join(
        f'<a class="post-link" href="{article_path(a, lang)}"><span>{e(localized(a, lang)["short"])}</span><span aria-hidden="true">→</span></a>'
        for a in ARTICLES if a["slug"] != source["slug"]
    )
    return (
        head(lang, f"{article.get('seo_title', article['title'])} | Void Studio", article["description"], paths, "article", ld)
        + f"""<main>
<article class="post">
<header class="post-head"><p class="kicker"><a href="{index_path(lang)}">{ui['blog']}</a> · <time datetime="{article['date']}">{human_date(article['date'], lang)}</time></p><h1>{e(article['title'])}</h1><p class="post-lead">{e(article['lead'])}</p></header>
<div class="post-body">{article['body']}</div>
<aside class="post-service"><p class="kicker">{ui['service_kicker']}</p><a href="{ui['base']}/{service}.html">{ui['services'][service]} →</a><p>{ui['service_text']}</p><a class="button primary" href="{TELEGRAM}" target="_blank" rel="noopener">{ui['telegram']}</a></aside>
</article>
<section class="post-more"><p class="kicker">{ui['more']}</p><div>{others}</div></section>
</main>
"""
        + foot(lang)
    )


def render_index(lang):
    e, ui = escape, UI[lang]
    paths = {code: index_path(code) for code in ("ru", "en")}
    url = SITE + paths[lang]
    items = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)
    ld = {
        "@context": "https://schema.org", "@type": "Blog", "@id": url + "#blog", "url": url,
        "name": ui["index_name"], "description": ui["index_description"], "inLanguage": ui["in_language"],
        "publisher": {"@id": SITE + "/#organization"},
        "blogPost": [
            {"@type": "BlogPosting", "headline": localized(a, lang)["title"], "url": SITE + article_path(a, lang), "datePublished": a["date"]}
            for a in items
        ],
    }
    rows = "".join(
        f'<article class="post-row"><time datetime="{a["date"]}">{human_date(a["date"], lang)}</time>'
        f'<h2><a href="{article_path(a, lang)}">{e(localized(a, lang)["short"])}</a></h2><p>{e(localized(a, lang)["description"])}</p></article>'
        for a in items
    )
    return (
        head(lang, ui["index_title"], ui["index_description"], paths, "website", ld)
        + f"""<main>
<section class="blog-hero"><p class="kicker">{ui['blog']}</p><h1>{ui['index_h1']}</h1><p>{ui['index_lead']}</p></section>
<section class="post-list">{rows}</section>
</main>
"""
        + foot(lang)
    )


def write(path, html):
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print(target.relative_to(ROOT))


def main():
    for lang in ("ru", "en"):
        write(index_path(lang), render_index(lang))
        for article in ARTICLES:
            write(article_path(article, lang), render_article(article, lang))


if __name__ == "__main__":
    main()
