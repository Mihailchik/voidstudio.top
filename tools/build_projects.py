#!/usr/bin/env python3
"""Собирает страницы проектов: projects/<имя>.html и en/projects/<имя>.html.

Тексты лежат здесь же, в PROJECTS. Короткие карточки тех же проектов живут
в projects.html и правятся там руками.

    python3 tools/build_projects.py
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://voidstudio.top"
TELEGRAM = "https://t.me/LuchkoOlga"

UI = {
    "ru": {
        "base": "", "locale": "ru_RU", "in_language": "ru-RU",
        "logo_label": "Void Studio, визуальные работы", "nav_label": "Основная навигация",
        "nav": [("/", "Работы"), ("/projects.html", "Проекты"), ("/studio.html#about", "О студии")],
        "switch_code": "en", "switch_text": "EN", "switch_label": "Переключить на английский",
        "contact": "Написать ↗", "projects": "Проекты", "what": "Что это", "how": "Как устроено",
        "stack": "На чём сделано", "service_kicker": "Сделаем похожее", "service_text": "Расскажите о задаче, и мы предложим решение.",
        "telegram": "Написать в Telegram ↗", "other_kicker": "Другие проекты", "other_title": "Что ещё мы сделали.",
        "article": "Статья по теме", "closed": "Закрытый проект",
        "footer": [("/studio.html", "О студии"), ("/projects.html", "Проекты"), ("/blog/", "Блог")],
        "og_alt": "Логотип Void Studio . Lab", "title_tail": "проект Void Studio",
        "services": {"websites": "Сайты и интерактив", "apps": "Приложения и прототипы", "automation": "Боты и автоматизация"},
    },
    "en": {
        "base": "/en", "locale": "en_US", "in_language": "en",
        "logo_label": "Void Studio, visual work", "nav_label": "Main navigation",
        "nav": [("/en/", "Work"), ("/en/projects.html", "Projects"), ("/en/studio.html#about", "Studio")],
        "switch_code": "ru", "switch_text": "RU", "switch_label": "Switch to Russian",
        "contact": "Contact ↗", "projects": "Projects", "what": "What it is", "how": "How it works",
        "stack": "Built with", "service_kicker": "We can build something similar", "service_text": "Tell us about your task and we will suggest a solution.",
        "telegram": "Message us on Telegram ↗", "other_kicker": "Other projects", "other_title": "What else we have built.",
        "article": "Related article", "closed": "Private project",
        "footer": [("/en/studio.html", "Studio"), ("/en/projects.html", "Projects"), ("/en/blog/", "Blog")],
        "og_alt": "Void Studio . Lab logo", "title_tail": "a Void Studio project",
        "services": {"websites": "Websites and interactive work", "apps": "Apps and prototypes", "automation": "Bots and automation"},
    },
}

PROJECTS = [
    {
        "slug": "surf", "service": "websites", "schema": "WebApplication",
        "stack": "Vanilla JS · Open-Meteo · MET Norway · NOAA · GitHub Pages",
        "article": {"ru": ("/blog/interaktivnyj-sajt.html", "Интерактивный сайт: что это и примеры"), "en": ("/en/blog/interactive-website.html", "Interactive websites: what they are, with examples")},
        "ru": {
            "name": "Surf", "kind": "Веб-сервис",
            "title": "Surf: прогноз волн для серфинга на Пхукете",
            "description": "Surf показывает волну, ветер, прилив и камеры пляжей Пхукета и ставит каждому пляжу оценку от 0 до 10. Как устроен сервис и на чём он сделан.",
            "tagline": "Стоит ли ехать на серфинг прямо сейчас?",
            "what": "Чтобы понять, есть ли сегодня волна, приходится открывать несколько погодных сайтов и сравнивать графики. Surf отвечает на один вопрос: стоит ли ехать сейчас и на какой пляж. Волна, ветер, прилив и камеры пляжей Пхукета и Као Лака собраны на одной странице.",
            "how": [
                ("Оценка от 0 до 10", "Каждый час у каждого пляжа получает число и слово, от «плоско» до «лучше не бывает». Оценка округляется вниз, чтобы пляж не оказался хуже обещанного."),
                ("Несколько моделей", "Данные Open-Meteo, MET Norway и NOAA сводятся в медиану. Разброс между источниками показывает, насколько прогнозу можно верить."),
                ("Без сервера", "Это одна статическая страница. Данные загружаются прямо в браузере, без регистрации и ключей."),
                ("История прогнозов", "Каждое утро записывается, что обещал прогноз и что показали модели за прошедший день. Так видно, где прогноз ошибается."),
                ("Три языка", "Интерфейс на английском, русском и тайском."),
            ],
            "links": [("Открыть Surf ↗", "https://surf.voidstudio.top"), ("Код на GitHub ↗", "https://github.com/Mihailchik/surf")],
        },
        "en": {
            "name": "Surf", "kind": "Web service",
            "title": "Surf: a surf forecast for Phuket",
            "description": "Surf shows waves, wind, tide and beach cameras for Phuket and scores every beach from 0 to 10. How the service works and what it is built with.",
            "tagline": "Is it worth going surfing right now?",
            "what": "To know whether there are waves today you have to open several weather sites and compare charts. Surf answers one question: is it worth going now, and to which beach. Waves, wind, tide and beach cameras for Phuket and Khao Lak sit on one page.",
            "how": [
                ("A score from 0 to 10", "Every hour at every beach gets a number and a word, from flat to epic. The score is rounded down so a beach is never worse than promised."),
                ("Several models", "Data from Open-Meteo, MET Norway and NOAA is combined into a median. The spread between sources shows how far the forecast can be trusted."),
                ("No server", "It is a single static page. Data is loaded straight in the browser, with no sign-up and no keys."),
                ("Forecast history", "Every morning the site records what the forecast promised and what the models show for the day that passed. This makes it clear where the forecast is wrong."),
                ("Three languages", "The interface is in English, Russian and Thai."),
            ],
            "links": [("Open Surf ↗", "https://surf.voidstudio.top"), ("Code on GitHub ↗", "https://github.com/Mihailchik/surf")],
        },
    },
    {
        "slug": "inkfall", "service": "websites", "schema": "WebApplication",
        "stack": "WebGL2 · GLSL · MediaPipe · Web Audio",
        "image": {"ru": ("/assets/project-inkfall.jpg", 1200, 630), "en": ("/assets/project-inkfall.jpg", 1200, 630)},
        "article": {"ru": ("/blog/interaktivnyj-sajt.html", "Интерактивный сайт: что это и примеры"), "en": ("/en/blog/interactive-website.html", "Interactive websites: what they are, with examples")},
        "ru": {
            "name": "Inkfall", "kind": "Интерактивная графика",
            "title": "Inkfall: симуляция чернил в воде в браузере",
            "description": "Inkfall показывает чернила в воде, которыми управляют мышью, пальцами, жестами рук и голосом. Это симуляция жидкости на WebGL. Как она устроена.",
            "tagline": "Чернила в воде: мышью, пальцем, рукой или голосом.",
            "what": "Inkfall показывает воду, в которой расходятся чернила. Каждый кадр видеокарта заново решает уравнения движения жидкости, готового видео здесь нет. Чернила уносит поток, поток закручивается в вихри, тяжёлые чернила тонут, лёгкие поднимаются.",
            "how": [
                ("Шесть характеров", "Чернила, шёлк, дым, масло, акварель и пыльца. Каждый меняет сразу несколько свойств жидкости: от тяжёлого масла до лёгкого дыма."),
                ("Управление руками", "Жесты перед камерой: щепоть рисует, открытая ладонь перемешивает воду, сжатый кулак очищает её. Изображение с камеры обрабатывается на устройстве и никуда не отправляется."),
                ("Голос и музыка", "С включённым микрофоном кистью управляет звук: чем громче, тем быстрее она движется и тем больше чернил оставляет."),
                ("Фото и видео", "Кадр сохраняется в PNG, видео записывается в качестве до 4K. Интерфейс в запись не попадает."),
                ("Один файл", "Вся работа помещается в одну HTML-страницу без сборки и без фреймворков. Устанавливать ничего не нужно."),
            ],
            "links": [("Открыть Inkfall ↗", "https://inkfall.voidstudio.top"), ("Код на GitHub ↗", "https://github.com/Mihailchik/inkfall")],
        },
        "en": {
            "name": "Inkfall", "kind": "Interactive graphic",
            "title": "Inkfall: an ink-in-water simulation in the browser",
            "description": "Inkfall is a WebGL fluid simulation: ink in water driven by mouse, touch, hand gestures and voice. How it works.",
            "tagline": "Ink in water: mouse, finger, hand or voice.",
            "what": "Inkfall shows water with ink blooming through it. Every frame the GPU solves the equations of fluid motion again, and there is no pre-made video. The ink is carried by the flow, the flow curls into vortices, heavy ink sinks and light ink rises.",
            "how": [
                ("Six modes", "Ink, silk, smoke, oil, watercolour and pollen. Each changes several properties of the fluid at once, from heavy oil to light smoke."),
                ("Hand control", "Gestures in front of the camera: a pinch paints, an open palm stirs the water, a held fist clears it. The camera image is processed on the device and never uploaded."),
                ("Voice and music", "With the microphone on, sound drives the brush: the louder it gets, the faster it moves and the more ink it lays."),
                ("Photo and video", "A still is saved as PNG and video is recorded at up to 4K. The interface never appears in the recording."),
                ("One file", "The whole piece is a single HTML page with no build step and no framework. There is nothing to install."),
            ],
            "links": [("Open Inkfall ↗", "https://inkfall.voidstudio.top"), ("Code on GitHub ↗", "https://github.com/Mihailchik/inkfall")],
        },
    },
    {
        "slug": "glazomer", "service": "websites", "schema": "VideoGame",
        "stack": "Vanilla JS · SVG · localStorage",
        "image": {"ru": ("/assets/project-glazomer.jpg", 1600, 1110), "en": ("/assets/project-glazomer-en.jpg", 1600, 1110)},
        "article": {"ru": ("/blog/interaktivnyj-sajt.html", "Интерактивный сайт: что это и примеры"), "en": ("/en/blog/interactive-website.html", "Interactive websites: what they are, with examples")},
        "ru": {
            "name": "Глазомер", "kind": "Браузерная игра",
            "title": "Глазомер: ежедневная браузерная игра на точность глаза",
            "description": "В браузерной игре «Глазомер» пять заданий на глаз и одна попытка в день. Задания одинаковые у всех, результат можно сравнить. Как она устроена.",
            "tagline": "Пять заданий на глаз. Одна попытка в день.",
            "what": "«Глазомер» проверяет, насколько точен ваш глаз. Это ежедневная мини-игра. Линейку нужно убрать. Игра открывается по ссылке и занимает пару минут.",
            "how": [
                ("Пять заданий", "Остановить таймер вслепую, отметить долю отрезка, выставить угол, найти центр круга и оценить число точек."),
                ("Одинаково для всех", "Набор заданий каждый день новый и одинаковый у всех игроков, поэтому результат есть с кем сравнить."),
                ("Балл и сетка", "В конце игрок получает балл из 100 и сетку из эмодзи, которой можно поделиться."),
                ("Без сервера", "Регистрации нет, сервера тоже. Прогресс хранится в браузере."),
            ],
            "links": [("Играть ↗", "https://glazomer.voidstudio.top"), ("Код на GitHub ↗", "https://github.com/Mihailchik/glazomer")],
        },
        "en": {
            "name": "Eyeball", "kind": "Browser game",
            "title": "Eyeball: a daily browser game about judging by eye",
            "description": "Eyeball is a browser game: five tasks done by eye and one attempt a day. Everyone gets the same set, so scores can be compared. How it works.",
            "tagline": "Five tasks done by eye. One attempt a day.",
            "what": "Eyeball is a daily mini-game that tests how accurate your eye is. Put the ruler away. The game opens from a link and takes a couple of minutes.",
            "how": [
                ("Five tasks", "Stop a timer blind, mark a share of a line, set an angle, find the centre of a circle and estimate a number of dots."),
                ("The same for everyone", "The set is new every day and the same for every player, so there is someone to compare your result with."),
                ("A score and a grid", "You finish with a score out of 100 and an emoji grid to share."),
                ("No server", "There is no sign-up and no server. Progress is kept in the browser."),
            ],
            "links": [("Play ↗", "https://glazomer.voidstudio.top"), ("Code on GitHub ↗", "https://github.com/Mihailchik/glazomer")],
        },
    },
    {
        "slug": "argyns", "service": "apps", "schema": "MobileApplication", "os": "iOS, Android",
        "stack": "Flutter · Firebase · iOS · Android",
        "image": {"ru": ("/assets/project-argyn.jpg", 600, 640), "en": ("/assets/project-argyn.jpg", 600, 640)},
        "article": {"ru": ("/blog/mvp-prilozheniya.html", "MVP приложения: что это и как сделать первую версию"), "en": ("/en/blog/app-mvp.html", "An app MVP: what it is and how to build the first version")},
        "ru": {
            "name": "Argyns", "kind": "Приложение для iOS и Android",
            "title": "Argyns: приложение-реестр двенадцати родов Аргын",
            "description": "Мобильное приложение Argyns сделано на Flutter и Firebase. В нём общая база, статистика родов и уведомления о съездах. Опубликовано в App Store и Google Play.",
            "tagline": "Цифровой реестр двенадцати родов Аргын.",
            "what": "Argyns ведёт цифровой реестр двенадцати родов Аргын. Приложение объединяет потомков и помогает сохранить историю рода. Оно опубликовано в App Store и Google Play.",
            "how": [
                ("Единая база", "Общая база с актуальной статистикой представителей родов."),
                ("Счётчик рода", "Численность каждого рода видна наглядно."),
                ("Уведомления", "Важные новости и объявления о съездах приходят уведомлениями."),
                ("Регистрация с городом", "При регистрации человек указывает свой город."),
                ("iOS и Android", "Один код на Flutter работает на обеих платформах."),
            ],
            "links": [("Сайт ↗", "https://argyns.kz"), ("App Store ↗", "https://apps.apple.com/us/app/argyns/id6759314097"), ("Google Play ↗", "https://play.google.com/store/apps/details?id=com.argyn.app")],
        },
        "en": {
            "name": "Argyns", "kind": "iOS and Android app",
            "title": "Argyns: a registry app for the twelve Argyn clans",
            "description": "Argyns is a mobile app built with Flutter and Firebase: a shared database, clan statistics and gathering announcements. Available on the App Store and Google Play.",
            "tagline": "A digital registry for the twelve Argyn clans.",
            "what": "Argyns is a digital registry for the twelve Argyn clans. The app brings descendants together and helps keep the history of the clan. It is available on the App Store and Google Play.",
            "how": [
                ("A shared database", "One database with up-to-date statistics on clan members."),
                ("Clan counter", "The size of every clan is shown at a glance."),
                ("Notifications", "Important news and gathering announcements arrive as notifications."),
                ("Sign-up with a city", "People give their city when they register."),
                ("iOS and Android", "One Flutter codebase runs on both platforms."),
            ],
            "links": [("Website ↗", "https://argyns.kz"), ("App Store ↗", "https://apps.apple.com/us/app/argyns/id6759314097"), ("Google Play ↗", "https://play.google.com/store/apps/details?id=com.argyn.app")],
        },
    },
    {
        "slug": "fittimer", "service": "apps", "schema": "MobileApplication", "os": "iOS",
        "stack": "Flutter · Dart · iPhone и iPad",
        "image": {"ru": ("/assets/project-fittimer.jpg", 1600, 1300), "en": ("/assets/project-fittimer-en.jpg", 1600, 1300)},
        "article": {"ru": ("/blog/mvp-prilozheniya.html", "MVP приложения: что это и как сделать первую версию"), "en": ("/en/blog/app-mvp.html", "An app MVP: what it is and how to build the first version")},
        "ru": {
            "name": "FitTimer", "kind": "Мобильное приложение",
            "title": "FitTimer: таймер интервальных тренировок для iPhone и iPad",
            "description": "Таймер FitTimer подходит для Tabata, HIIT, EMOM, AMRAP и своих круговых тренировок. Без регистрации, рекламы и сбора данных. Как устроено приложение.",
            "tagline": "Интервальный таймер, с которым можно не смотреть в телефон.",
            "what": "FitTimer помогает вести интервальные тренировки на iPhone и iPad: Tabata, HIIT, EMOM, AMRAP и собственные круговые. Приложение опубликовано в App Store.",
            "how": [
                ("Быстрый старт", "Три колеса: работа, отдых, раунды. Тренировка запускается за несколько секунд."),
                ("Шаблоны", "Tabata, EMOM, AMRAP и HIIT можно запустить как есть или сохранить и изменить."),
                ("Свои тренировки", "Тренировка собирается из блоков с повторами: разминка, круг, заминка. Блоки переставляются перетаскиванием."),
                ("Экран тренировки", "Экран целиком заливается цветом фазы. Крупные цифры, кольцо прогресса и подсказка, что дальше."),
                ("Сигналы", "Отсчёт 3-2-1 звучит поверх музыки. Если экран погас, смена интервала приходит уведомлением."),
                ("Точное время", "Время считается по часам устройства, поэтому не сбивается после пауз и переключения между приложениями."),
                ("Без аккаунта", "Нет регистрации, рекламы и слежки. Данные остаются на устройстве."),
            ],
            "links": [("App Store ↗", "https://apps.apple.com/ru/app/fittimer999/id6755115543"), ("Код на GitHub ↗", "https://github.com/Mihailchik/flutter_timer_Test")],
        },
        "en": {
            "name": "FitTimer", "kind": "Mobile app",
            "title": "FitTimer: an interval training timer for iPhone and iPad",
            "description": "FitTimer is a timer for Tabata, HIIT, EMOM, AMRAP and your own circuits. No account, no ads, no tracking. How the app works.",
            "tagline": "An interval timer that lets you keep your eyes off the phone.",
            "what": "FitTimer is an interval training timer for iPhone and iPad: Tabata, HIIT, EMOM, AMRAP and your own circuits. The app is available on the App Store.",
            "how": [
                ("Quick start", "Three wheels: work, rest, rounds. A workout starts in a few seconds."),
                ("Templates", "Tabata, EMOM, AMRAP and HIIT can be started as they are or saved and edited."),
                ("Your workouts", "A workout is built from blocks with repeats: warm-up, circuit, cool-down. Drag blocks to reorder them."),
                ("Workout screen", "The whole screen takes the colour of the phase. Big digits, a progress ring and a hint about what comes next."),
                ("Cues", "The 3-2-1 countdown plays over your music. If the screen is off, interval changes arrive as notifications."),
                ("Exact time", "Time is counted from the device clock, so it stays right after pauses and switching apps."),
                ("No account", "No sign-up, no ads, no tracking. Data stays on the device."),
            ],
            "links": [("App Store ↗", "https://apps.apple.com/app/id6755115543"), ("Code on GitHub ↗", "https://github.com/Mihailchik/flutter_timer_Test")],
        },
    },
    {
        "slug": "poster", "service": "automation", "schema": "SoftwareApplication",
        "stack": "Python · SQLite · Docker · Telegram API",
        "article": {"ru": ("/blog/avtoposting-v-socseti.html", "Автопостинг в соцсети без ручной работы"), "en": ("/en/blog/scheduled-social-posting.html", "Scheduled social posting without manual work")},
        "ru": {
            "name": "Poster 2.0", "kind": "Автоматизация",
            "title": "Poster 2.0: система автопостинга для нескольких площадок",
            "description": "Poster 2.0 готовит один выпуск для Telegram, Instagram, YouTube и Pikabu, проверяет файлы и публикует по расписанию. Как устроена система.",
            "tagline": "Один выпуск для нескольких площадок.",
            "what": "Poster 2.0 хранит идеи и материалы, собирает форматы для Telegram, Instagram, YouTube и Pikabu, проверяет файлы, планирует публикации и записывает результат. На этой системе работает контент Void Studio.",
            "how": [
                ("Наполнение", "В систему попадают идея, текст и исходные материалы. У каждого проекта свой паспорт: тема, язык, площадки и расписание."),
                ("Подготовка форматов", "Из одного выпуска собираются картинки и видео нужных размеров и подписи для каждой площадки. Шаг работает по шаблонам, без нейросетей."),
                ("Проверка", "Готовые файлы проходят автоматическую проверку до того, как попадут в расписание."),
                ("Одобрение человеком", "Перед выходом администратор получает предпросмотр и решает, публиковать или нет. Без одобрения ничего не выходит."),
                ("Публикация и учёт", "В назначенное время система публикует выпуск и записывает, что вышло и с каким результатом."),
            ],
            "links": [],
        },
        "en": {
            "name": "Poster 2.0", "kind": "Automation",
            "title": "Poster 2.0: a scheduled publishing system for several platforms",
            "description": "Poster 2.0 prepares one release for Telegram, Instagram, YouTube and Pikabu, validates files and publishes on a schedule. How the system works.",
            "tagline": "One release for several platforms.",
            "what": "Poster 2.0 stores ideas and media, prepares formats for Telegram, Instagram, YouTube and Pikabu, validates files, schedules publications and records the result. It runs the Void Studio content workflow.",
            "how": [
                ("Content", "An idea, a text and source media go into the system. Every project has its own profile: topic, language, platforms and schedule."),
                ("Formats", "One release becomes images and video in the right sizes, with captions for each platform. This step runs on templates, with no AI."),
                ("Validation", "Finished files are checked automatically before they reach the schedule."),
                ("Human approval", "Before a release goes out, an admin gets a preview and decides whether to publish. Nothing goes out without approval."),
                ("Publishing and records", "At the set time the system publishes the release and records what went out and with what result."),
            ],
            "links": [],
        },
    },
    {
        "slug": "podcast", "service": "automation", "schema": "SoftwareApplication",
        "stack": "Python · aiogram · yt-dlp · ffmpeg · SQLite",
        "article": {"ru": ("/blog/telegram-bot-dlya-biznesa.html", "Telegram-бот для бизнеса: что умеет и от чего зависит цена"), "en": ("/en/blog/telegram-bot-for-business.html", "A Telegram bot for business: what it can do and what the cost depends on")},
        "ru": {
            "name": "Podcast Bot", "kind": "Telegram-бот",
            "title": "Podcast Bot: Telegram-бот, который собирает подкасты в один канал",
            "description": "Podcast Bot следит за RSS, YouTube и Telegram, скачивает новые выпуски, переводит звук в MP3 и отправляет в канал. Как устроен бот.",
            "tagline": "Подкасты из разных источников в одном канале.",
            "what": "Podcast Bot собирает подкасты из разных мест в один Telegram-канал. Он сам следит за источниками, скачивает новые выпуски и присылает их в удобном для прослушивания виде.",
            "how": [
                ("Три вида источников", "Ленты RSS, каналы и плейлисты YouTube и каналы Telegram."),
                ("Проверка по расписанию", "Бот сам проверяет источники и забирает новые выпуски, человек для этого не нужен."),
                ("Две версии", "Каждый выпуск приводится к MP3 и отправляется в двух версиях: обычной и ускоренной вдвое."),
                ("Большие файлы", "Слишком большие файлы бот делит на части перед отправкой."),
                ("Ссылки от людей", "Боту можно прислать ссылку, и он поставит её в очередь на обработку."),
            ],
            "links": [("Код на GitHub ↗", "https://github.com/Mihailchik/podcastQ")],
        },
        "en": {
            "name": "Podcast Bot", "kind": "Telegram bot",
            "title": "Podcast Bot: a Telegram bot that gathers podcasts into one channel",
            "description": "Podcast Bot watches RSS, YouTube and Telegram, downloads new episodes, converts audio to MP3 and sends it to a channel. How the bot works.",
            "tagline": "Podcasts from different sources in one channel.",
            "what": "Podcast Bot gathers podcasts from different places into one Telegram channel. It watches the sources by itself, downloads new episodes and sends them in a form that is easy to listen to.",
            "how": [
                ("Three kinds of sources", "RSS feeds, YouTube channels and playlists, and Telegram channels."),
                ("Scheduled checks", "The bot checks the sources and picks up new episodes by itself; no one has to do it."),
                ("Two versions", "Every episode is converted to MP3 and sent in two versions: normal and double speed."),
                ("Large files", "Files that are too large are split into parts before sending."),
                ("Links from people", "You can send the bot a link and it will queue it for processing."),
            ],
            "links": [("Code on GitHub ↗", "https://github.com/Mihailchik/podcastQ")],
        },
    },
]


def path(lang, slug):
    return f"{UI[lang]['base']}/projects/{slug}.html"


def language_script(slug):
    pair = {"ru": path("ru", slug), "en": path("en", slug)}
    table = json.dumps({pair["ru"]: pair, pair["en"]: pair}, separators=(",", ":"))
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


def render(project, lang):
    ui, text, slug = UI[lang], project[lang], project["slug"]
    other = ui["switch_code"]
    url = SITE + path(lang, slug)
    e = escape
    image = project.get("image", {}).get(lang)
    og_image = SITE + (image[0] if image else "/assets/img/og.png")

    app = {
        "@type": project["schema"], "@id": url + "#project", "url": url, "name": text["name"],
        "description": text["description"], "inLanguage": ui["in_language"],
        "creator": {"@id": SITE + "/#organization"},
    }
    if project["schema"] != "VideoGame":
        app["applicationCategory"] = text["kind"]
    if project["schema"] in ("WebApplication", "VideoGame"):
        app["operatingSystem"] = "Any"
    if project.get("os"):
        app["operatingSystem"] = project["os"]
    if image:
        app["image"] = og_image
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            app,
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Void Studio", "item": SITE + ui["nav"][0][0]},
                    {"@type": "ListItem", "position": 2, "name": ui["projects"], "item": SITE + ui["nav"][1][0]},
                    {"@type": "ListItem", "position": 3, "name": text["name"], "item": url},
                ],
            },
        ],
    }

    nav = "".join(f'<a href="{href}">{label}</a>' for href, label in ui["nav"])
    buttons = "".join(
        f'<a class="button{" primary" if i == 0 else ""}" href="{href}" target="_blank" rel="noopener">{e(label)}</a>'
        for i, (label, href) in enumerate(text["links"])
    ) or f'<span class="project-closed">{ui["closed"]}</span>'
    shot = (
        f'<figure class="project-shot"><img src="{image[0]}" alt="{e(text["name"])}, {e(text["kind"].lower())}" width="{image[1]}" height="{image[2]}" fetchpriority="high"></figure>'
        if image else ""
    )
    cards = "".join(
        f'<article class="service"><span>{i:02d}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>'
        for i, (title, body) in enumerate(text["how"], 1)
    )
    article_href, article_title = project["article"][lang]
    service = project["service"]
    others = "".join(
        f'<a class="other-service" href="{path(lang, p["slug"])}"><span>{e(p[lang]["name"])} <small>{e(p[lang]["kind"])}</small></span><span aria-hidden="true">→</span></a>'
        for p in PROJECTS if p["slug"] != slug
    )
    footer = "".join(f'<a href="{href}">{label}</a>' for href, label in ui["footer"])
    stack = project["stack"] if lang == "ru" else project["stack"].replace("iPhone и iPad", "iPhone and iPad")

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{language_script(slug)}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-E9G3NGMQ6F"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-E9G3NGMQ6F');</script>
<meta name="theme-color" content="#f4f4f0">
<title>{e(text['title'])} | Void Studio</title>
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
<meta property="og:description" content="{e(text['tagline'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon-64.png" type="image/png" sizes="64x64">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/site.css?v=9">
<link rel="stylesheet" href="/assets/services.css?v=4">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}};</script>
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body><header class="site-header"><a class="site-logo" href="{ui['nav'][0][0]}" aria-label="{ui['logo_label']}"></a><nav aria-label="{ui['nav_label']}">{nav}<a class="nav-language" href="{path(other, slug)}" lang="{other}" hreflang="{other}" aria-label="{ui['switch_label']}">{ui['switch_text']}</a><a class="nav-contact" href="{TELEGRAM}" target="_blank" rel="noopener">{ui['contact']}</a></nav></header>
<main>
<section class="service-hero project-hero"><p class="kicker"><a href="{ui['nav'][1][0]}">{ui['projects']}</a> · {e(text['kind'])}</p><h1>{e(text['name'])}</h1><p>{e(text['tagline'])}</p><div class="hero-actions">{buttons}</div></section>
{shot}
<section class="project-what"><p class="kicker">{ui['what']}</p><p>{e(text['what'])}</p></section>
<section class="services"><p class="kicker">{ui['how']}</p><div class="service-grid">{cards}</div><p class="stack"><span>{ui['stack']}:</span> {e(stack)}</p></section>
<section class="other-services related"><p class="kicker">{ui['article']}</p><div><a class="other-service" href="{article_href}"><span>{e(article_title)}</span><span aria-hidden="true">→</span></a></div></section>
<section class="project-service"><p class="kicker">{ui['service_kicker']}</p><a class="project-service-link" href="{ui['base']}/{service}.html">{ui['services'][service]} →</a><p>{ui['service_text']}</p><a class="button primary" href="{TELEGRAM}" target="_blank" rel="noopener">{ui['telegram']}</a></section>
<section class="other-services"><p class="kicker">{ui['other_kicker']}</p><h2>{ui['other_title']}</h2><div>{others}</div></section>
</main>
<footer><span>© 2026 Void Studio . Lab</span><div>{footer}<a href="https://github.com/Mihailchik" target="_blank" rel="noopener">GitHub ↗</a></div></footer>
<script src="/assets/track.js" defer></script>
<script>window.shareConfig={{position:"bottom-right"}};</script>
<script src="/assets/share.js" defer></script>
</body></html>
"""


def main():
    for project in PROJECTS:
        for lang in ("ru", "en"):
            target = ROOT / path(lang, project["slug"]).lstrip("/")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(project, lang), encoding="utf-8")
            print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
