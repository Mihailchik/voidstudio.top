"""Английские версии статей блога. Ключ — адрес русской статьи из build_blog.py.

Перевод держим рядом с оригиналом по смыслу: поменялась русская статья —
поправить и здесь, потом заново запустить tools/build_blog.py.
"""

ARTICLES_EN = {
    "avtoposting-v-socseti": {
        "slug": "scheduled-social-posting",
        "title": "Scheduled social posting: publishing to Telegram, Instagram and YouTube without manual work",
        "short": "Scheduled social posting without manual work",
        "seo_title": "Scheduled social posting: Telegram, Instagram, YouTube",
        "description": "What scheduled posting is, when an off-the-shelf tool is enough and when you need your own system. Explained through Poster 2.0, which runs Void Studio's publishing.",
        "lead": "The same piece of content has to be prepared separately for every platform: its own image size, its own caption length, its own time slot. Here is how we removed that work for ourselves.",
        "body": """
<h2>What scheduled posting is</h2>
<p>Scheduled posting means a post goes out by itself, at a set time, with nobody at the screen. You prepare the content once and a system sends it to Telegram, Instagram, YouTube and other platforms on a schedule.</p>
<p>The slow part is not the sending but the preparation. Every platform has its own format requirements, so one release turns into several different files and captions.</p>

<h2>An off-the-shelf tool or your own system</h2>
<p>A ready-made scheduling tool is enough if you run one or two platforms and publish the content as it is. It solves the main problem: the post goes out on time.</p>
<p>Your own system makes sense when at least one of these is true:</p>
<ul>
<li>content has to be reworked for each platform, not just copied;</li>
<li>images are built from a template out of text and a background;</li>
<li>there are several projects, each with its own schedule and accounts;</li>
<li>a person has to approve a post before it goes out;</li>
<li>you need to know what went out, what did not, and why.</li>
</ul>

<h2>How our Poster 2.0 works</h2>
<p>We built such a system for ourselves. It runs Void Studio's publishing and works in three steps that do not depend on each other.</p>
<h3>1. Content</h3>
<p>An idea, a text and source media go into the system. Every project has a profile: topic, language, tone, platforms and schedule. That is why a new project can be added without changing code.</p>
<h3>2. Formats</h3>
<p>From one release the system builds images and video in the right sizes for every platform, with captions. This step runs on templates and without AI, so the result is predictable. The files then go through an automatic check.</p>
<h3>3. Publishing</h3>
<p>The finished release takes its slot in the schedule. An admin gets a preview in advance and presses OK or Reject. Nothing goes out without a person's approval. At the set time the system checks the files once more, publishes and records the result.</p>

<h2>What this gives you</h2>
<ul>
<li>A release is prepared once, not separately for each platform.</li>
<li>Posts go out on schedule even when everyone is busy with something else.</li>
<li>A broken file is found before publishing, not after.</li>
<li>For every release you can see where it went out and with what result.</li>
</ul>

<h2>Where to start</h2>
<p>Write down what you do by hand for every post: which sizes you prepare, where and when you send them, who checks. The steps that repeat without change can be handed to a system first. Usually that is preparing sizes and sending on a schedule.</p>
""",
    },
    "telegram-bot-dlya-biznesa": {
        "slug": "telegram-bot-for-business",
        "title": "A Telegram bot for business: what it can do and what the cost depends on",
        "short": "A Telegram bot for business: what it can do and what the cost depends on",
        "seo_title": "Telegram bot for business: features and cost",
        "description": "Which tasks a Telegram bot solves, how it is built inside and what makes up the cost of building and running one. With an example of a working bot.",
        "lead": "A Telegram bot is a program that answers people and does work on a schedule. Here is which tasks are worth handing to it and what affects the price.",
        "body": """
<h2>What a Telegram bot can do</h2>
<p>A bot does two things: it replies to messages and it works by itself on a schedule. Typical tasks come from that:</p>
<ul>
<li>take a request or a booking and pass it to a member of staff;</li>
<li>answer frequent questions without an operator;</li>
<li>watch sources and send new items to a channel;</li>
<li>process a file: download it, convert it, send it out;</li>
<li>send a reminder, build a report, post a daily summary.</li>
</ul>
<p>A bot fits where an action repeats the same way many times. Where a live conversation and a judgement call are needed, it only takes the request and hands it to a person.</p>

<h2>An example: a bot that gathers podcasts</h2>
<p>Our Podcast Bot works with nobody involved. It watches RSS feeds, YouTube channels and playlists, and Telegram channels. When a new episode comes out, the bot goes through several steps:</p>
<ol>
<li>downloads the episode;</li>
<li>converts the audio to MP3;</li>
<li>prepares two versions, normal and double speed;</li>
<li>splits files that are too large into parts;</li>
<li>sends everything to a channel and deletes temporary files.</li>
</ol>
<p>Sources are checked on a schedule. You can also send the bot a link and it will queue it for processing. The state of every episode is written to a database, so the bot always knows what has been sent and what is still waiting.</p>

<h2>What a bot is made of</h2>
<ul>
<li><strong>The bot's code.</strong> We write in Python with the aiogram library.</li>
<li><strong>A database.</strong> It keeps what has been done and what is in the queue. SQLite is enough for small bots.</li>
<li><strong>A server.</strong> A bot has to run around the clock, so it needs a server. We run bots in Docker so they are easy to move and restart.</li>
<li><strong>External services.</strong> Payments, spreadsheets, a CRM or an AI model, if the bot is connected to them.</li>
</ul>

<h2>What the cost depends on</h2>
<p>The price of development depends not on the word "bot" but on how many scenarios it has and how many other systems it talks to. It is affected by:</p>
<ul>
<li><strong>The number of scenarios.</strong> Answering three questions and walking a person through a booking with a choice of time are different amounts of work.</li>
<li><strong>Integrations.</strong> Every connection to payments, a CRM or a spreadsheet is a separate task with its own checks.</li>
<li><strong>Working with files.</strong> Audio, video and large files need processing and server space.</li>
<li><strong>An admin panel.</strong> Whether texts and settings must be editable without a developer.</li>
<li><strong>Load.</strong> A bot for a hundred people and a bot for a hundred thousand are built differently.</li>
</ul>
<p>After launch there are running costs: a server and maintenance. The platforms a bot works with change their rules over time, and the code has to be updated.</p>

<h2>How to tell whether you need a bot</h2>
<p>Count how many times a week you or your staff do the same action in the same way. If it can be described as "when this happens, do that", it can be handed to a bot. It is better to start with one such action, not with all of them at once.</p>
""",
    },
    "mvp-prilozheniya": {
        "slug": "app-mvp",
        "title": "An app MVP: what it is and how to build the first version",
        "short": "An app MVP: what it is and how to build the first version",
        "description": "What a mobile app MVP is, how it differs from a prototype and what to put into it. With the FitTimer and Argyns apps as examples.",
        "lead": "An MVP is the first working version of an app with only the essentials in it. It exists to test an idea on real people before serious money is spent.",
        "body": """
<h2>What an MVP is</h2>
<p>MVP stands for minimum viable product. It is an app that already solves one user task from start to finish and does nothing beyond that.</p>
<p>The point is testing. Until someone has used the app, every decision about it is a guess. An MVP quickly shows which guesses were right.</p>

<h2>How an MVP differs from a prototype</h2>
<ul>
<li><strong>A prototype</strong> shows what the app will look like and how a person moves through its screens. It is built quickly and shown to a few people. The data in it is usually fake.</li>
<li><strong>An MVP</strong> is a real app. It can be installed and used every day, and it stores real data.</li>
</ul>
<p>A prototype answers "is this clear". An MVP answers "is this needed". Usually the prototype comes first and the MVP follows.</p>

<h2>What to put into the first version</h2>
<p>Write down in one sentence what a person must be able to do in the app. Everything that action cannot happen without goes into the MVP. The rest waits for later versions.</p>
<p>Our workout timer, FitTimer, is an example. Its main action is starting an interval workout in a few seconds. So the first screen is three wheels: work, rest, rounds. The app has no sign-up at all, because it does nothing to help start a timer.</p>
<p>A common mistake is adding social login, profile settings and statistics to the first version "for later". Each of those pushes back the day the first users see the app.</p>

<h2>What to build it with</h2>
<p>We build apps with Flutter. One codebase runs on both iPhone and Android, so the app does not have to be written twice. That matters most for a first version: changes after the first feedback are made once.</p>
<p>When an app needs a shared database, sign-up and notifications, we use Firebase. The Argyns app is built this way: it has a shared database, clan statistics and gathering announcements. It is available on the App Store and Google Play.</p>

<h2>How work on an MVP goes</h2>
<ol>
<li><strong>One main action.</strong> Agree on what exactly is being tested.</li>
<li><strong>A prototype of the screens.</strong> Walk through it as a user and remove what is not needed.</li>
<li><strong>Development.</strong> The path of the main action first, everything around it after.</li>
<li><strong>Testing on devices.</strong> Different screen sizes, weak internet, a locked screen.</li>
<li><strong>Publishing.</strong> App stores review every version, and time has to be allowed for that.</li>
<li><strong>Feedback and the next version.</strong> From here the app grows from what real users do.</li>
</ol>

<h2>When you do not need an MVP</h2>
<p>If a website, a bot or a spreadsheet solves the task, an app can be skipped. An app is justified when a person needs to come back to it often, get notifications or work offline.</p>
""",
    },
    "interaktivnyj-sajt": {
        "slug": "interactive-website",
        "title": "Interactive websites: what they are, with examples",
        "short": "Interactive websites: what they are, with examples",
        "description": "What an interactive website is in plain words, what kinds there are and what they are built with. Four examples you can open and try.",
        "lead": "An interactive website responds to what a person does: it changes with the mouse, a touch, a gesture or a sound. Here are examples that open from a link.",
        "body": """
<h2>What an interactive website is</h2>
<p>An ordinary site shows finished text and pictures. An interactive site does something in response: it calculates, draws, moves, gives a result. The person on it is a participant, not a reader.</p>
<p>A site like this gives people a reason to share it: everyone gets a result of their own.</p>

<h2>Kinds of interactive websites</h2>
<ul>
<li><strong>A web service.</strong> It gathers data and gives a ready answer to a question.</li>
<li><strong>Interactive graphics.</strong> An image the visitor controls.</li>
<li><strong>A browser game.</strong> It opens from a link with nothing to install.</li>
<li><strong>Unusual navigation.</strong> The way you move through the site becomes part of it.</li>
</ul>

<h2>Four examples</h2>
<h3>Inkfall: ink in water</h3>
<p><a href="https://inkfall.voidstudio.top" target="_blank" rel="noopener">Inkfall</a> is water with ink blooming through it. You can drive it with a mouse, several fingers at once, hand gestures in front of the camera and your voice through the microphone. The fluid motion is computed from real equations on the GPU, which is why the ink behaves as if it were alive. There are six modes, from heavy oil to light smoke. The camera image is processed on the device and never uploaded.</p>
<h3>Surf: is it worth going</h3>
<p><a href="https://surf.voidstudio.top" target="_blank" rel="noopener">Surf</a> is an example of a web service. It gathers the wave, wind and tide forecast for Phuket's beaches from several weather models and turns it into one score from 0 to 10. Instead of a dozen tabs with charts a person gets one answer.</p>
<h3>Eyeball: a game for once a day</h3>
<p><a href="https://glazomer.voidstudio.top" target="_blank" rel="noopener">Eyeball</a> is a browser game with five tasks done by eye: stop a timer blind, find the centre of a circle, set an angle. The tasks are new every day and the same for everyone, so you can compare results with friends. The game has no server; progress is kept in the browser.</p>
<h3>The strip of work on our home page</h3>
<p>The <a href="/en/">Void Studio</a> home page is a strip of images you drag with a mouse or a finger. It is drawn on the GPU, and where that is not supported ordinary images are shown.</p>

<h2>What interactive websites are built with</h2>
<ul>
<li><strong>WebGL</strong> — drawing on the GPU right in the browser. Needed for complex graphics and physics.</li>
<li><strong>SVG and Canvas</strong> — for simpler graphics: diagrams, charts, small games.</li>
<li><strong>Camera and microphone</strong> — a browser can recognise gestures and sound if the visitor allows it.</li>
<li><strong>Open data</strong> — weather, maps, exchange rates, timetables.</li>
</ul>
<p>Nothing has to be installed in any of these cases: everything opens from a link on a phone and on a computer.</p>

<h2>What to think about in advance</h2>
<ul>
<li><strong>Speed.</strong> The site has to open quickly on a phone with a slow connection.</li>
<li><strong>A fallback.</strong> On an old device the graphics may not start, and the person should still see a simple version.</li>
<li><strong>A clear start.</strong> A visitor should understand within a few seconds what can be done here.</li>
<li><strong>Text for search.</strong> A search engine cannot see what is drawn. The essentials have to be repeated as ordinary text.</li>
</ul>

<h2>When interactivity is the right choice</h2>
<p>It is justified when it helps people understand a product or get an answer faster than text would. If the job of the site is to give an address and prices, an ordinary page does it better.</p>
""",
    },
}
