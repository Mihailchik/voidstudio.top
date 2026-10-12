"""Английские версии статей блога. Ключ — адрес русской статьи из build_blog.py.

Перевод держим рядом с оригиналом по смыслу. Если поменялась русская статья,
поправить и здесь, потом заново запустить tools/build_blog.py.
Писать просто: без длинного тире и без оборотов "not X but Y".
"""

ARTICLES_EN = {
    "avtoposting-v-socseti": {
        "slug": "scheduled-social-posting",
        "title": "Scheduled social posting: publishing to Telegram, Instagram and YouTube without manual work",
        "short": "Scheduled social posting without manual work",
        "seo_title": "Scheduled social posting: Telegram, Instagram, YouTube",
        "description": "What scheduled posting is, when an off-the-shelf tool is enough and when you need your own system. Explained through Poster 2.0, the system behind Void Studio's publishing.",
        "lead": "One piece of content has to be prepared separately for every platform, because image sizes and caption lengths differ. Here is how we removed that work for ourselves.",
        "body": """
<h2>What scheduled posting is</h2>
<p>Scheduled posting means a post goes out by itself at a set time. You prepare the content once and a system sends it to Telegram, Instagram, YouTube and other platforms on a schedule.</p>
<p>Most of the time goes into preparation. Every platform has its own requirements for image size and caption length, so one release turns into several files and texts.</p>

<h2>An off-the-shelf tool or your own system</h2>
<p>A ready-made scheduling tool is enough if you run one or two platforms and publish the content as it is.</p>
<p>Your own system makes sense in these cases:</p>
<ul>
<li>content has to be reworked for each platform;</li>
<li>images are built from a template out of text and a background;</li>
<li>there are several projects, each with its own schedule and accounts;</li>
<li>a person has to approve a post before it goes out;</li>
<li>you need to see what went out and what failed.</li>
</ul>

<h2>How our Poster 2.0 works</h2>
<p>We built such a system for ourselves, and Void Studio's posts go out through it. The work happens in three steps.</p>
<h3>1. Content</h3>
<p>An idea, a text and source media go into the system. Every project has a profile that records its topic, language, platforms and schedule. Thanks to the profile, a new project can be added without changing code.</p>
<h3>2. Formats</h3>
<p>From one release the system builds images and video in the right sizes for every platform, with captions. This step runs on templates and uses no AI, so the result is predictable. The finished files go through an automatic check.</p>
<h3>3. Publishing</h3>
<p>The release takes its slot in the schedule. An admin gets a preview in advance and presses OK or Reject. Until a person approves the release, it stays unpublished. At the set time the system checks the files once more, publishes and records the result.</p>

<h2>What this gives you</h2>
<ul>
<li>A release is prepared once for all platforms.</li>
<li>Posts go out on schedule even when everyone is busy.</li>
<li>A broken file is found before publishing.</li>
<li>For every release you can see where it went out and with what result.</li>
</ul>

<h2>Where to start</h2>
<p>Write down what you do by hand for every post: which sizes you prepare, where and when you send them, who checks. The steps that repeat the same way every time can be handed to a system first. Usually that is preparing sizes and sending on a schedule.</p>
""",
    },
    "telegram-bot-dlya-biznesa": {
        "slug": "telegram-bot-for-business",
        "title": "A Telegram bot for business: what it can do and what the cost depends on",
        "short": "A Telegram bot for business: what it can do and what the cost depends on",
        "seo_title": "Telegram bot for business: features and cost",
        "description": "Which tasks a Telegram bot solves, how it is built inside and what makes up the cost of building and running one. With an example of a working bot.",
        "lead": "A Telegram bot answers people and does work on a schedule. Here is which tasks are worth handing to it and what affects the price.",
        "body": """
<h2>What a Telegram bot can do</h2>
<p>A bot replies to messages and runs tasks by itself on a schedule. These are the usual jobs for it:</p>
<ul>
<li>take a request or a booking and pass it to a member of staff;</li>
<li>answer frequent questions without an operator;</li>
<li>watch sources and send new items to a channel;</li>
<li>download a file, convert it and send it out;</li>
<li>send a reminder or a daily summary.</li>
</ul>
<p>A bot suits actions that repeat the same way many times. When a live conversation is needed, the bot takes the request and hands it to a person.</p>

<h2>An example: a bot that gathers podcasts</h2>
<p>Our Podcast Bot runs by itself. It watches RSS feeds, YouTube channels and playlists, and Telegram channels. When a new episode comes out, the bot does the following:</p>
<ol>
<li>downloads the episode;</li>
<li>converts the audio to MP3;</li>
<li>prepares a normal version and a double-speed one;</li>
<li>splits files that are too large into parts;</li>
<li>sends everything to a channel and deletes temporary files.</li>
</ol>
<p>Sources are checked on a schedule. You can also send the bot a link and it will queue it for processing. The state of every episode is written to a database, so the bot knows what has been sent and what is still waiting.</p>

<h2>What a bot is made of</h2>
<p>We write the bot's code in Python with the aiogram library. Next to the code runs a database that keeps what has been done and what is in the queue. SQLite is enough for small bots.</p>
<p>A bot has to run around the clock, so it needs a server. We run bots in Docker, which makes them easier to move and restart.</p>
<p>If a bot takes payments, writes to a spreadsheet or a CRM, or calls an AI model, those external services are connected to it.</p>

<h2>What the cost depends on</h2>
<p>The price is set by the number of scenarios and connections to other systems.</p>
<ul>
<li>How many scenarios there are. Answering three questions is simpler than walking a person through a booking with a choice of time.</li>
<li>How many integrations there are. Every connection to payments, a CRM or a spreadsheet needs its own work and testing.</li>
<li>Whether the bot handles files. Audio, video and large files have to be processed and stored somewhere.</li>
<li>Whether an admin panel is needed to change texts and settings without a developer.</li>
<li>What the load is. A bot for a hundred thousand people is more complex than a bot for a hundred.</li>
</ul>
<p>After launch there are costs for a server and maintenance. The platforms a bot works with change their rules, and the code has to be updated.</p>

<h2>How to tell whether you need a bot</h2>
<p>Count how many times a week you or your staff do the same action in the same way. If it can be described as "when this happens, do that", it can be handed to a bot. Start with one such action.</p>
""",
    },
    "mvp-prilozheniya": {
        "slug": "app-mvp",
        "title": "An app MVP: what it is and how to build the first version",
        "short": "An app MVP: what it is and how to build the first version",
        "description": "What a mobile app MVP is, how it differs from a prototype and what to put into it. With the FitTimer and Argyns apps as examples.",
        "lead": "An MVP is the first working version of an app with only the essentials in it. It is built to test an idea on real people before serious money is spent.",
        "body": """
<h2>What an MVP is</h2>
<p>MVP stands for minimum viable product. Such an app solves one user task from start to finish and does nothing else.</p>
<p>Until someone has used the app, every decision about it is a guess. An MVP quickly shows which guesses were right.</p>

<h2>How an MVP differs from a prototype</h2>
<p>A prototype shows what the app will look like and how a person moves through its screens. It is built quickly and shown to a few people, and the data in it is usually fake.</p>
<p>An MVP can already be installed and used every day, and it stores real data.</p>
<p>A prototype tests whether the app is clear. An MVP tests whether people need it. Usually the prototype comes first and the MVP follows.</p>

<h2>What to put into the first version</h2>
<p>Write down in one sentence what a person must be able to do in the app. Everything that action cannot happen without goes into the MVP. The rest waits for later versions.</p>
<p>Take our workout timer, FitTimer. Its main action is starting an interval workout in a few seconds. So the first screen has three wheels for work time, rest time and the number of rounds. The app has no sign-up, because sign-up does nothing to help start a timer.</p>
<p>First versions often get social login, profile settings and statistics added "for later". Each of those pushes back the day the first users see the app.</p>

<h2>What to build it with</h2>
<p>We build apps with Flutter. One codebase runs on both iPhone and Android, so the app does not have to be written twice. This is especially handy for a first version, because changes after the first feedback are made once.</p>
<p>When an app needs a shared database, sign-up and notifications, we use Firebase. The Argyns app is built this way: it has a shared database, clan statistics and gathering announcements. It is available on the App Store and Google Play.</p>

<h2>How work on an MVP goes</h2>
<ol>
<li>Agree on the one action being tested.</li>
<li>Build a prototype of the screens, walk through it as a user and remove what is not needed.</li>
<li>Develop the path of the main action first, then everything else.</li>
<li>Test on devices with different screens, on weak internet and with the screen locked.</li>
<li>Publish. App stores review every version, and time has to be allowed for that.</li>
<li>Collect feedback and plan the next version from what users do.</li>
</ol>

<h2>When you do not need an MVP</h2>
<p>If a website, a bot or a spreadsheet solves the task, an app can be skipped. An app is needed when a person comes back to it often, gets notifications or works offline.</p>
""",
    },
    "interaktivnyj-sajt": {
        "slug": "interactive-website",
        "title": "Interactive websites: what they are, with examples",
        "short": "Interactive websites: what they are, with examples",
        "description": "What an interactive website is in plain words, what kinds there are and what they are built with. Four examples you can open and try.",
        "lead": "An interactive website responds to what a person does: to the mouse, a touch, a gesture or a sound. Here are examples that open from a link.",
        "body": """
<h2>What an interactive website is</h2>
<p>An ordinary site shows finished text and pictures. An interactive site reacts to the visitor: it calculates, draws or shows a result.</p>
<p>Every visitor gets a result of their own, which gives people a reason to share the site.</p>

<h2>Kinds of interactive websites</h2>
<ul>
<li>a web service that gathers data and gives a ready answer;</li>
<li>interactive graphics that the visitor controls;</li>
<li>a browser game that opens from a link with nothing to install;</li>
<li>a site with unusual navigation, where the way you move through it is part of the experience.</li>
</ul>

<h2>Four examples</h2>
<h3>Inkfall, ink in water</h3>
<p><a href="https://inkfall.voidstudio.top" target="_blank" rel="noopener">Inkfall</a> shows water with ink blooming through it. You can drive it with a mouse, several fingers at once, hand gestures in front of the camera and your voice through the microphone. The fluid motion is computed on the GPU from the equations of fluid dynamics, so the ink behaves believably. Inkfall has six modes, from heavy oil to light smoke. The camera image is processed on the device and never uploaded.</p>
<h3>Surf, a surf forecast</h3>
<p><a href="https://surf.voidstudio.top" target="_blank" rel="noopener">Surf</a> works as a web service. It gathers the wave, wind and tide forecast for Phuket's beaches from several weather models and turns it into one score from 0 to 10. There is no need to compare charts on several sites, because the answer is right there.</p>
<h3>Eyeball, a game for once a day</h3>
<p><a href="https://glazomer.voidstudio.top" target="_blank" rel="noopener">Eyeball</a> has five tasks done by eye. For example, you stop a timer blind, find the centre of a circle and set an angle. The tasks are new every day and the same for everyone, so you can compare results with friends. The game has no server, and progress is kept in the browser.</p>
<h3>The strip of work on our home page</h3>
<p>The <a href="/en/">Void Studio</a> home page shows work as a strip you drag with a mouse or a finger. The strip is drawn on the GPU. If a device cannot do that, ordinary images are shown.</p>

<h2>What interactive websites are built with</h2>
<ul>
<li>WebGL draws on the GPU right in the browser. It is needed for complex graphics and physics.</li>
<li>SVG and Canvas suit simpler graphics such as diagrams, charts and small games.</li>
<li>The camera and microphone let visitors control a site with gestures and sound, if they allow access.</li>
<li>Open data gives a site weather, maps, exchange rates and timetables.</li>
</ul>
<p>Nothing has to be installed. Everything opens from a link on a phone and on a computer.</p>

<h2>What to think about in advance</h2>
<ul>
<li>The site has to open quickly on a phone with a slow connection.</li>
<li>On an old device the graphics may not start, so a simple fallback version is needed.</li>
<li>A visitor should understand within a few seconds what can be done here.</li>
<li>A search engine cannot see what is drawn, so the essentials have to be repeated as ordinary text.</li>
</ul>

<h2>When interactivity is the right choice</h2>
<p>Interactivity is worth it when it helps people understand a product or get an answer faster than text would. If the site only has to give an address and prices, an ordinary page is enough.</p>
""",
    },
}
