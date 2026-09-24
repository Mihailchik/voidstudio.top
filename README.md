# voidstudio.top

Сайт студии Void Studio: лента визуальных работ, рассказ о студии и портфолио
проектов. Живёт на **[voidstudio.top](https://voidstudio.top)**.

Статика без сборки: HTML, CSS и несколько файлов на JavaScript. Vercel отдаёт
файлы как есть и выкатывает каждый push в `main`.

## Страницы

| Файл | Что это |
|---|---|
| `index.html` | главная: лента работ, которую тянут мышью или пальцем |
| `studio.html` | о студии, направления, избранные проекты, контакты |
| `projects.html` | полный список проектов |
| `en/` | те же три страницы на английском |

Язык выбирается сам по языку браузера, выбор запоминается. Русская и английская
версии связаны через `hreflang`.

## Как посмотреть локально

Сборки нет, нужен любой статический сервер:

```bash
python3 -m http.server 4173
```

## Как всё устроено

- `assets/filmstrip.js` — лента на главной. Рисует WebGL, при его отсутствии
  откатывается на обычные картинки.
- `assets/gallery-data.js` — список работ: название, описание, цвета раскрытой
  карточки. Порядок ленты задаётся массивом `suggestedGalleryIds`.
- `assets/site.css` — стили студии и проектов.
- `assets/img/` — логотип и иконки. Белая заливка на прозрачном фоне,
  подключены через CSS `mask`, поэтому красятся любым цветом.

Ничего не считается руками: сколько работ показать, страница берёт из данных.

## Инструменты

`tools/` не публикуется, файлы исключены через `.vercelignore`.

```bash
# витрина работ из библиотеки проекта Poster 2.0
python3 tools/build_media.py --thumbs-only --limit 12
python3 tools/build_media.py

# карточка проекта из скриншотов приложения
python3 tools/build_project_card.py --out assets/project-app.jpg --radius 52 \
    --bg 15161a shot-1.png shot-2.png
```

Домен, DNS и поддомены описаны отдельно, в `~/Trae_PJ/voidstudio.top/DNS.md`.

---

# voidstudio.top (English)

The Void Studio website: a filmstrip of visual work, a page about the studio and
a portfolio of projects. Live at **[voidstudio.top](https://voidstudio.top)**.

Static, with no build step — HTML, CSS and a few JavaScript files. Vercel serves
them as they are and deploys every push to `main`.

## Pages

| File | What it is |
|---|---|
| `index.html` | home: a filmstrip of work you drag with a mouse or a finger |
| `studio.html` | about the studio, services, selected projects, contacts |
| `projects.html` | the full list of projects |
| `en/` | the same three pages in English |

The language follows the browser and the choice is remembered. The Russian and
English versions are linked with `hreflang`.

## Running locally

No build step, any static server will do:

```bash
python3 -m http.server 4173
```

## How it works

- `assets/filmstrip.js` — the filmstrip on the home page. Renders with WebGL and
  falls back to plain images when it is unavailable.
- `assets/gallery-data.js` — the works: titles, descriptions and the colours of
  the expanded card. `suggestedGalleryIds` sets the order.
- `assets/site.css` — styles for the studio and projects pages.
- `assets/img/` — logo and icons: white on transparent, applied through a CSS
  `mask`, so they take any colour.

Nothing is counted by hand: how many works to show comes from the data.

## Tools

`tools/` is never published — the files are excluded through `.vercelignore`.

```bash
# build the works gallery from the Poster 2.0 library
python3 tools/build_media.py --thumbs-only --limit 12
python3 tools/build_media.py

# build a project card out of app screenshots
python3 tools/build_project_card.py --out assets/project-app.jpg --radius 52 \
    --bg 15161a shot-1.png shot-2.png
```

The domain, DNS and subdomains are documented separately, in
`~/Trae_PJ/voidstudio.top/DNS.md`.
