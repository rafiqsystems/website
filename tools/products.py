#!/usr/bin/env python3
"""Generates public/products/<slug>/index.html and public/products/index.html.

Run from the repository root:  python3 tools/products.py
Edit the PRODUCTS list below, run the script, commit the generated pages. The pages are plain
static HTML: no scripts, no inline styles (the site's Content-Security-Policy forbids both).
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "public"

# slug, name, tag, one-line summary, lede, what it does, your data, status, works with (slugs)
PRODUCTS = [
    dict(slug="chat", name="Najwa", tag="Phase 1",
         summary="A private chatbot that runs on your own machine and tells you which model answered and where.",
         lede="A chatbot for your terminal first, then desktop and web. It talks to a model on your own computer by default and keeps your conversations and memory as files you can read.",
         does=["Chat from the command line, in one shot or interactively, with answers streamed as they arrive.",
               "A badge on every answer: which model ran, on which provider, and whether that was this device, your own network or a cloud service.",
               "Memory you control: one document you can read, edit and delete from, used at the start of each conversation.",
               "Consent in place: when a cloud model needs permission, you see exactly what would be sent and approve or decline on the spot.",
               "History and export as plain Markdown and JSON."],
         data="Conversations and memory stay on your device. Nothing reaches a cloud model unless you grant that specific flow, and every grant is listed in one place and can be withdrawn.",
         status="The command-line client exists and is tested against Qalb. Desktop and web follow in Phase 1. The repository opens publicly at the first installable milestone.",
         works=["core", "hub", "assistant"]),
    dict(slug="study", name="Hikma", tag="Phase 2",
         summary="Lessons become transcripts, flashcards and a tutor that cites its sources, with study plans and a clear view for parents.",
         lede="A study companion for any course, any school and any family. It turns lessons and documents into material to revise from, answers questions only from what was actually taught, and helps parents follow and plan their children's learning.",
         does=["Transcripts, summaries, glossaries, flashcards and quizzes from lecture recordings and course documents.",
               "A tutor that answers from your course material and cites the exact timestamp or page.",
               "Scanned and handwritten pages read with OCR.",
               "Pluggable engines for transcription, OCR, search and models, so a school can run everything on its own hardware or mix in cloud services it trusts.",
               "Built for more than one language from the start.",
               "For parents: each child's progress, what is due, and the topics that are not sticking yet, in one view.",
               "Study plans made for the child from the syllabus, the school calendar and the family calendar, adjusted when a week goes badly.",
               "Study guides and aids at the child's level: summaries, flashcards, practice quizzes, worked examples and audio recaps."],
         data="A school, a family or a student can host it themselves. Course material, notes and questions stay on that server unless a cloud provider is switched on, and each provider is a visible, revocable grant. A child sees exactly what a parent can see about them. There is no advertising, no profiling and nothing designed to hook a child.",
         status="Phase 2. The ingestion pipeline and its provider interfaces are built and tested, with local and cloud engines behind the same interface. The features for parents are designed, not yet built.",
         works=["core", "hub", "assistant", "tv"]),
    dict(slug="assistant", name="Najid", tag="Phase 3",
         summary="A personal assistant for your day, with a grant behind every data source.",
         lede="One page that tells you what today looks like: your calendar, what needs attention in your inbox, open tasks from your notes, and a few headlines. Every line says where it came from.",
         does=["A daily briefing, on request or on a schedule you set.",
               "Calendar, mail headers, notes and news through connectors that each declare what they read and where they send it.",
               "Scheduled runs only touch what you explicitly allowed to run unattended.",
               "Suggestions are text. Acting on one, such as moving an event or replying, is a separate permission.",
               "A missing permission produces a skipped section, never a nag."],
         data="Connectors contact only the hosts named on their consent card. Credentials live in the vault, never in the grant. Every call is written to an audit log you can read.",
         status="Phase 3. A reference briefing with file, calendar, mail and feed connectors works today against Qalb.",
         works=["core", "chat", "tv"]),
    dict(slug="mobile", name="Jawwal", tag="Phase 3",
         summary="Rafiq on your phone, with small models on the device and encrypted sync to your own Markaz.",
         lede="The companion on Android and iOS: chat, voice, your study material and your daily briefing, working without a cloud account.",
         does=["Chat and voice with a small model that runs on the phone.",
               "Your briefing, flashcards and lecture player on the go.",
               "End-to-end encrypted sync with your own Markaz."],
         data="The phone holds its own encrypted copy of your data. Sync passes through a relay that only ever sees ciphertext, and you can run that relay yourself.",
         status="Phase 3. Not started yet.",
         works=["core", "hub", "assistant", "study"]),
    dict(slug="lamha", name="Lamha", tag="In development",
         summary="A document viewer and editor for phone, tablet and desktop, with no network and no accounts.",
         lede="A touch-first way to read and mark up PDFs, images and notes, built once for Android, iOS, iPadOS, Linux, Windows and macOS.",
         does=["View PDFs and images, with search, page tools and form filling.",
               "Mark up with ink, shapes, highlights and text. Stylus pressure is supported.",
               "Notebooks with paper templates, a text and Markdown editor, and photo markup.",
               "Opens files through the system picker, the share sheet or \"open with\". It never scans your storage.",
               "Adapts to foldables, tablets and desktop windows."],
         data="Everything happens on the device. Export strips location data from images by default, and sharing goes through the system share sheet only. Optional sync to a self-hosted server, end-to-end encrypted, is planned.",
         status="In development. Viewing, markup, forms, notebooks and the editors are built. Encrypted sync and sharing come later.",
         works=["manzar", "hub"]),
    dict(slug="manzar", name="Manzar", tag="In development",
         summary="A video player for your own files, on the phone and on Android Auto, with no internet permission at all.",
         lede="Plays the videos you already have, from one folder you choose. The same queue continues on the car display.",
         does=["A library built from a single folder you pick with the system picker.",
               "Phone screen, lock-screen controls and the car display all drive one player, so switching between them never restarts playback.",
               "Single files also arrive through \"open with\"."],
         data="The app does not request the internet permission, so it cannot send anything anywhere. It asks for no storage permission either: it sees only the folder you chose.",
         status="In development for Android and Android Auto.",
         works=["lamha", "car"]),
    dict(slug="os", name="Nizam", tag="Phase 4",
         summary="An AI-first desktop: one command surface where you say what you want and agents do it, with every permission visible.",
         lede="A refreshed GNOME desktop whose front door is a single command palette. Type what you want in your own words, and Rafiq does it with the machine's own capabilities, inside limits you can see.",
         does=["One shortcut raises the palette: launch, find, arrange windows, change settings, or ask in plain language.",
               "Agents run multi-step work in a sandbox that contains only the files and network destinations you granted.",
               "The operating system's own functions, such as files, windows, clipboard, settings and notifications, are offered to agents as MCP servers under the same consent rules as any connector.",
               "A live panel shows what Rafiq can see right now, with revoke on every row.",
               "The classic desktop stays one toggle away."],
         data="A tool that lies about what it needs gains nothing: it runs with a filesystem that contains only the granted paths and a network that reaches only the granted hosts. Every decision is logged.",
         status="Phase 4. The Linux sandbox and the agent runtime are built and tested. The palette and the desktop image are designed, not yet built.",
         works=["core", "firewall", "assistant"]),
    dict(slug="firewall", name="Hisn", tag="Phase 4",
         summary="A next-generation firewall with on-device AI that explains itself, for your laptop, desktop and home.",
         lede="It learns what normal traffic looks like for each app and device, blocks the usual suspicious activity out of the box, and helps you write rules in plain language.",
         does=["Shows what is talking to whom, per app and per device.",
               "Blocks known-bad activity with curated, signed rule packs, and gives a reason for every block.",
               "Learns a baseline for each device and flags departures from it.",
               "Onboards a new device with one card: what it seems to be, what it tried to reach, and a sensible set of rules to approve, narrow or deny.",
               "Runs on a laptop or desktop first, then on the Markaz as the gateway for the whole home."],
         data="It records connection details such as addresses, names, sizes and timing. It never stores the contents of your traffic. The models run on your own hardware, and nothing is reported anywhere unless you opt in.",
         status="Phase 4. Designed, not yet built.",
         works=["core", "hub", "os"]),
    dict(slug="car", name="Qafila", tag="Later",
         summary="Cars that cooperate to avoid accidents and traffic, with no central map of who is where.",
         lede="Rafiq in each car. Cars that run it share hazards, intentions and congestion with one another, so each driver learns sooner what the cars ahead already know.",
         does=["Warnings about what you cannot see yet: a stopped vehicle around the bend, sudden braking ahead, a reported hazard.",
               "Route, departure and speed advice that keeps traffic flowing for everyone, not just one car.",
               "Suggestions at merges and junctions.",
               "Standard message formats, so it can interoperate with existing vehicle-to-vehicle systems."],
         data="What leaves the car is a small, signed, short-lived message you can read. Identities rotate every few minutes, shared knowledge travels as aggregates, and no party outside the car holds a record of where it has been.",
         status="Later, from the second half of 2028. Designed, not yet built. The first releases only advise the driver. Anything that influences steering, braking or acceleration waits for a safety case and a certified vehicle interface.",
         works=["core", "hub", "manzar"]),
    dict(slug="tv", name="Majlis", tag="Incubating",
         summary="A living-room front end for Android TV and Google TV, fed by the household's own server.",
         lede="One shared screen for the household: your own film and show library, your photos, and each person's day behind their own profile.",
         does=["Library and title pages with resume, trailers, cast, reviews and a parents' guide.",
               "Playback with high-quality video and surround sound passed straight to your equipment.",
               "Profiles opened with a short pattern on the remote, so a shared screen still keeps mail and calendars personal.",
               "Each person's day: a short brief, mail, calendar and messages.",
               "Photos: memories, albums, people and places from the household library."],
         data="Everything personal comes from the household's own server over the home network. Mail is shown without fetching anything from the internet, so a sender cannot tell that a message was opened. It plays what is already in your library and does not search for or download titles.",
         status="Incubating: it runs in one household today and is not yet a supported product. It has not been connected to Qalb yet.",
         works=["hub", "assistant"]),
    dict(slug="home", name="Dar", tag="Later",
         summary="Your home's own brain: devices, power, cameras and groceries, run in the house and connected to everything else Rafiq does.",
         lede="A home-automation hub that runs on your own server. Control the house in plain language, manage your power, keep an eye on the cameras and never run out of milk, without a vendor's cloud in the middle.",
         does=["Lights, heating, locks, sensors and appliances in one place, working with the smart devices you already own.",
               "Say what you want, or let Rafiq propose an automation and show you exactly what it would do before it runs.",
               "Power: solar, battery, grid and what is using what, with suggestions for when to run the heavy loads and a plan for outages.",
               "Cameras that record and detect inside the house. Footage is not uploaded anywhere.",
               "Groceries: what is running low, the shopping list, and what you can cook tonight.",
               "Part of the suite: cameras on the TV, the house in your morning briefing, new devices kept in check by Hisn, energy and grocery costs in your budget."],
         data="Everything runs on your Markaz. Unlocking a door, opening the garage or switching off an alarm always needs a person to confirm it, and can never be done by a schedule or an agent on its own. Face recognition is off unless you turn it on. Camera clips are encrypted, kept for days rather than months, and every viewing is logged.",
         status="Later, from 2029. Designed, not yet built.",
         works=["hub", "tv", "firewall", "finance"]),
    dict(slug="finance", name="Mizan", tag="Later",
         summary="All your accounts, cards and loans in one private ledger, with advice that knows your situation.",
         lede="See every account, transaction and loan in one place, kept on your own device. Then ask it things: where the money goes, how to reach a goal sooner, and whether a purchase is worth it right now.",
         does=["One ledger for bank accounts, cards, loans, recurring bills and net worth over time.",
               "Transactions sorted for you by a model that runs on your device and learns from your corrections.",
               "Budgets and goals with honest projections based on how you actually spend.",
               "A forecast that warns you before a shortfall, not after.",
               "Ask before you buy: a reasoned answer showing what a purchase does to this month and to your goals, the cost per use, and what waiting would change.",
               "A household view for shared bills, with each person's private accounts kept private."],
         data="Your finances stay on your device, encrypted. Connections to banks are read-only by design: Rafiq can see your accounts and can never move your money. You can run it entirely from files you import and never connect a bank. It explains and reasons from your own numbers; it is not regulated financial advice and does not sell you products.",
         status="Later, from 2029. Designed, not yet built.",
         works=["core", "assistant", "home", "mobile"]),
    dict(slug="core", name="Qalb", tag="Foundation",
         summary="The shared engine behind every Rafiq product: models, memory, permissions and an audit log.",
         lede="One service on your device that every Rafiq product talks to. It routes requests to models, stores your data encrypted, and decides what is allowed to leave.",
         does=["A model gateway that treats local and cloud models alike and labels every answer with the model and where it ran.",
               "A permission engine: every outbound connection needs a named grant, and anything that never leaves the device needs none.",
               "A tamper-evident audit log of every decision, which you can read and verify.",
               "An encrypted database per user, with keyword and semantic search.",
               "Memory as a versioned document you own, plus a one-command export of everything.",
               "A standard API, so existing tools that speak the common chat format work unchanged."],
         data="Qalb is where the promises are enforced. A request to a provider you have not granted is refused before anything is sent, and the refusal itself is logged.",
         status="Built and tested: gateway, permissions, consent flow, audit log, encrypted storage, memory, scheduling and the local API.",
         works=["hub", "chat", "assistant", "os"]),
    dict(slug="hub", name="Markaz", tag="Foundation",
         summary="Qalb as a one-command server for a household, a school or a team.",
         lede="A small server you run yourself. It packages Qalb with a local model server so everyone at home, or in a class, shares one private companion.",
         does=["One command to start, using Docker Compose.",
               "A local model server included, on CPU or on a graphics card.",
               "An optional larger database for many users.",
               "Reachable only from the machine it runs on until you choose to open it to your network."],
         data="Your Markaz, your data. No account with us is needed, and no secrets ship in the configuration.",
         status="A first version exists: the server, a choice of two model servers and an optional database. Multi-user schools and encrypted sync follow in Phase 2.",
         works=["core", "study", "mobile", "firewall"]),
]

# Three scenes per product: (tab label, caption, alt text). Pictures come from tools/art.py.
TOURS = {
 "chat": [
  [
   "Ask",
   "Ask in your own words. The answer streams in, and a badge says which model ran and that it stayed on your computer.",
   "A chat window with a question, a streamed answer, and badges reading: ran on this device, nothing left your computer."
  ],
  [
   "Decide",
   "Want a bigger cloud model? Rafiq shows exactly what would be sent and to whom, and waits. Nothing has left yet.",
   "A consent card listing what a cloud model would receive, with Allow and Not now buttons."
  ],
  [
   "Remember",
   "Memory is one document you own. Read it, edit a line, delete a line, export it.",
   "A plain text memory document with headings for About me, Preferences and Notes."
  ]
 ],
 "study": [
  [
   "Listen",
   "A lecture becomes a transcript you can search, with a summary, glossary and quiz beside it.",
   "A lecture video with a timeline and a transcript, one passage highlighted at 12:31."
  ],
  [
   "Revise",
   "Flashcards and quizzes are made from what was actually taught.",
   "A flashcard asking a question, with a Show answer button and progress dots."
  ],
  [
   "Ask",
   "The tutor answers only from your course material and shows where each answer came from.",
   "A tutor answer with two source labels: Lecture 4 at 12:31 and Notes page 18."
  ],
  [
   "For parents",
   "See each child's week at a glance, with a plan built around your family. Your child sees exactly what you see.",
   "A parent's view with two children's progress rings, upcoming tests, and a five-day study plan."
  ]
 ],
 "assistant": [
  [
   "Your day",
   "One page: calendar, mail that needs you, open tasks and a few headlines. Each section says where it came from.",
   "A briefing page with four panels: Calendar, Mail, Tasks and News, each with a source line."
  ],
  [
   "You decide",
   "Before a connector touches anything, a card lists what it reads, sends, writes and keeps, and when it may run.",
   "A consent card for a calendar connector listing reads, sends, writes, keeps and runs."
  ],
  [
   "While you sleep",
   "A scheduled briefing uses only what you allowed to run unattended. Everything else is skipped, and all of it is logged.",
   "A schedule set for 06:30 daily beside a log showing two sources allowed and two skipped."
  ]
 ],
 "mobile": [
  [
   "Ask anywhere",
   "A small model on the phone answers without a connection.",
   "A phone showing a short chat, with a label reading on this phone."
  ],
  [
   "Today",
   "Your briefing, mail that needs you, tasks and flashcards due, in one list.",
   "A phone showing a Today list with four items from calendar, mail, notes and study."
  ],
  [
   "Sync privately",
   "Your phone and your Markaz exchange only encrypted data. The relay in between cannot read it.",
   "A diagram: your phone, a relay that sees only ciphertext, and your Markaz at home, joined by locked arrows."
  ]
 ],
 "lamha": [
  [
   "Mark up",
   "Highlight, circle and write on any PDF or image with a finger, stylus or mouse.",
   "A document with a highlighted line, a hand-drawn circle and the note check this, beside page thumbnails."
  ],
  [
   "Write",
   "Notebooks with ruled, grid or plain paper. Pressure-sensitive ink for a stylus.",
   "A ruled notebook page with handwriting, a triangle sketch and a formula."
  ],
  [
   "Fill and share",
   "Fill in forms, sign, and share a copy with location data stripped out.",
   "A filled-in form with a signature, beside a share panel confirming location was removed."
  ]
 ],
 "manzar": [
  [
   "Your folder",
   "Pick one folder. That is the whole library. No account, no scanning.",
   "A phone showing a video library grid, with labels: no internet permission, no storage permission."
  ],
  [
   "Play",
   "A clean player for the videos you already have.",
   "A video player with a pause button, a progress bar and the title Coast trip."
  ],
  [
   "In the car",
   "The same queue continues on the car display. One player, so nothing restarts.",
   "A phone connected to a car display showing the same video, with an Up next list."
  ]
 ],
 "os": [
  [
   "Say it",
   "One shortcut raises the palette. Type a command or just say what you want done.",
   "A command palette with a typed request and four suggested actions, the first being Do it for me."
  ],
  [
   "Approve",
   "An agent does the steps and stops to ask before it touches a folder or reaches a server.",
   "A progress list with two finished steps, above a card asking permission to read, write and reach specific places."
  ],
  [
   "See everything",
   "A live panel lists what Rafiq can reach right now. Revoke any row. Everything else does not exist to it.",
   "A panel titled What Rafiq can see right now, with Files and Network rows that have Revoke buttons."
  ]
 ],
 "firewall": [
  [
   "Watch",
   "See which app is talking to which address, and what was stopped.",
   "Apps on the left connected to internet addresses on the right; two connections are crossed out as blocked."
  ],
  [
   "Onboard",
   "A new device joins. Rafiq works out what it is and proposes sensible rules for you to approve.",
   "A printer icon beside a card proposing two allow rules and two block rules."
  ],
  [
   "Understand",
   "Every block comes with a reason you can read, and a way to say it was you.",
   "A card explaining a blocked connection, with a chart showing one spike far above the usual range."
  ]
 ],
 "car": [
  [
   "Be warned",
   "Your car hears about a hazard from the cars ahead before you can see it. It advises; you drive.",
   "A car display warning Stopped vehicle ahead, 400 metres, with a suggested speed."
  ],
  [
   "Cars cooperate",
   "A stopped car tells the cars behind it, and they pass it on. Messages are signed, short-lived and go car to car.",
   "A road seen from above: a stopped car sends dotted signals back to three other cars."
  ],
  [
   "Flow together",
   "Route and departure advice is worked out in your car from what nearby cars shared, so traffic eases for everyone.",
   "A map with two routes; a card recommends leaving at 07:40 by the river road."
  ]
 ],
 "tv": [
  [
   "Who is watching",
   "A shared lock screen. Each person opens their profile with a short pattern on the remote.",
   "A television lock screen with the time, the weather and four profile circles."
  ],
  [
   "Watch",
   "Your own library with resume, trailers and details.",
   "A television showing two rows of posters: Continue watching and Recently added."
  ],
  [
   "Your day",
   "Behind your profile: a short brief, your mail and your calendar, from your own server.",
   "A television showing one person's brief, calendar and mail."
  ]
 ],
 "home": [
  [
   "Your home",
   "Every room and device on one screen. Type or say what you want.",
   "A home dashboard with eight tiles for rooms and devices, and a typed request to turn off the lights downstairs."
  ],
  [
   "Power",
   "Watch energy flow between solar, battery, grid and the house, and get a plan for outages.",
   "A diagram of power flowing from solar to the home and battery, with a suggestion to run the dishwasher at 13:00."
  ],
  [
   "Cameras and groceries",
   "Cameras that keep their footage at home, and a pantry that tells you what is running low.",
   "Four camera tiles, one showing a person detected, beside a grocery list with items running out."
  ]
 ],
 "finance": [
  [
   "Everything in one place",
   "Net worth, every account and loan, and where the money went.",
   "A finance overview with net worth, four accounts and a spending breakdown by category."
  ],
  [
   "Ask before you buy",
   "Describe a purchase and get a reasoned answer from your own numbers.",
   "A question about buying a laptop, answered with Wait about six weeks and four reasons."
  ],
  [
   "Plan ahead",
   "Goals with honest projections, bills coming up, and a ledger that can never move your money.",
   "Three goal progress bars, a list of upcoming bills, and a panel reading Read-only by design."
  ]
 ],
 "core": [
  [
   "One gate",
   "Every product goes through Qalb. A model on this device needs no permission; a cloud model needs your grant.",
   "Four products feed into Qalb, which connects freely to a local model and through a lock to a cloud model."
  ],
  [
   "Your grants",
   "Everything that may leave your device is on one list. Revoke any of it at any time.",
   "A list of grants with their status and Revoke buttons; one has expired."
  ],
  [
   "The record",
   "Every decision is logged, and each entry seals the one before it, so a missing or altered entry shows.",
   "Four linked log entries reading allow, deny, grant, allow, and a banner saying all 44 entries verified."
  ]
 ],
 "hub": [
  [
   "One command",
   "Start it and you have Qalb, a model server and a database running on your own machine.",
   "A terminal showing docker compose up and three services started."
  ],
  [
   "At home",
   "Laptops, phones, the TV and tablets all talk to one small server inside the house.",
   "A house outline with a Markaz in the middle connected to a laptop, phone, TV and tablet; a crossed-out cloud."
  ],
  [
   "For everyone",
   "One Markaz and one model shared by a household or a class, each person with their own memory and permissions.",
   "One Markaz connected to three people, each with their own lock."
  ]
 ]
}

# The plain word for what each product is, shown beside its name.
KIND = {'chat': 'Chat', 'study': 'Study', 'assistant': 'Assistant', 'mobile': 'Mobile', 'lamha': 'Documents', 'manzar': 'Video', 'os': 'Desktop', 'firewall': 'Firewall', 'car': 'Cooperative cars', 'tv': 'TV', 'home': 'Home', 'finance': 'Finance', 'core': 'Core', 'hub': 'Home server'}

BY_SLUG = {p["slug"]: p for p in PRODUCTS}
E = html.escape

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Rafiq</title><meta name="description" content="{desc}">
<link rel="stylesheet" href="/assets/site.css?v=20261124"><link rel="icon" href="/assets/favicon-32.png" sizes="32x32"><link rel="icon" href="/assets/icon-192.png" sizes="192x192"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:title" content="{title} | Rafiq"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://rafiqsystems.com/assets/social-card.png"><meta property="og:type" content="website"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b0b1f"></head><body><div class="wrap">
<header class="top"><a class="brand" href="/"><img src="/assets/icon-64.png" alt="" width="40" height="40">Rafiq</a>
<nav><a href="/products/">Products</a><a href="/principles/">Principles</a><a href="/roadmap/">Roadmap</a><a href="/security/">Security</a><a href="https://github.com/rafiqsystems">GitHub</a></nav></header>
"""

FOOT = """<footer><div class="cols"><div><strong>Rafiq Systems</strong><br>Privacy-first, open-source AI companions.<br>Code: AGPL-3.0 and Apache-2.0. Name and logo: <a href="/trademark/">trademark policy</a>.</div>
<div><a href="/products/">Products</a> · <a href="/principles/">Principles</a> · <a href="/roadmap/">Roadmap</a> · <a href="/security/">Security</a> · <a href="https://github.com/rafiqsystems">GitHub</a><br>
<a href="mailto:hello@rafiqsystems.com">hello@rafiqsystems.com</a></div></div>
<p class="fine">This site sets no cookies, loads nothing from third parties, and collects no analytics. It is static HTML with no JavaScript.</p></footer></div></body></html>
"""


def card(p):
    return ('<a class="card link shot" href="/products/{slug}/"><img src="/assets/products/{slug}-1.svg" alt="" width="960" height="600" loading="lazy">'
            '<span class="tag">{tag}</span><h3>{name}</h3><p>{summary}</p></a>'
            .format(slug=p["slug"], tag=E(KIND[p["slug"]] + " · " + p["tag"]), name=E(p["name"]), summary=E(p["summary"])))


def tour(steps, heading="See how it works"):
    """A click-through walkthrough built from radio buttons and CSS only. steps: (slug, n, tab, caption, alt)."""
    out = ['<section class="tour" aria-label="{}"><h2>{}</h2><p class="hint">Pick a step.</p>\n'.format(E(heading), E(heading))]
    for i in range(len(steps)):
        out.append('<input class="tour-r" type="radio" name="tour" id="s{0}"{1}>'.format(i + 1, " checked" if i == 0 else ""))
    out.append('\n<div class="tour-tabs">' + "".join('<label for="s{0}"><b>{0}</b>{1}</label>'.format(i + 1, E(st[2])) for i, st in enumerate(steps)) + "</div>\n")
    out.append('<div class="tour-stage">\n')
    for i, (slug, n, tab, cap, alt) in enumerate(steps):
        out.append('<figure class="tour-p p{0}"><img src="/assets/products/{1}-{2}.svg" alt="{3}" width="960" height="600"{4}><figcaption><strong>{5}.</strong> {6}</figcaption></figure>\n'
                   .format(i + 1, slug, n, E(alt, quote=True), "" if i == 0 else ' loading="lazy"', E(tab), E(cap)))
    out.append("</div></section>\n")
    return "".join(out)


def page(p):
    out = [HEAD.format(title=E(p["name"] + ": " + KIND[p["slug"]]), desc=E(p["summary"], quote=True))]
    out.append('<main class="prose product"><p class="crumbs"><a href="/products/">Products</a> / {}</p>\n'.format(E(p["name"])))
    out.append('<span class="tag">{}</span><h1>{}</h1><p class="lede">{}</p>\n'.format(E(KIND[p["slug"]] + " · " + p["tag"]), E(p["name"]), E(p["lede"])))
    out.append("</main>\n" + tour([(p["slug"], i + 1, t, c, a) for i, (t, c, a) in enumerate(TOURS[p["slug"]])]) + '<div class="prose">\n')
    out.append("<h2>What it does</h2>\n<ul>\n" + "".join("<li>{}</li>\n".format(E(d)) for d in p["does"]) + "</ul>\n")
    out.append("<h2>Your data</h2>\n<p>{}</p>\n".format(E(p["data"])))
    out.append('<h2>Status</h2>\n<p class="note">{}</p>\n'.format(E(p["status"])))
    out.append('<h2>Works with</h2>\n</div>\n<div class="grid related">\n' + "\n".join(card(BY_SLUG[s]) for s in p["works"]) + "\n</div>\n")
    out.append('<p class="back"><a href="/products/">All products</a> · <a href="/roadmap/">Roadmap</a> · <a href="/principles/">Principles</a></p>\n')
    out.append(FOOT)
    return "".join(out)


def index():
    out = [HEAD.format(title="Products", desc="Every Rafiq product: chat, study, assistant, apps, an AI-first desktop, a firewall, the home, your finances, cooperative cars, and the core they share.")]
    out.append('<main><div class="prose"><h1>Products</h1><p class="lede">Every product is a surface on one shared core, and each is held to the same principles: local by default, consent for every data flow, and data you can take with you.</p></div>\n')
    out.append('<div class="grid products">\n' + "\n".join(card(p) for p in PRODUCTS) + "\n</div>\n")
    out.append('<p class="back">Build order follows the <a href="/roadmap/">roadmap</a>.</p></main>\n')
    out.append(FOOT)
    return "".join(out)


def main():
    for p in PRODUCTS:
        for s in p["works"]:
            assert s in BY_SLUG, (p["slug"], s)
        assert len(TOURS[p["slug"]]) in (3, 4), p["slug"]
        d = ROOT / "products" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(p), encoding="utf-8")
    (ROOT / "products" / "index.html").write_text(index(), encoding="utf-8")
    print("wrote", len(PRODUCTS) + 1, "pages")


if __name__ == "__main__":
    main()
