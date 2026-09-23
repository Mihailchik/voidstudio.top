# SEO-чек-лист для Void Studio

Актуально на 12 сентября 2026 года. Область: небольшой русскоязычный сайт-портфолио `https://voidstudio.top/`. Источники — официальная документация Google Search Central и стандарты Schema.org/Sitemaps.

## Главное

- SEO не гарантирует первое место и даже сам факт индексации. Минимум для участия в поиске: Googlebot не заблокирован, страница публично отвечает HTTP `200`, на ней есть индексируемый контент. [Технические требования Google](https://developers.google.com/search/docs/essentials/technical)
- Тега с «кодовыми словами» для Google нет: `<meta name="keywords">` не влияет ни на индексацию, ни на ранжирование. Нужны естественные слова в видимом тексте, заголовках, названиях и описаниях работ. [Поддерживаемые Google метатеги](https://developers.google.com/search/docs/crawling-indexing/special-tags)
- Самый сильный практический актив такого сайта — отдельные содержательные страницы/кейсы: задача, идея, что сделано студией, формат, результат и изображения/видео. Google рекомендует полезный, оригинальный, ориентированный на людей контент. [People-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)

## P0 — сделать до или сразу после публикации

### 1. Единая версия домена и индексируемые страницы

- Основная версия: `https://voidstudio.top/` без `www`.
- Настроить постоянные редиректы с `http://voidstudio.top/` и `https://www.voidstudio.top/` на основную HTTPS-версию.
- Каждая публичная страница должна отвечать `200`; удалённая — настоящим `404`/`410`, а не пустой страницей с `200`.
- Не публиковать прототипы и служебные каталоги. Если файл уже доступен в интернете и должен исчезнуть из Google, использовать пароль или `noindex`; одного запрета в `robots.txt` недостаточно, потому что URL всё равно может попасть в индекс. [Назначение robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- Все важные страницы связать обычными ссылками `<a href="…">` с понятным текстом. Для самостоятельной индексации каждой работы ей нужен собственный стабильный URL; открытие карточки только по клику/фрагменту `#…` не создаёт полноценную отдельную страницу. [Руководство для разработчиков](https://developers.google.com/search/docs/fundamentals/get-started-developers)

### 2. `robots.txt`

Разместить строго по адресу `https://voidstudio.top/robots.txt`:

```txt
User-agent: *
Allow: /

Sitemap: https://voidstudio.top/sitemap.xml
```

Не закрывать CSS, JavaScript, изображения и видео, которые нужны для отображения публичных страниц. `robots.txt` управляет сканированием, а не надёжным удалением HTML-страниц из поиска. [Руководство Google по robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro) · [Правила разбора robots.txt](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)

### 3. `sitemap.xml`

Разместить UTF-8 XML-карту по адресу `https://voidstudio.top/sitemap.xml`. Включать только абсолютные канонические URL, которые действительно должны быть в поиске. Для текущего публичного набора проверить такой состав:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://voidstudio.top/</loc></url>
  <url><loc>https://voidstudio.top/studio.html</loc></url>
  <url><loc>https://voidstudio.top/projects.html</loc></url>
</urlset>
```

`<lastmod>` добавлять только при возможности указывать реальную дату существенного изменения контента; не обновлять её фиктивно при каждом деплое. Карту указать в `robots.txt` и отправить в Search Console. Sitemap — подсказка, а не гарантия индексации. [Создание и отправка sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) · [Протокол Sitemaps](https://www.sitemaps.org/protocol.html)

### 4. Canonical

На каждой индексируемой странице поставить один абсолютный self-referencing canonical непосредственно в исходном HTML:

```html
<link rel="canonical" href="https://voidstudio.top/">
```

Для остальных страниц заменить URL на их собственный канонический адрес. Canonical, URL в sitemap и внутренние ссылки должны совпадать. Если одна страница доступна как `/studio`, `/studio.html` и с параметрами, выбрать один адрес, остальные перенаправить. Не применять `robots.txt`, URL Removal или `noindex` как замену canonical. [Канонизация URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)

### 5. Уникальные `<title>`, H1 и meta description

- На каждой странице — один ясный видимый H1 и уникальный краткий `<title>`, точно соответствующий содержимому.
- Рабочие варианты, которые нужно сверить с фактическим текстом:
  - главная: `Void Studio — AI-видео, изображения и визуальные проекты`;
  - студия: `О студии Void Studio — подход и услуги`;
  - проекты: `Проекты Void Studio — собственные продукты и эксперименты`.
- Бренд допустимо кратко добавлять в начало или конец, но не повторять одинаковую длинную формулу на всех страницах.
- Для каждой страницы написать отдельный `meta description`: нормальное предложение о конкретной странице, а не перечень запросов. Фиксированного лимита символов у Google нет; сниппет обрезается под устройство, и Google может взять более подходящий фрагмент из видимого текста.
- Google формирует заголовок результата автоматически из `<title>`, видимого главного заголовка, H1, `og:title`, ссылочного текста и других сигналов, поэтому они не должны противоречить друг другу. [Title links](https://developers.google.com/search/docs/appearance/title-link) · [Сниппеты и meta description](https://developers.google.com/search/docs/appearance/snippet)

### 6. Доступный статический текст и JavaScript

- Ключевые H1, описания студии/услуг/работ и навигационные ссылки лучше отдавать сразу в HTML. Google исполняет JavaScript, но рендеринг — отдельный этап и может задерживаться; статический HTML быстрее и надёжнее для пользователей и роботов.
- Смысл изображения или видео продублировать обычным текстом рядом: текст внутри ролика и текст, нарисованный в `canvas`, не заменяют HTML-текст.
- Ссылки делать как `<a href="полный-или-относительный-URL">`, а важный контент — доступным в DOM без обязательного клика, свайпа или ввода.
- Не закрывать от Google JS/CSS, нужные для рендера. Проверить итоговый rendered HTML и снимок страницы через URL Inspection. [Основы JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) · [SEO для разработчиков](https://developers.google.com/search/docs/fundamentals/get-started-developers)

## P1 — поисковое представление

### 7. Organization JSON-LD на главной

Добавить один блок на главную или страницу о студии. Не выдумывать адрес, телефон, ИНН или профили: разметка должна соответствовать реально доступной информации.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://voidstudio.top/#organization",
  "name": "Void Studio",
  "url": "https://voidstudio.top/",
  "logo": "https://voidstudio.top/assets/img/logo-cat.png",
  "description": "Креативная студия визуальных проектов, изображений и видео."
}
</script>
```

Логотип `logo-cat.png` имеет достаточный размер 608×608; Google требует минимум 112×112, доступный для сканирования URL и корректный вид на белом фоне. Когда появятся подтверждённые контактные данные и официальные профили, можно добавить `email`, `telephone`, `address`, `sameAs`, `legalName` и `taxID`. Проверить код в [Rich Results Test](https://search.google.com/test/rich-results), затем через URL Inspection. Разметка помогает Google понять организацию, но не гарантирует расширенный результат. [Organization у Google](https://developers.google.com/search/docs/appearance/structured-data/organization) · [Organization в Schema.org](https://schema.org/Organization)

### 8. Open Graph

На каждой публичной странице синхронизировать `og:title` с реальным заголовком, `og:description` — с описанием, `og:url` — с canonical; поставить абсолютный `og:image` с репрезентативным изображением высокого разрешения и неэкстремальных пропорций.

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Void Studio">
<meta property="og:title" content="…">
<meta property="og:description" content="…">
<meta property="og:url" content="https://voidstudio.top/…">
<meta property="og:image" content="https://voidstudio.top/assets/img/…">
```

Это не «ключевые слова» и не обещание роста позиций. Google указывает `og:title` среди источников title link, а `og:image` — как способ обозначить предпочтительное изображение. [Title links](https://developers.google.com/search/docs/appearance/title-link) · [Изображения в Google](https://developers.google.com/search/docs/appearance/google-images)

### 9. Изображения

- Основные работы размещать через `<img src>` или `<picture>`; Google не индексирует изображения, заданные только CSS `background-image`.
- Для содержательных изображений — короткий естественный `alt`, описывающий увиденное и его роль; для чисто декоративных — `alt=""`.
- Использовать стабильные короткие описательные имена файлов, релевантный текст/подпись рядом, качественные исходники и адаптивные размеры. Сжимать без заметной потери качества, задавать `width`/`height`, чтобы не было скачков макета.
- Изображения не закрывать в robots.txt. Image sitemap нужен только если важные изображения иначе трудно обнаружить; для обычных `<img src>` небольшого сайта он необязателен. [Рекомендации Google Images](https://developers.google.com/search/docs/appearance/google-images)

### 10. Видео

- Встраивать видео стандартным `<video>`, `<embed>`, `<iframe>` или `<object>`; не делать загрузку зависимой только от клика/свайпа и не использовать фрагмент URL как единственный адрес видео.
- Для выхода именно в видео-результаты каждой важной работе лучше дать индексируемую страницу, где ролик — основной контент, с уникальными title/description, текстовым описанием и стабильной доступной миниатюрой (`poster`).
- Если видео-поиск важен, добавить согласованные `VideoObject` и/или video sitemap: `name`, `description`, `thumbnailUrl`, `contentUrl` должны правдиво описывать конкретный ролик. Контейнер, миниатюра и сам видеофайл должны быть доступны Googlebot.
- Проверять Video indexing и Video rich results в Search Console. [Видео SEO](https://developers.google.com/search/docs/appearance/video)

## P1 — подключение Google и контроль качества

### 11. Search Console

После выхода домена в интернет:

1. Добавить Domain property `voidstudio.top` и подтвердить владение DNS TXT-записью. Это охватит протоколы и поддомены; для URL-prefix property возможна проверка HTML-файлом или `<meta name="google-site-verification">` в `<head>` главной.
2. Не удалять DNS/HTML-подтверждение: Search Console периодически перепроверяет его.
3. Отправить `https://voidstudio.top/sitemap.xml`.
4. Через URL Inspection проверить live-версии главной, `/studio.html` и `/projects.html`: доступ, HTTP-код, отсутствие `noindex`, rendered HTML, ресурсы, user-declared и Google-selected canonical.
5. Нажать Request indexing для нескольких главных URL. Для массовых обновлений использовать sitemap с честным `<lastmod>`. Запрос не гарантирует включение и может обрабатываться от дней до недель.
6. После накопления данных смотреть Performance, Page indexing, Core Web Vitals, Enhancements, Manual actions и Security issues. [Проверка владения](https://support.google.com/webmasters/answer/9008080) · [URL Inspection](https://support.google.com/webmasters/answer/9012289)

### 12. Core Web Vitals

Цели на 75-м перцентиле реальных визитов:

- LCP ≤ 2,5 с;
- INP < 200 мс;
- CLS ≤ 0,1.

Для визуального портфолио особенно важны: не загружать все тяжёлые изображения/ролики сразу; правильно подбирать размеры файлов; задавать размеры медиа; не лениво загружать главный LCP-кадр; не блокировать первый экран тяжёлым JavaScript; резервировать место под шрифты и медиа. Измерять лабораторно в PageSpeed Insights, а после появления трафика — по полевым данным Core Web Vitals в Search Console. Хорошие показатели помогают общему качеству страницы, но не являются отдельной гарантией высокой позиции. [Core Web Vitals и поиск](https://developers.google.com/search/docs/appearance/core-web-vitals)

## Чего не делать

- Не добавлять `meta keywords` — Google его игнорирует.
- Не повторять десятки раз «AI студия», «нейросети», «создание видео» и географические названия. Не прятать ключи белым текстом, за экраном, в `alt` или JSON-LD. Keyword stuffing нарушает spam policies. [Spam policies: keyword stuffing](https://developers.google.com/search/docs/essentials/spam-policies#keyword-stuffing)
- Не покупать массовые ссылки и не делать обмен ссылками ради PageRank. [Spam policies: link spam](https://developers.google.com/search/docs/essentials/spam-policies#link-spam)
- Не создавать десятки почти одинаковых страниц под каждую формулировку запроса/город без самостоятельной пользы.
- Не обещать в title/description/structured data то, чего нет на видимой странице.
- Не считать Lighthouse 100/100, sitemap, JSON-LD или отправку URL в Search Console гарантией позиций.

## Проверка после внедрения

- Открываются: `/robots.txt`, `/sitemap.xml`, все URL из sitemap и все указанные медиа.
- На каждом публичном URL ровно один правильный canonical, уникальные title/H1/description и согласованный Open Graph.
- Без JavaScript в исходном HTML остаются название страницы, существенное описание и навигационные ссылки; после рендера Google видит все работы.
- Нет `noindex` на публичных страницах и нет запрета нужных ресурсов в robots.txt.
- JSON-LD проходит Rich Results Test и совпадает с видимыми сведениями.
- Search Console видит sitemap без ошибок и показывает выбранные Google canonical.
- Полевые CWV достигли целевых значений либо заведён список конкретных проблем для исправления.

Изменения в поиске проявляются не мгновенно: Google должен повторно просканировать и обработать страницы; индексация и выбранный сниппет не гарантируются.
