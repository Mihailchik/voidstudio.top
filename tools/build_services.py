#!/usr/bin/env python3
"""Собирает страницы услуг: четыре на русском в корне и четыре на английском в en/.

Тексты лежат здесь же, в SERVICES. Править их нужно в этом файле, а потом
запускать сборку заново, иначе русская и английская версии разойдутся.

    python3 tools/build_services.py
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://voidstudio.top"
TELEGRAM = "https://t.me/LuchkoOlga"
CSS_VERSION = 2

UI = {
    "ru": {
        "html_lang": "ru", "locale": "ru_RU", "in_language": "ru-RU", "prefix": "",
        "logo_label": "Void Studio — визуальные работы", "nav_label": "Основная навигация",
        "nav": [("/", "Работы"), ("projects.html", "Проекты"), ("studio.html#about", "О студии")],
        "switch_code": "en", "switch_text": "EN", "switch_label": "Переключить на английский",
        "contact": "Написать ↗", "kicker": "Услуги", "includes": "Что входит",
        "process_kicker": "Как идёт работа", "examples_kicker": "Примеры",
        "stack_kicker": "На чём делаем", "other_kicker": "Другие услуги",
        "other_title": "Что ещё делаем.", "cta_kicker": "Обсудить проект",
        "cta_title": "Есть идея или задача?", "cta_link": "Написать в Telegram ↗",
        "discuss": "Обсудить задачу", "all_projects": "Все проекты ↗",
        "footer": [("studio.html", "О студии"), ("projects.html", "Проекты"), ("/", "Работы")],
        "og_alt": "Логотип Void Studio . Lab", "home": "Void Studio", "home_url": "/",
        "process_title": "От разговора до запуска.",
        "process": [
            ("Разбираемся в задаче", "Вы рассказываете, что нужно и для кого. Мы задаём вопросы и предлагаем решение."),
            ("Показываем рабочую версию", "Не картинку, а то, что можно открыть и попробовать. На ней видно, что стоит поменять."),
            ("Доводим и проверяем", "Дописываем, проверяем на телефонах и компьютерах, правим по вашим замечаниям."),
            ("Запускаем", "Выкладываем результат и остаёмся на связи после запуска."),
        ],
    },
    "en": {
        "html_lang": "en", "locale": "en_US", "in_language": "en", "prefix": "en/",
        "logo_label": "Void Studio — visual work", "nav_label": "Main navigation",
        "nav": [("./", "Work"), ("projects.html", "Projects"), ("studio.html#about", "Studio")],
        "switch_code": "ru", "switch_text": "RU", "switch_label": "Switch to Russian",
        "contact": "Contact ↗", "kicker": "Services", "includes": "What is included",
        "process_kicker": "How we work", "examples_kicker": "Examples",
        "stack_kicker": "What we build with", "other_kicker": "Other services",
        "other_title": "What else we do.", "cta_kicker": "Discuss a project",
        "cta_title": "Have an idea or a task?", "cta_link": "Message us on Telegram ↗",
        "discuss": "Discuss a task", "all_projects": "All projects ↗",
        "footer": [("studio.html", "Studio"), ("projects.html", "Projects"), ("./", "Work")],
        "og_alt": "Void Studio . Lab logo", "home": "Void Studio", "home_url": "/en/",
        "process_title": "From the first talk to launch.",
        "process": [
            ("We learn the task", "You tell us what you need and who it is for. We ask questions and suggest a solution."),
            ("We show a working version", "Not a picture but something you can open and try. It shows what is worth changing."),
            ("We finish and test", "We complete the work, test it on phones and computers, and fix what you point out."),
            ("We launch", "We publish the result and stay in touch after launch."),
        ],
    },
}

# Примеры ссылаются на карточки в projects.html и на сами проекты.
PROJECTS = {
    "surf": {"url": "https://surf.voidstudio.top", "ru": ("Surf", "Веб-сервис", "Волна, ветер, прилив и камеры пляжей Пхукета в одном интерфейсе. Данные нескольких моделей сводятся в одну понятную оценку."), "en": ("Surf", "Web service", "Waves, wind, tide and beach cameras for Phuket in one interface. Several forecast models are combined into one clear score.")},
    "inkfall": {"url": "https://inkfall.voidstudio.top", "ru": ("Inkfall", "Интерактивная графика", "Чернила в воде, которыми управляют мышью, пальцем, жестами перед камерой или голосом. Физика жидкости считается на видеокарте."), "en": ("Inkfall", "Interactive graphic", "Ink in water driven by mouse, touch, hand gestures or voice. The fluid physics runs on the GPU.")},
    "glazomer": {"url": "https://glazomer.voidstudio.top", "ru": ("Глазомер", "Браузерная игра", "Пять заданий на глаз, одна попытка в день. Работает без регистрации и без сервера."), "en": ("Eyeball", "Browser game", "Five tasks done by eye, one attempt a day. No sign-up and no server.")},
    "argyns": {"url": "https://argyns.kz", "ru": ("Argyns", "iOS и Android", "Цифровой реестр двенадцати родов Аргын: общая база, статистика, уведомления о съездах. Опубликовано в App Store и Google Play."), "en": ("Argyns", "iOS and Android", "A digital registry for the twelve Argyn clans: a shared database, statistics and gathering announcements. Available on the App Store and Google Play.")},
    "fittimer": {"url": "https://apps.apple.com/ru/app/fittimer999/id6755115543", "ru": ("FitTimer", "Мобильное приложение", "Таймер интервальных тренировок с шаблонами Tabata, EMOM, AMRAP и HIIT. Без регистрации, рекламы и сбора данных."), "en": ("FitTimer", "Mobile app", "An interval training timer with Tabata, EMOM, AMRAP and HIIT templates. No sign-up, no ads, no data collection.")},
    "poster": {"url": "", "ru": ("Poster 2.0", "Автоматизация", "Система готовит один выпуск для Telegram, Instagram, YouTube и Pikabu, проверяет файлы и планирует публикации. На ней работает контент студии."), "en": ("Poster 2.0", "Automation", "A system that prepares one release for Telegram, Instagram, YouTube and Pikabu, validates files and schedules publications. It runs the studio's own content.")},
    "podcast": {"url": "https://github.com/Mihailchik/podcastQ", "ru": ("Podcast Bot", "Telegram-бот", "Бот следит за RSS, YouTube и Telegram, скачивает новые выпуски, приводит звук к MP3 и отправляет в один канал."), "en": ("Podcast Bot", "Telegram bot", "The bot watches RSS, YouTube and Telegram, downloads new episodes, converts audio to MP3 and sends them to one channel.")},
}

GALLERY = [
    ("assets/gallery/heat-of-oven.webp", 1080, 1350, "Жар печи", "Heat of the Oven"),
    ("assets/gallery/hot-sandwich.webp", 810, 1440, "Горячий тост", "Hot Toast"),
    ("assets/gallery/light-and-shadow.webp", 1080, 1350, "Свет и тени", "Light and Shadow"),
    ("assets/hero-snow-leopard.webp", 1100, 1100, "Снежный барс", "Snow Leopard"),
]

SERVICES = [
    {
        "slug": "websites",
        "examples": ["surf", "inkfall", "glazomer"],
        "stack": "Vanilla JS · WebGL2 · GLSL · SVG · Vercel · GitHub Pages",
        "ru": {
            "name": "Сайты и интерактив", "service_type": "Разработка сайтов",
            "title": "Разработка сайтов и интерактивных проектов — Void Studio",
            "description": "Void Studio делает лендинги, портфолио, веб-сервисы, браузерные игры и интерактивную графику на WebGL. От идеи до рабочего сайта.",
            "h1": "Разработка сайтов и интерактивных проектов.",
            "lead": "Лендинг, портфолио, веб-сервис или страница с необычной механикой. Проектируем, программируем и запускаем.",
            "items": [
                ("Лендинг или портфолио", "Быстрая страница, которая понятно объясняет, что вы делаете, и хорошо выглядит на телефоне."),
                ("Веб-сервис", "Страница, которая собирает данные и даёт человеку готовый ответ. Так устроен наш прогноз для серфинга Surf."),
                ("Интерактивная графика", "Графика в браузере, которая отвечает на мышь, касание, жесты и звук. Пример — Inkfall."),
                ("Браузерная игра", "Небольшая игра, которая открывается по ссылке без установки и регистрации. Пример — «Глазомер»."),
            ],
            "examples_title": "Сайты, которые можно открыть прямо сейчас.",
        },
        "en": {
            "name": "Websites and interactive work", "service_type": "Website development",
            "title": "Website and interactive development — Void Studio",
            "description": "Void Studio builds landing pages, portfolios, web services, browser games and interactive WebGL graphics. From an idea to a working site.",
            "h1": "Websites and interactive projects.",
            "lead": "A landing page, a portfolio, a web service or a page with an unusual mechanic. We design, code and launch.",
            "items": [
                ("Landing page or portfolio", "A fast page that explains what you do and looks good on a phone."),
                ("Web service", "A page that gathers data and gives a person a ready answer. Our surf forecast, Surf, works this way."),
                ("Interactive graphics", "Graphics in the browser that respond to mouse, touch, gestures and sound. Inkfall is an example."),
                ("Browser game", "A small game that opens from a link with no install and no sign-up. Eyeball is an example."),
            ],
            "examples_title": "Sites you can open right now.",
        },
    },
    {
        "slug": "apps",
        "examples": ["argyns", "fittimer"],
        "stack": "Flutter · Dart · Firebase · iOS · Android",
        "ru": {
            "name": "Приложения и прототипы", "service_type": "Разработка мобильных приложений",
            "title": "Разработка мобильных приложений и прототипов — Void Studio",
            "description": "Void Studio делает приложения для iOS и Android на Flutter и рабочие прототипы продукта. Публикуем в App Store и Google Play.",
            "h1": "Мобильные приложения и прототипы продукта.",
            "lead": "Приложения для iOS и Android на Flutter и рабочие прототипы, на которых можно проверить идею до больших вложений.",
            "items": [
                ("Приложение для iOS и Android", "Один код на Flutter работает на обеих платформах. Доводим до публикации в App Store и Google Play."),
                ("Прототип продукта", "Рабочая версия идеи, чтобы проверить сценарий, интерфейс и техническое решение."),
                ("Серверная часть", "Общая база, регистрация и уведомления на Firebase. Так устроено приложение Argyns."),
            ],
            "examples_title": "Приложения, которые уже в магазинах.",
        },
        "en": {
            "name": "Apps and prototypes", "service_type": "Mobile app development",
            "title": "Mobile app and prototype development — Void Studio",
            "description": "Void Studio builds iOS and Android apps with Flutter and working product prototypes. We publish to the App Store and Google Play.",
            "h1": "Mobile apps and product prototypes.",
            "lead": "iOS and Android apps built with Flutter, and working prototypes that let you test an idea before a large investment.",
            "items": [
                ("App for iOS and Android", "One Flutter codebase runs on both platforms. We take it all the way to the App Store and Google Play."),
                ("Product prototype", "A working version of an idea to test the user journey, interface and technical direction."),
                ("Backend", "A shared database, sign-up and notifications on Firebase. The Argyns app is built this way."),
            ],
            "examples_title": "Apps that are already in the stores.",
        },
    },
    {
        "slug": "automation",
        "examples": ["poster", "podcast"],
        "stack": "Python · aiogram · SQLite · Docker · ffmpeg · Telegram API",
        "ru": {
            "name": "Боты и автоматизация", "service_type": "Разработка Telegram-ботов и автоматизация",
            "title": "Разработка Telegram-ботов и автоматизация — Void Studio",
            "description": "Void Studio делает Telegram-ботов и системы, которые забирают ручную работу: сбор материалов, обработка файлов, публикация по расписанию.",
            "h1": "Telegram-боты и автоматизация рутины.",
            "lead": "Бот или система, которая заберёт повторяющуюся ручную работу: собрать, обработать, опубликовать, записать результат.",
            "items": [
                ("Telegram-бот", "Бот, который принимает запросы, следит за источниками и присылает готовый результат в чат или канал."),
                ("Публикация по расписанию", "Один материал расходится по нескольким площадкам в нужных форматах. Так работает наш Poster 2.0."),
                ("Обработка аудио и видео", "Скачать, перевести в нужный формат, разрезать большие файлы и разослать без участия человека."),
            ],
            "examples_title": "Системы, которые работают каждый день.",
        },
        "en": {
            "name": "Bots and automation", "service_type": "Telegram bot development and automation",
            "title": "Telegram bots and automation — Void Studio",
            "description": "Void Studio builds Telegram bots and systems that take over manual work: collecting material, processing files and publishing on a schedule.",
            "h1": "Telegram bots and automation.",
            "lead": "A bot or a system that takes repetitive manual work off your hands: collect, process, publish and record the result.",
            "items": [
                ("Telegram bot", "A bot that takes requests, watches sources and sends a finished result to a chat or a channel."),
                ("Scheduled publishing", "One piece of content goes to several platforms in the right formats. Our Poster 2.0 works this way."),
                ("Audio and video processing", "Download, convert to the right format, split large files and send them out with no one at the keyboard."),
            ],
            "examples_title": "Systems that run every day.",
        },
    },
    {
        "slug": "ai-visuals",
        "examples": [],
        "stack": "",
        "ru": {
            "name": "AI-изображения и видео", "service_type": "Создание AI-изображений и видео",
            "title": "AI-изображения и видео: реклама, постеры, иллюстрации — Void Studio",
            "description": "Void Studio создаёт изображения и короткие видео с помощью нейросетей: рекламные кадры еды и продуктов, постеры, иллюстрации и серии для соцсетей.",
            "h1": "AI-изображения и видео.",
            "lead": "Изображения и короткие видео, сделанные с помощью нейросетей: рекламные кадры, постеры, иллюстрации и серии для соцсетей.",
            "items": [
                ("Рекламные кадры", "Еда и продукты крупным планом: фактура, свет и настроение без съёмочной площадки."),
                ("Постеры и иллюстрации", "Отдельные изображения и серии в одном стиле для сайта, обложек и публикаций."),
                ("Короткие видео", "Ролики для Instagram, Telegram и YouTube. Готовые работы публикуем в своих каналах."),
            ],
            "examples_title": "Работы из нашей ленты.",
            "gallery_link": "Смотреть все работы ↗",
        },
        "en": {
            "name": "AI images and video", "service_type": "AI image and video production",
            "title": "AI images and video: ads, posters, illustration — Void Studio",
            "description": "Void Studio creates images and short videos with generative AI: food and product shots, posters, illustration and series for social media.",
            "h1": "AI images and video.",
            "lead": "Images and short videos made with generative AI: advertising shots, posters, illustration and series for social media.",
            "items": [
                ("Advertising shots", "Food and products up close: texture, light and mood without a film set."),
                ("Posters and illustration", "Single images and series in one style for a site, covers and posts."),
                ("Short videos", "Clips for Instagram, Telegram and YouTube. We publish finished work in our own channels."),
            ],
            "examples_title": "Work from our feed.",
            "gallery_link": "See all work ↗",
        },
    },
]

# Статьи блога по теме услуги. Блог только на русском.
RELATED = {
    "websites": [("blog/interaktivnyj-sajt.html", "Интерактивный сайт: что это и примеры")],
    "apps": [("blog/mvp-prilozheniya.html", "MVP приложения: что это и как сделать первую версию")],
    "automation": [
        ("blog/telegram-bot-dlya-biznesa.html", "Telegram-бот для бизнеса: что умеет и от чего зависит цена"),
        ("blog/avtoposting-v-socseti.html", "Автопостинг в соцсети без ручной работы"),
    ],
}

SLUGS = [s["slug"] for s in SERVICES]


def path(lang, slug):
    return f"/{UI[lang]['prefix']}{slug}.html"


def language_script():
    routes = {}
    for slug in SLUGS:
        pair = {"ru": path("ru", slug), "en": path("en", slug)}
        routes[pair["ru"]] = pair
        routes[pair["en"]] = pair
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


def render(service, lang):
    ui, text, slug = UI[lang], service[lang], service["slug"]
    other = ui["switch_code"]
    up = "../" if lang == "en" else ""
    url = SITE + path(lang, slug)
    e = escape

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service", "@id": url + "#service", "url": url,
                "name": text["name"], "serviceType": text["service_type"],
                "description": text["description"], "inLanguage": ui["in_language"],
                "provider": {"@id": SITE + "/#organization"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": ui["home"], "item": SITE + ui["home_url"]},
                    {"@type": "ListItem", "position": 2, "name": text["name"], "item": url},
                ],
            },
        ],
    }

    nav = "".join(f'<a href="{href}">{label}</a>' for href, label in ui["nav"])
    items = "".join(
        f'<article class="service"><span>{i:02d}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>'
        for i, (title, body) in enumerate(text["items"], 1)
    )
    steps = "".join(
        f'<li><span>{i:02d}</span><h3>{e(title)}</h3><p>{e(body)}</p></li>'
        for i, (title, body) in enumerate(ui["process"], 1)
    )

    if service["examples"]:
        rows = ""
        for i, key in enumerate(service["examples"], 1):
            project = PROJECTS[key]
            name, kind, body = project[lang]
            link = (
                f'<a href="{project["url"]}" target="_blank" rel="noopener">{"Открыть" if lang == "ru" else "Open"} ↗</a>'
                if project["url"] else ""
            )
            more = "Подробнее" if lang == "ru" else "Details"
            rows += (
                f'<article class="project-row"><span class="index">{i:02d}</span><h3>{e(name)}<small>{e(kind)}</small></h3>'
                f'<div class="project-description"><p>{e(body)}</p></div>'
                f'<div class="project-links">{link}<a href="projects.html#{key}">{more} →</a></div></article>'
            )
        examples = (
            f'<section class="service-examples"><div class="section-head"><div><p class="kicker">{ui["examples_kicker"]}</p>'
            f'<h2>{e(text["examples_title"])}</h2></div><a href="projects.html">{ui["all_projects"]}</a></div>{rows}'
            f'<p class="stack"><span>{ui["stack_kicker"]}:</span> {e(service["stack"])}</p></section>'
        )
    else:
        figures = "".join(
            f'<figure><img src="{up}{src}" alt="{e(ru if lang == "ru" else en)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
            f'<figcaption>{e(ru if lang == "ru" else en)}</figcaption></figure>'
            for src, w, h, ru, en in GALLERY
        )
        examples = (
            f'<section class="service-examples"><div class="section-head"><div><p class="kicker">{ui["examples_kicker"]}</p>'
            f'<h2>{e(text["examples_title"])}</h2></div><a href="{ui["nav"][0][0]}">{text["gallery_link"]}</a></div>'
            f'<div class="service-gallery">{figures}</div></section>'
        )

    others = "".join(
        f'<a class="other-service" href="{s["slug"]}.html"><span>{e(s[lang]["name"])}</span><span aria-hidden="true">→</span></a>'
        for s in SERVICES if s["slug"] != slug
    )
    footer = "".join(f'<a href="{href}">{label}</a>' for href, label in ui["footer"])
    related = ""
    if lang == "ru" and RELATED.get(slug):
        links = "".join(
            f'<a class="other-service" href="{href}"><span>{e(title)}</span><span aria-hidden="true">→</span></a>'
            for href, title in RELATED[slug]
        )
        related = f'<section class="other-services related"><p class="kicker">Статьи по теме</p><div>{links}</div></section>\n'
        footer += '<a href="blog/">Блог</a>'

    return f"""<!doctype html>
<html lang="{ui['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{language_script()}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-E9G3NGMQ6F"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-E9G3NGMQ6F');</script>
<meta name="theme-color" content="#f4f4f0">
<title>{e(text['title'])}</title>
<meta name="description" content="{e(text['description'])}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ru" href="{SITE + path('ru', slug)}">
<link rel="alternate" hreflang="en" href="{SITE + path('en', slug)}">
<link rel="alternate" hreflang="x-default" href="{SITE + path('ru', slug)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{ui['locale']}">
<meta property="og:site_name" content="Void Studio">
<meta property="og:title" content="{e(text['title'])}">
<meta property="og:description" content="{e(text['lead'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ui['og_alt']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(text['title'])}">
<meta name="twitter:description" content="{e(text['lead'])}">
<meta name="twitter:image" content="{SITE}/assets/img/og.png">
<link rel="icon" href="{up}assets/img/favicon-64.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="{up}assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="{up}assets/site.css?v=9">
<link rel="stylesheet" href="{up}assets/services.css?v={CSS_VERSION}">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script>
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body><header class="site-header"><a class="site-logo" href="{ui['nav'][0][0]}" aria-label="{ui['logo_label']}"></a><nav aria-label="{ui['nav_label']}">{nav}<a class="nav-language" href="{'../' if lang == 'en' else 'en/'}{slug}.html" lang="{other}" hreflang="{other}" aria-label="{ui['switch_label']}">{ui['switch_text']}</a><a class="nav-contact" href="{TELEGRAM}" target="_blank" rel="noopener">{ui['contact']}</a></nav></header>
<main>
<section class="service-hero"><p class="kicker">{ui['kicker']} · {e(text['name'])}</p><h1>{e(text['h1'])}</h1><p>{e(text['lead'])}</p><a class="button primary" href="{TELEGRAM}" target="_blank" rel="noopener">{ui['discuss']} ↗</a></section>
<section class="services"><p class="kicker">{ui['includes']}</p><div class="service-grid count-{len(text['items'])}">{items}</div></section>
{examples}
<section class="service-process"><p class="kicker">{ui['process_kicker']}</p><h2>{ui['process_title']}</h2><ol>{steps}</ol></section>
{related}<section class="other-services"><p class="kicker">{ui['other_kicker']}</p><h2>{ui['other_title']}</h2><div>{others}</div></section>
<section class="projects-contact"><p class="kicker">{ui['cta_kicker']}</p><h2>{ui['cta_title']}</h2><a href="{TELEGRAM}" target="_blank" rel="noopener">{ui['cta_link']}</a></section>
</main>
<footer><span>© 2026 Void Studio . Lab</span><div>{footer}<a href="https://github.com/Mihailchik" target="_blank" rel="noopener">GitHub ↗</a></div></footer>
<script>window.shareConfig={{position:"bottom-right"}};</script>
<script src="{up}assets/share.js" defer></script>
</body></html>
"""


def main():
    for service in SERVICES:
        for lang in ("ru", "en"):
            target = ROOT / UI[lang]["prefix"] / f"{service['slug']}.html"
            target.write_text(render(service, lang), encoding="utf-8")
            print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
