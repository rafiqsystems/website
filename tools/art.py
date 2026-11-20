#!/usr/bin/env python3
"""Draws the product illustrations: public/assets/products/<slug>-<n>.svg (three or four scenes per product).

Run from the repository root:  python3 tools/art.py
Plain SVG with presentation attributes only: no scripts, no <style>, no external references, so the
site's Content-Security-Policy applies cleanly. Small SMIL animations (a blinking cursor, a pulse).
"""
import html
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "public" / "assets" / "products"
W, H = 960, 600
TEXT, MUTED, CYAN, VIOLET, PINK = "#e9e9f7", "#a6a6c8", "#4fd6ff", "#8b6cf6", "#ff6fc1"
GOOD, WARN, BAD = "#5be3a0", "#ffc857", "#ff6b7a"
PANEL, CARD, LINE, DEEP = "#12122e", "#1b1b4a", "#2f2f66", "#0b0b1f"
FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"


def esc(s):
    return html.escape(str(s), quote=True)


def T(x, y, s, size=16, fill=TEXT, w=400, anchor="start", font=FONT, op=1):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" opacity="{op}">{esc(s)}</text>'


def R(x, y, w, h, r=10, fill=CARD, stroke=None, sw=1, op=1, dash=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}{da} opacity="{op}"/>'


def C(cx, cy, r, fill, stroke=None, sw=1, op=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{st} opacity="{op}"/>'


def L(x1, y1, x2, y2, stroke=LINE, sw=2, dash=None, op=1):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{da} opacity="{op}"/>'


def P(d, stroke=CYAN, sw=3, fill="none", op=1, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"{da} opacity="{op}"/>'


def tw(s, size):
    return len(str(s)) * size * 0.56


def pill(x, y, s, color=CYAN, size=13, fill=None):
    w = tw(s, size) + 22
    return R(x, y, w, size + 13, (size + 13) / 2, fill or DEEP, color, 1.2) + T(x + 11, y + size + 3, s, size, color, 600), w


def pills(x, y, items, gap=8, size=13):
    out = ""
    for s, c in items:
        g, w = pill(x, y, s, c, size)
        out += g
        x += w + gap
    return out


def button(x, y, w, s, primary=False, color=None):
    if primary:
        return R(x, y, w, 38, 9, "url(#brand)") + T(x + w / 2, y + 25, s, 15, "#ffffff", 700, "middle")
    return R(x, y, w, 38, 9, CARD, color or LINE, 1.3) + T(x + w / 2, y + 25, s, 15, color or TEXT, 600, "middle")


def skeleton(x, y, widths, gap=18, h=8, fill=MUTED, op=.35):
    return "".join(R(x, y + i * gap, w, h, 4, fill, op=op) for i, w in enumerate(widths))


def cursor(x, y, h=18, color=CYAN):
    return f'<rect x="{x}" y="{y}" width="9" height="{h}" rx="2" fill="{color}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>'


def pulse(cx, cy, r, color):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="2">'
            f'<animate attributeName="r" values="{r};{r * 2.4}" dur="2s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>' + C(cx, cy, r, color))


def window(x, y, w, h, title=""):
    g = R(x + 6, y + 10, w, h, 16, "#000000", op=.35) + R(x, y, w, h, 16, PANEL, LINE, 1.5)
    g += L(x, y + 40, x + w, y + 40, LINE, 1.5) + C(x + 22, y + 20, 5, BAD) + C(x + 40, y + 20, 5, WARN) + C(x + 58, y + 20, 5, GOOD)
    return g + T(x + w / 2, y + 26, title, 14, MUTED, 600, "middle")


def phone(x, y, w=250, h=500):
    return R(x + 5, y + 9, w, h, 36, "#000000", op=.4) + R(x, y, w, h, 36, PANEL, LINE, 2) + R(x + w / 2 - 32, y + 12, 64, 8, 4, LINE)


def tv(x, y, w, h):
    return (R(x + 6, y + 10, w, h, 14, "#000000", op=.4) + R(x, y, w, h, 14, "#07071a", LINE, 3)
            + R(x + w / 2 - 70, y + h + 14, 140, 8, 4, LINE) + L(x + w / 2, y + h + 2, x + w / 2, y + h + 16, LINE, 6))


def bubble(x, y, w, lines, me=False, size=15):
    h = 20 + len(lines) * (size + 7)
    g = R(x, y, w, h, 14, "url(#brand)" if me else CARD, None if me else LINE, 1.2, op=.95 if me else 1)
    for i, s in enumerate(lines):
        g += T(x + 14, y + 26 + i * (size + 7), s, size, "#ffffff" if me else TEXT)
    return g, h


def row(x, y, w, left, right=None, color=TEXT, sub=None, rcolor=MUTED, h=44):
    g = R(x, y, w, h, 9, CARD, LINE, 1) + T(x + 14, y + (20 if sub else h / 2 + 5), left, 14.5, color, 600)
    if sub:
        g += T(x + 14, y + 36, sub, 12, MUTED)
    if right:
        g += T(x + w - 14, y + h / 2 + 5, right, 13, rcolor, 600, "end")
    return g


def consent(x, y, w, title, sub, rows, buttons):
    h = 96 + len(rows) * 40 + 62
    g = R(x + 6, y + 10, w, h, 16, "#000000", op=.45) + R(x, y, w, h, 16, "#16163c", VIOLET, 1.6)
    g += T(x + 24, y + 38, title, 19, TEXT, 700) + T(x + 24, y + 62, sub, 13.5, MUTED)
    yy = y + 86
    for label, text, color in rows:
        g += T(x + 24, yy + 16, label, 11.5, color, 700) + T(x + 104, yy + 16, text, 14.5, TEXT)
        g += L(x + 24, yy + 30, x + w - 24, yy + 30, LINE, 1)
        yy += 40
    bx = x + 24
    for s, kind in buttons:
        bw = tw(s, 15) + 36
        g += button(bx, yy + 12, bw, s, kind == "primary", None if kind != "danger" else BAD)
        bx += bw + 12
    return g


def arrow(x1, y1, x2, y2, color=CYAN, dash=None, sw=2.5):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 11 * math.cos(a), y2 - 11 * math.sin(a)
    p1 = (hx + 6 * math.sin(a), hy - 6 * math.cos(a))
    p2 = (hx - 6 * math.sin(a), hy + 6 * math.cos(a))
    return L(x1, y1, hx, hy, color, sw, dash) + f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>'


def node(x, y, w, h, s, color=CYAN, sub=None):
    g = R(x, y, w, h, 12, CARD, color, 1.6) + T(x + w / 2, y + (h / 2 - 2 if sub else h / 2 + 5), s, 15, TEXT, 700, "middle")
    if sub:
        g += T(x + w / 2, y + h / 2 + 17, sub, 12, MUTED, 400, "middle")
    return g


def backdrop(seed):
    # Soft glows and orbit arcs: the "art" behind every scene. Positions vary by scene.
    spots = [(170, 110, CYAN), (800, 480, PINK), (760, 120, VIOLET), (200, 500, VIOLET)]
    a, b = spots[seed % 4], spots[(seed + 1) % 4]
    g = f'<rect width="{W}" height="{H}" rx="22" fill="url(#bg)"/>'
    g += f'<circle cx="{a[0]}" cy="{a[1]}" r="300" fill="url(#g{seed % 4})"/><circle cx="{b[0]}" cy="{b[1]}" r="260" fill="url(#g{(seed + 1) % 4})"/>'
    g += f'<ellipse cx="{W / 2}" cy="{H / 2}" rx="{430 + seed % 3 * 12}" ry="{250 - seed % 3 * 14}" fill="none" stroke="{VIOLET}" stroke-width="1" opacity=".22" transform="rotate({-12 + seed % 5 * 6} {W / 2} {H / 2})"/>'
    g += f'<ellipse cx="{W / 2}" cy="{H / 2}" rx="{360}" ry="{300}" fill="none" stroke="{CYAN}" stroke-width="1" opacity=".14" transform="rotate({20 - seed % 4 * 9} {W / 2} {H / 2})"/>'
    return g


DEFS = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d0d26"/><stop offset="1" stop-color="#17123f"/></linearGradient>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".6" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="poster1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="poster2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PINK}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<linearGradient id="poster3" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#2b2b7a"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="poster4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WARN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<radialGradient id="g0"><stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<radialGradient id="g1"><stop offset="0" stop-color="{PINK}" stop-opacity=".2"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".28"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="g3"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".2"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
</defs>"""


def poster(x, y, w, h, n, label=None, progress=None):
    g = R(x, y, w, h, 10, f"url(#poster{n % 4 + 1})", op=.9) + C(x + w * .7, y + h * .3, w * .16, "#ffffff", op=.18)
    g += P(f"M{x} {y + h * .75} Q{x + w * .3} {y + h * .5} {x + w * .55} {y + h * .72} T{x + w} {y + h * .6} V{y + h} H{x} Z", "none", 0, DEEP, .35)
    if label:
        g += T(x + 4, y + h + 18, label, 12.5, MUTED)
    if progress is not None:
        g += R(x + 8, y + h - 12, w - 16, 4, 2, DEEP, op=.7) + R(x + 8, y + h - 12, (w - 16) * progress, 4, 2, CYAN)
    return g

# ---------------------------------------------------------------- scenes


def chat_1():
    g = window(110, 60, 740, 480, "rafiq chat")
    b, h = bubble(450, 124, 370, ["Summarise today's meeting notes", "in five bullet points."], True)
    g += b
    b, h2 = bubble(140, 124 + h + 22, 540, ["Here is the short version:", "• Budget approved for the spring term", "• Field trip moved to the 14th", "• New timetable goes out on Monday"])
    g += b + cursor(156, 124 + h + 22 + h2 - 4 + 10, 16)
    g += pills(140, 460, [("gemma-3-4b", CYAN), ("ran on this device", GOOD), ("nothing left your computer", MUTED)])
    return g


def chat_2():
    g = window(110, 60, 740, 480, "rafiq chat")
    b, h = bubble(430, 110, 390, ["Use the bigger cloud model for this one."], True)
    g += b + R(111, 101 + 60, 738, 378, 0, DEEP, op=.55)
    g += consent(230, 190, 500, "A cloud model wants to receive", "Nothing has been sent yet.",
                 [("SENDS", "this conversation to api.example-ai.com", PINK), ("KEEPS", "what that provider's policy says", WARN), ("RUNS", "only when you ask", GOOD)],
                 [("Allow", "primary"), ("Change what it sees", ""), ("Not now", "")])
    return g


def chat_3():
    g = window(170, 60, 620, 480, "memory.md")
    lines = [("# Rafiq memory", 20, TEXT, 700), ("## About me", 16, CYAN, 700), ("- I teach secondary maths", 15, TEXT, 400), ("- I live near the coast", 15, TEXT, 400),
             ("## Preferences", 16, CYAN, 700), ("- Short answers, metric units", 15, TEXT, 400), ("## Notes", 16, CYAN, 700), ("- Sam's birthday is 3 March", 15, TEXT, 400)]
    y = 140
    for s, size, col, w in lines:
        g += T(210, y, s, size, col, w, font=MONO)
        y += 40 if size > 15 else 32
    g += cursor(210 + len("- Sam's birthday is 3 March") * 15 * .6 + 8, y - 46, 17)
    g += pills(210, 478, [("version 7", VIOLET), ("yours to edit, export or delete", MUTED)])
    return g


def study_1():
    g = window(80, 60, 800, 480, "Lecture 4 · Derivatives")
    g += R(110, 124, 360, 210, 12, "url(#poster3)", op=.85) + C(290, 229, 34, DEEP, op=.6) + f'<polygon points="280,212 280,246 308,229" fill="{TEXT}"/>'
    g += R(110, 356, 360, 6, 3, LINE) + R(110, 356, 150, 6, 3, CYAN) + C(260, 359, 8, CYAN) + T(110, 386, "12:31", 13, CYAN, 600) + T(470, 386, "48:02", 13, MUTED, 400, "end")
    g += pills(110, 420, [("Transcript", CYAN), ("Summary", MUTED), ("Glossary", MUTED), ("Quiz", MUTED)])
    y = 130
    for ts, wds, hot in [("12:04", [300, 250], False), ("12:31", [310, 270, 180], True), ("13:10", [280, 300], False), ("13:42", [310, 160], False)]:
        hgt = 18 + len(wds) * 18
        if hot:
            g += R(500, y - 12, 350, hgt + 6, 9, CARD, CYAN, 1.4)
        g += T(514, y + 6, ts, 13, CYAN if hot else MUTED, 600) + skeleton(566, y - 2, [w * .85 for w in wds], op=.75 if hot else .35)
        y += hgt + 22
    return g


def study_2():
    g = R(232, 122, 500, 290, 20, "#000000", op=.35) + R(244, 110, 480, 290, 20, CARD, LINE, 1.5, op=.6) + R(226, 96, 508, 300, 20, "#16163c", VIOLET, 1.6)
    g += T(480, 150, "FLASHCARD 8 OF 24", 12, MUTED, 700, "middle") + T(480, 222, "What does the chain rule", 26, TEXT, 700, "middle") + T(480, 258, "let you differentiate?", 26, TEXT, 700, "middle")
    g += button(400, 316, 160, "Show answer", True)
    for i in range(12):
        g += C(326 + i * 28, 436, 5, CYAN if i < 8 else LINE)
    g += pills(350, 470, [("Again", BAD), ("Good", CYAN), ("Easy", GOOD)], 14, 15)
    return g


def study_3():
    g = window(110, 60, 740, 480, "Tutor · answers only from your course")
    b, h = bubble(400, 118, 420, ["Why is the derivative of sin x", "equal to cos x?"], True)
    g += b
    b, h2 = bubble(140, 118 + h + 22, 560, ["Your lecturer showed it from the limit definition:", "the slope of sin x at any point matches the", "height of cos x there. She drew both curves."])
    g += b
    y = 118 + h + 22 + h2 + 18
    g += T(140, y + 14, "From your material:", 13, MUTED) + pills(140, y + 26, [("Lecture 4 · 12:31", CYAN), ("Notes · page 18", VIOLET)])
    g += P("M560 470 q30 -60 60 0 t60 0 t60 0", CYAN, 2.5, op=.8) + P("M560 440 q30 60 60 0 t60 0 t60 0", PINK, 2.5, op=.8)
    return g


def assistant_1():
    g = window(80, 50, 800, 500, "Briefing · Friday")
    cards = [("Calendar", [("11:30  Dentist", "overlaps your 11:45 call", WARN), ("16:00  School pickup", None, TEXT)], "calendar · grant 1d35"),
             ("Mail", [("Sara: Budget draft", "needs a reply", CYAN), ("Invitation: Open day", None, TEXT)], "mail headers · grant 9c88"),
             ("Tasks", [("Call the plumber", None, TEXT), ("Book flights", None, TEXT)], "notes folder · on this device"),
             ("News", [("Council approves cycle lane", None, TEXT), ("Storm warning lifted", None, TEXT)], "3 feeds · grant c40e")]
    for i, (title, rows, src) in enumerate(cards):
        x, y = 104 + (i % 2) * 388, 106 + (i // 2) * 214
        g += R(x, y, 364, 196, 14, CARD, LINE, 1.2) + T(x + 18, y + 32, title, 17, TEXT, 700)
        yy = y + 60
        for s, sub, col in rows:
            g += C(x + 24, yy - 5, 4, col if col != TEXT else MUTED) + T(x + 38, yy, s, 14.5, TEXT, 600)
            if sub:
                g += T(x + 38, yy + 18, sub, 12, col)
            yy += 44 if sub else 30
        g += T(x + 18, y + 180, "source: " + src, 11.5, MUTED)
    return g


def assistant_2():
    g = pills(250, 70, [("Rafiq Assistant asks before it connects", MUTED)], size=14)
    g += consent(210, 112, 540, "Calendar · for your morning briefing", "This is everything it can do. Untick anything.",
                 [("READS", "events from cal.example.org", CYAN), ("SENDS", "your calendar login and the date range", PINK), ("WRITES", "nothing", MUTED),
                  ("KEEPS", "nothing between calls", GOOD), ("RUNS", "when you ask   ·   not on a schedule", WARN)],
                 [("Allow", "primary"), ("Change what it can see", ""), ("Not now", "")])
    return g


def assistant_3():
    g = R(90, 110, 300, 330, 16, "#16163c", VIOLET, 1.5) + T(116, 154, "Morning briefing", 19, TEXT, 700) + T(116, 180, "Every day at 06:30", 14.5, MUTED)
    g += R(116, 208, 62, 30, 15, GOOD, op=.9) + C(163, 223, 11, "#ffffff") + T(190, 229, "Scheduled", 14.5, TEXT, 600)
    g += T(116, 290, "While you are away it may use", 13, MUTED) + T(116, 310, "only what you ticked to run", 13, MUTED) + T(116, 330, "unattended.", 13, MUTED)
    g += pills(116, 370, [("2 of 4 sources allowed", WARN)])
    g += T(430, 128, "What ran this morning", 15, MUTED, 600)
    for i, (t, s, right, col) in enumerate([("06:30", "calendar · list events", "allowed", GOOD), ("06:30", "notes · search tasks", "allowed", GOOD),
                                           ("06:30", "mail · list headers", "skipped: not allowed unattended", WARN), ("06:30", "news · fetch", "skipped: not allowed unattended", WARN),
                                           ("06:31", "briefing saved, one notification", "", MUTED)]):
        g += row(430, 146 + i * 56, 440, f"{t}   {s}", right, TEXT, None, col)
    g += pills(430, 440, [("every line is in your audit log", MUTED)])
    return g


def mobile_1():
    g = phone(355, 50)
    b, h = bubble(425, 110, 160, ["Am I free at 4?"], True, 14)
    g += b
    b, h2 = bubble(375, 110 + h + 16, 200, ["Yes. Pickup is at", "16:00, so leave by", "15:40."], False, 14)
    g += b + pills(375, 110 + h + h2 + 30, [("on this phone", GOOD)], size=12)
    g += R(375, 486, 160, 40, 20, CARD, LINE, 1.2) + T(391, 511, "Ask Rafiq", 14, MUTED) + C(566, 506, 20, "url(#brand)") + R(562, 496, 8, 14, 4, "#ffffff") + P("M556 506 q10 12 20 0", "#ffffff", 2)
    g += pulse(190, 300, 9, CYAN) + T(190, 350, "small model", 14, MUTED, 600, "middle") + T(190, 370, "runs offline", 14, MUTED, 400, "middle")
    g += pills(690, 286, [("no cloud account", VIOLET)])
    return g


def mobile_2():
    g = phone(355, 50) + T(380, 104, "Today", 20, TEXT, 700)
    for i, (s, sub, col) in enumerate([("11:30  Dentist", "calendar", CYAN), ("Sara: Budget draft", "mail · needs a reply", PINK), ("Call the plumber", "notes", GOOD), ("Flashcards: 12 due", "study", VIOLET)]):
        y = 124 + i * 78
        g += R(375, y, 210, 66, 12, CARD, LINE, 1) + R(375, y, 5, 66, 2, col) + T(392, y + 28, s, 14, TEXT, 600) + T(392, y + 48, sub, 11.5, MUTED)
    g += pills(388, 470, [("synced from your Markaz", MUTED)], size=12)
    return g


def mobile_3():
    g = phone(110, 150, 170, 320) + T(195, 300, "your", 15, MUTED, 400, "middle") + T(195, 322, "phone", 17, TEXT, 700, "middle")
    g += node(410, 250, 150, 110, "relay", VIOLET, "sees only ciphertext")
    g += R(690, 230, 170, 150, 14, CARD, CYAN, 1.6) + T(775, 296, "your Markaz", 17, TEXT, 700, "middle") + T(775, 320, "at home", 13, MUTED, 400, "middle")
    for y in (350, 362):
        g += C(712, y, 3, GOOD) + R(722, y - 2, 110, 4, 2, LINE)
    g += arrow(290, 305, 402, 305, CYAN) + arrow(568, 305, 682, 305, CYAN)
    for x in (345, 625):
        g += R(x - 12, 268, 24, 20, 5, DEEP, GOOD, 1.6) + P(f"M{x - 6} 268 v-6 a6 6 0 0 1 12 0 v6", GOOD, 1.8)
    g += T(480, 440, "encrypted on the phone, decrypted only on your devices", 14.5, MUTED, 400, "middle")
    g += pills(376, 120, [("you can run the relay yourself", GOOD)])
    return g


def lamha_1():
    g = window(90, 50, 780, 500, "Lamha · contract.pdf")
    for i, col in enumerate([CYAN, PINK, WARN, GOOD, MUTED]):
        g += R(108, 112 + i * 54, 42, 42, 10, CARD, LINE, 1) + C(129, 133 + i * 54, 8, col)
    g += R(190, 108, 430, 420, 6, "#f3f1ea") + T(220, 150, "Service agreement", 20, "#22223a", 700)
    g += skeleton(220, 176, [370, 350, 372, 300], 20, 7, "#4a4a66", .5) + R(216, 252, 300, 20, 3, WARN, op=.55)
    g += skeleton(220, 258, [290, 372, 340, 360, 220], 20, 7, "#4a4a66", .5)
    g += P("M430 372 q40 -34 96 -8 q28 14 -6 30 q-60 22 -96 -4 q-14 -10 6 -18", PINK, 3.5) + T(540, 420, "check this", 15, PINK, 700, font="'Comic Sans MS', 'Segoe Print', cursive")
    g += skeleton(220, 440, [372, 330, 180], 20, 7, "#4a4a66", .5)
    g += T(650, 136, "Pages", 13, MUTED, 600)
    for i in range(3):
        g += R(650, 150 + i * 118, 82, 104, 5, "#f3f1ea", CYAN if i == 0 else LINE, 2 if i == 0 else 1, op=1 if i == 0 else .7) + skeleton(660, 164 + i * 118, [60, 54, 62, 40], 14, 4, "#4a4a66", .5)
    g += pills(750, 150, [("ink", PINK)], size=12) + pills(750, 186, [("highlight", WARN)], size=12) + pills(750, 222, [("text", CYAN)], size=12)
    return g


def lamha_2():
    g = window(120, 50, 720, 500, "Lamha · Notebook")
    g += R(150, 106, 660, 424, 6, "#f3f1ea")
    for i in range(12):
        g += L(170, 148 + i * 32, 790, 148 + i * 32, "#c9c5b5", 1)
    g += L(214, 110, 214, 526, "#e7a3a3", 1.5)
    g += P("M236 140 q10 -22 20 0 t20 0 M290 140 q4 -26 14 -2 q8 14 -8 4 M326 140 v-24 M344 140 q-10 -18 6 -20 q16 2 2 20 M374 140 q0 -22 14 -14", "#26267a", 3)
    g += P("M236 204 q12 -26 22 -2 t22 0 t22 0 M320 204 q0 -30 12 -4 M350 204 q-14 -16 4 -22 q14 6 0 22 M380 204 v-22 q10 -6 16 4 v18", "#26267a", 2.6)
    g += P("M470 420 L560 250 L650 420 Z", "#2d6cdf", 3) + P("M560 250 V420", "#2d6cdf", 2, dash="6 6") + T(566, 344, "h", 20, "#2d6cdf", 700, font="Georgia, serif") + T(548, 446, "b", 20, "#2d6cdf", 700, font="Georgia, serif")
    g += P("M236 300 q40 -30 90 -6 q40 20 90 -10", PINK, 6, op=.8) + P("M236 330 q40 -30 90 -6", PINK, 2.5, op=.8)
    g += T(240, 400, "A = ½ b h", 30, "#26267a", 700, font="Georgia, serif")
    g += pills(590, 122, [("stylus pressure", PINK), ("grid · ruled · plain", MUTED)], size=12)
    return g


def lamha_3():
    g = window(90, 60, 470, 480, "Lamha · form.pdf") + R(116, 118, 418, 400, 6, "#f3f1ea")
    for i, (label, val) in enumerate([("Full name", "Sam Rivera"), ("Date", "14 March"), ("Reference", "A-2291")]):
        y = 150 + i * 78
        g += T(140, y, label, 12.5, "#4a4a66", 600) + R(140, y + 10, 370, 36, 5, "#ffffff", "#8b8bb0", 1.2) + T(152, y + 34, val, 15.5, "#1c1c5c", 600)
    g += R(140, 392, 20, 20, 4, "#ffffff", "#8b8bb0", 1.2) + P("M144 402 l5 6 l9 -12", "#1c1c5c", 2.6) + T(170, 408, "I agree to the terms", 14, "#22223a")
    g += P("M300 486 q16 -34 30 -6 q10 18 22 -14 q10 -20 20 8 q8 16 40 0", "#1c1c5c", 2.6) + L(280, 496, 500, 496, "#8b8bb0", 1)
    g += R(600, 150, 280, 300, 16, "#16163c", VIOLET, 1.5) + T(624, 192, "Share a copy", 19, TEXT, 700)
    for i, (s, col) in enumerate([("Location removed from photos", GOOD), ("Your markup flattened in", GOOD), ("Sent via the share sheet", GOOD)]):
        g += C(634, 232 + i * 44, 9, DEEP, col, 1.6) + P(f"M629 {232 + i * 44} l4 4 l7 -8", col, 2) + T(654, 237 + i * 44, s, 13.5, TEXT)
    g += button(624, 380, 232, "Export", True)
    return g


def manzar_1():
    g = phone(355, 50) + T(380, 104, "Library", 20, TEXT, 700) + T(380, 124, "Videos · one folder you chose", 11.5, MUTED)
    names = ["Coast trip", "Recital", "Lecture 4", "Wedding", "Hike", "Cooking"]
    for i in range(6):
        g += poster(378 + (i % 2) * 106, 144 + (i // 2) * 120, 96, 78, i, names[i], .4 if i == 0 else None)
    g += pills(120, 286, [("no internet permission", GOOD)]) + pills(650, 286, [("no storage permission", GOOD)])
    return g


def manzar_2():
    g = window(100, 70, 760, 460, "Manzar")
    g += R(126, 126, 708, 318, 10, "url(#poster3)", op=.9) + P("M126 380 Q300 280 480 370 T834 330 V444 H126 Z", "none", 0, DEEP, .45) + C(700, 200, 44, "#ffffff", op=.2)
    g += C(480, 285, 40, DEEP, op=.65) + R(466, 267, 9, 36, 3, TEXT) + R(485, 267, 9, 36, 3, TEXT)
    g += R(126, 470, 708, 6, 3, LINE) + R(126, 470, 190, 6, 3, CYAN) + C(316, 473, 8, CYAN)
    g += T(126, 508, "Coast trip", 16, TEXT, 700) + T(834, 508, "12:40 / 48:02", 14, MUTED, 400, "end")
    return g


def manzar_3():
    g = phone(80, 170, 150, 290) + R(98, 214, 114, 70, 8, "url(#poster3)", op=.9) + T(155, 310, "Coast trip", 13, TEXT, 700, "middle") + R(104, 326, 102, 4, 2, LINE) + R(104, 326, 40, 4, 2, CYAN)
    g += R(338, 146, 560, 320, 26, "#000000", op=.4) + R(330, 136, 560, 320, 26, "#07071a", LINE, 3)
    g += R(356, 166, 230, 150, 12, "url(#poster3)", op=.9) + T(356, 346, "Coast trip", 19, TEXT, 700) + T(356, 370, "12:40 of 48:02", 13.5, MUTED)
    g += R(356, 392, 230, 6, 3, LINE) + R(356, 392, 86, 6, 3, CYAN)
    g += T(616, 186, "Up next", 13, MUTED, 600)
    for i, s in enumerate(["Recital", "Hike", "Cooking"]):
        g += row(616, 200 + i * 54, 250, s, None, TEXT)
    g += C(616 + 28, 408, 22, CARD, LINE, 1.3) + C(616 + 92, 408, 26, "url(#brand)") + C(616 + 156, 408, 22, CARD, LINE, 1.3)
    g += R(699, 398, 6, 20, 2, "#ffffff") + R(711, 398, 6, 20, 2, "#ffffff")
    g += arrow(238, 315, 322, 300, CYAN, "6 6") + T(280, 270, "one player", 13, CYAN, 600, "middle")
    g += pills(520, 94, [("on the car display", VIOLET)])
    return g


def os_palette(extra, h):
    g = R(0, 0, W, 34, 0, DEEP, op=.55) + T(24, 23, "Nizam", 13, MUTED, 700) + T(W - 24, 23, "Fri 09:41", 13, MUTED, 400, "end")
    g += C(W - 232, 18, 5, GOOD) + T(W - 220, 23, "2 grants live", 12.5, GOOD, 600)
    g += R(176, 96, 620, h, 18, "#000000", op=.4) + R(170, 86, 620, h, 18, "#14143a", VIOLET, 1.6)
    return g + extra


def os_1():
    q = "move the budget sheet to Finance and"
    e = C(204, 124, 9, "url(#brand)") + T(226, 122, q, 17, TEXT, 600) + T(226, 146, "email Sara a summary", 17, TEXT, 600) + cursor(226 + tw("email Sara a summary", 17) + 6, 131, 18)
    e += L(170, 166, 790, 166, LINE, 1.2)
    for i, (s, sub, col) in enumerate([("Do it for me", "an agent plans the steps, you approve what it touches", CYAN), ("Move budget.xlsx to Finance", "Files", MUTED), ("New message to Sara", "Mail", MUTED), ("Search the web for it", "Browser", MUTED)]):
        y = 180 + i * 62
        e += R(186, y, 588, 52, 10, CARD if i == 0 else "#14143a", CYAN if i == 0 else None, 1.4) + T(206, y + 23, s, 15.5, TEXT, 700 if i == 0 else 500) + T(206, y + 42, sub, 12, col if i == 0 else MUTED)
    e += pills(186, 440, [("Enter  run", MUTED), ("Tab  refine", MUTED), ("Esc  close", MUTED)], size=12)
    return os_palette(e, 400)


def os_2():
    e = T(196, 124, "Working on it", 17, TEXT, 700)
    for i, (s, col) in enumerate([("Found budget.xlsx in Downloads", GOOD), ("Wrote a five-line summary", GOOD)]):
        e += C(206, 154 + i * 30, 8, DEEP, col, 1.6) + P(f"M201 {154 + i * 30} l4 4 l7 -8", col, 2) + T(224, 159 + i * 30, s, 14.5, TEXT)
    e += pulse(206, 214, 6, WARN) + T(224, 219, "Needs your say before it continues", 14.5, WARN, 600)
    e = os_palette(e, 150)
    e += consent(220, 252, 520, "Rafiq wants to", "For this task only.",
                 [("READ", "~/Documents/Finance", CYAN), ("WRITE", "~/Documents/Finance/budget.xlsx", PINK), ("REACH", "mail.example.org", WARN)],
                 [("Allow once", "primary"), ("Always for this", ""), ("Deny", "danger")])
    return e


def os_3():
    e = T(196, 126, "What Rafiq can see right now", 18, TEXT, 700) + T(196, 150, "Everything else on this computer does not exist to it.", 13, MUTED)
    rows = [("Files", "~/Documents/Finance · read and write", "Revoke", BAD), ("Network", "mail.example.org only", "Revoke", BAD), ("Clipboard", "nothing", "", MUTED), ("Camera, microphone", "nothing", "", MUTED)]
    for i, (a, b, r, col) in enumerate(rows):
        e += row(190, 172 + i * 62, 580, a, r, TEXT, b, col, 52)
    e += pills(190, 430, [("sandboxed", GOOD), ("ends when the task ends", MUTED), ("every step logged", MUTED)], size=12)
    return os_palette(e, 392)


def firewall_1():
    g = T(80, 76, "Right now on this laptop", 18, TEXT, 700) + pills(560, 56, [("214 allowed", GOOD), ("3 blocked", BAD)])
    apps = [("Browser", 140), ("Mail", 230), ("Updater", 320), ("Unknown app", 410)]
    dests = [("news.example.org", 120, GOOD), ("mail.example.org", 200, GOOD), ("updates.vendor.com", 280, GOOD), ("ads.tracker.net", 360, BAD), ("203.0.113.9", 440, BAD)]
    links = [(0, 0, GOOD), (0, 3, BAD), (1, 1, GOOD), (2, 2, GOOD), (3, 4, BAD)]
    for a, d, col in links:
        y1, y2 = apps[a][1] + 24, dests[d][1] + 22
        g += P(f"M300 {y1} C440 {y1} 480 {y2} 600 {y2}", col, 2.4, op=.85, dash=None if col == GOOD else "7 6")
        if col == BAD:
            g += C(450, (y1 + y2) / 2, 12, DEEP, BAD, 2) + L(444, (y1 + y2) / 2 - 6, 456, (y1 + y2) / 2 + 6, BAD, 2.4) + L(456, (y1 + y2) / 2 - 6, 444, (y1 + y2) / 2 + 6, BAD, 2.4)
    for s, y in apps:
        g += node(100, y, 200, 48, s, WARN if s.startswith("Unknown") else CYAN)
    for s, y, col in dests:
        g += R(600, y, 270, 44, 10, CARD, col, 1.4) + C(622, y + 22, 5, col) + T(638, y + 27, s, 14.5, TEXT, 600, font=MONO)
    g += pulse(300, 434, 5, WARN)
    g += T(480, 540, "who is talking to whom, per app, in plain view", 14, MUTED, 400, "middle")
    return g


def firewall_2():
    g = R(96, 150, 190, 220, 16, CARD, LINE, 1.4) + R(136, 196, 110, 30, 5, LINE) + R(124, 226, 134, 60, 8, "#24245c", CYAN, 1.5) + R(144, 270, 94, 44, 4, "#f3f1ea") + C(244, 242, 4, GOOD)
    g += T(191, 346, "new on your network", 13, MUTED, 400, "middle") + pulse(191, 124, 7, CYAN)
    g += consent(330, 84, 540, "This looks like a printer", "In its first minutes it tried to reach:",
                 [("ALLOW", "your laptops and phones, on the home network", GOOD), ("ALLOW", "firmware.printer-maker.com, for updates", GOOD), ("BLOCK", "ads.tracker.net", BAD), ("BLOCK", "everything else on the internet", BAD)],
                 [("Use these rules", "primary"), ("Change", ""), ("Block it all", "danger")])
    return g


def firewall_3():
    g = R(90, 80, 780, 440, 18, "#16163c", BAD, 1.6) + C(132, 128, 16, DEEP, BAD, 2) + L(124, 120, 140, 136, BAD, 3) + L(140, 120, 124, 136, BAD, 3)
    g += T(162, 124, "Blocked: the smart speaker tried to reach unusual-host.example", 17, TEXT, 700) + T(162, 148, "03:12 last night. Nothing was sent.", 13.5, MUTED)
    g += T(130, 200, "Its normal day", 13, MUTED, 600)
    vals = [18, 22, 16, 20, 24, 19, 21, 17, 23, 20, 150, 22, 18, 20]
    for i, v in enumerate(vals):
        col = BAD if v > 100 else CYAN
        g += R(130 + i * 30, 380 - v, 20, v, 4, col, op=1 if v > 100 else .7)
    g += L(120, 381, 560, 381, LINE, 1.5) + L(120, 352, 560, 352, GOOD, 1.2, "5 6") + T(130, 344, "usual range", 12, GOOD)
    g += T(440, 220, "40× its usual volume", 13, BAD, 700, "middle")
    g += T(606, 250, "Why", 13, MUTED, 600)
    for i, (s, col) in enumerate([("An address it never used", WARN), ("Normally silent at night", WARN), ("Matches a known-bad pattern", BAD)]):
        g += C(610, 276 + i * 34, 4, col) + T(624, 281 + i * 34, s, 13, TEXT)
    g += button(130, 440, 150, "Keep blocking", True) + button(294, 440, 180, "It was me, allow it") + T(850, 466, "explained, not just blocked", 13, MUTED, 400, "end")
    return g


def car_dash(inner):
    return R(66, 92, 840, 420, 34, "#000000", op=.4) + R(58, 80, 840, 420, 34, "#07071a", LINE, 3) + inner


def car_1():
    e = f'<polygon points="210,190 300,350 120,350" fill="none" stroke="{WARN}" stroke-width="8" stroke-linejoin="round"/>' + R(204, 240, 12, 62, 6, WARN) + C(210, 324, 8, WARN)
    e += T(350, 222, "Stopped vehicle ahead", 34, TEXT, 700) + T(350, 268, "400 m · around the bend", 22, WARN, 600)
    e += T(350, 316, "Seen by 3 cars, 2 seconds ago", 16, MUTED)
    e += R(350, 350, 250, 70, 14, CARD, CYAN, 1.5) + T(372, 380, "Ease off to", 14, MUTED) + T(372, 408, "60 km/h", 24, CYAN, 700)
    e += pills(620, 372, [("advice only: you drive", GOOD)])
    e += pulse(210, 440, 6, WARN)
    return car_dash(e)


def car_2():
    g = R(0, 170, W, 260, 0, "#101030") + L(0, 170, W, 170, LINE, 3) + L(0, 430, W, 430, LINE, 3)
    for y in (257, 343):
        g += L(20, y, W - 20, y, MUTED, 2, "26 22", .5)

    def car(x, y, col):
        return R(x, y, 86, 44, 12, col, op=.95) + R(x + 54, y + 7, 20, 30, 5, DEEP, op=.5) + R(x + 16, y + 7, 14, 30, 5, DEEP, op=.35)
    g += car(120, 278, CYAN) + car(330, 192, VIOLET) + car(430, 364, VIOLET) + car(700, 278, BAD)
    g += f'<polygon points="812,268 836,310 788,310" fill="none" stroke="{WARN}" stroke-width="4" stroke-linejoin="round"/>' + T(812, 304, "!", 22, WARN, 700, "middle")
    g += pulse(743, 300, 8, WARN)
    g += P("M700 290 C600 240 480 230 418 222", WARN, 2.2, dash="6 7") + P("M700 310 C620 360 560 380 518 384", WARN, 2.2, dash="6 7") + P("M330 222 C280 250 240 280 208 292", WARN, 2.2, dash="6 7")
    g += T(163, 348, "you", 14, CYAN, 700, "middle") + T(480, 110, "A car that has stopped tells the cars behind it. They pass it on.", 17, TEXT, 600, "middle")
    g += pills(250, 470, [("signed", GOOD), ("short-lived", GOOD), ("no central map of who is where", GOOD)])
    return g


def car_3():
    e = P("M130 440 C230 380 260 300 380 280 S560 240 660 160 S780 130 830 130", MUTED, 9, op=.35) + P("M130 440 C230 380 260 300 380 280 S560 240 660 160 S780 130 830 130", BAD, 3, dash="2 12")
    e += P("M130 440 C200 440 300 430 400 400 S600 330 700 240 S800 150 830 130", "url(#brand)", 7)
    e += C(130, 440, 10, CYAN) + C(830, 130, 10, PINK) + T(148, 470, "home", 13, MUTED) + T(812, 112, "work", 13, MUTED, 400, "end")
    e += R(130, 118, 330, 150, 16, CARD, CYAN, 1.5) + T(154, 152, "Leave at 07:40", 22, TEXT, 700) + T(154, 180, "Take the river road", 15, CYAN, 600) + T(154, 208, "The ring road is filling up.", 13.5, MUTED) + T(154, 228, "4 minutes sooner, and smoother for everyone.", 13.5, MUTED)
    e += T(560, 430, "worked out in your car, from what nearby cars shared", 13, MUTED, 400, "middle")
    return car_dash(e)


def tv_1():
    g = tv(90, 50, 780, 440) + R(93, 53, 774, 434, 11, "url(#bg)") + C(700, 150, 200, "url(#g2)")
    g += T(140, 136, "7:42", 56, TEXT, 700) + T(140, 170, "Friday · 18° and clear", 17, MUTED) + T(820, 110, "Who is watching?", 15, MUTED, 400, "end")
    for i, (s, col) in enumerate([("Maya", CYAN), ("Leo", PINK), ("Sam", VIOLET), ("Kids", GOOD)]):
        x = 250 + i * 150
        g += C(x, 320, 46, CARD, col, 3 if i == 1 else 1.5) + T(x, 331, s[0], 34, col, 700, "middle") + T(x, 396, s, 16, TEXT if i == 1 else MUTED, 600, "middle")
    g += pills(396, 420, [("opens with a pattern on the remote", MUTED)], size=12)
    return g


def tv_2():
    g = tv(90, 50, 780, 440) + R(93, 53, 774, 434, 11, "url(#bg)")
    for i, col in enumerate([CYAN, MUTED, MUTED, MUTED, MUTED]):
        g += C(124, 110 + i * 46, 9, DEEP, col, 2)
    g += T(160, 104, "Continue watching", 17, TEXT, 700)
    for i in range(5):
        g += poster(160 + i * 136, 120, 122, 150, i, None, [.4, .75, .2, .9, .55][i])
    g += T(160, 310, "Recently added", 17, TEXT, 700)
    for i in range(5):
        g += poster(160 + i * 136, 326, 122, 140, i + 2)
    g += R(158, 118, 126, 154, 12, "none", CYAN, 3)
    return g


def tv_3():
    g = tv(90, 50, 780, 440) + R(93, 53, 774, 434, 11, "url(#bg)") + T(140, 104, "Maya's day", 22, TEXT, 700)
    g += R(140, 124, 330, 150, 14, CARD, VIOLET, 1.4) + T(160, 154, "Your brief", 14, VIOLET, 700) + T(160, 182, "A quiet morning. The dentist at", 14.5, TEXT) + T(160, 204, "11:30 overlaps your call, and Sara", 14.5, TEXT) + T(160, 226, "is waiting on the budget draft.", 14.5, TEXT)
    g += T(140, 306, "Calendar", 14, MUTED, 700)
    for i, s in enumerate(["11:30  Dentist", "16:00  School pickup"]):
        g += row(140, 318 + i * 52, 330, s)
    g += T(500, 138, "Mail", 14, MUTED, 700)
    for i, (s, sub) in enumerate([("Sara", "Budget draft"), ("School office", "Open day invitation"), ("Leo", "Photos from Saturday")]):
        g += row(500, 150 + i * 62, 330, s, None, TEXT, sub, MUTED, 52)
    g += pills(500, 352, [("shown only on Maya's profile", GOOD)], size=12) + pills(500, 388, [("from your own server at home", MUTED)], size=12)
    return g


def core_1():
    g = ""
    for i, s in enumerate(["Chat", "Study", "Assistant", "OS"]):
        g += node(70, 120 + i * 96, 150, 60, s, VIOLET) + arrow(224, 150 + i * 96, 350, 280 + (i - 1.5) * 26, VIOLET, sw=2)
    g += R(356, 150, 250, 300, 22, "#16163c", CYAN, 2) + T(481, 190, "Qalb", 20, TEXT, 700, "middle")
    for i, (s, col) in enumerate([("model gateway", CYAN), ("permissions", PINK), ("encrypted store", VIOLET), ("audit log", GOOD)]):
        g += R(380, 212 + i * 54, 202, 42, 10, CARD, col, 1.3) + T(481, 238 + i * 54, s, 14.5, TEXT, 600, "middle")
    g += node(720, 150, 180, 70, "Model on this device", GOOD, "no permission needed") + arrow(610, 250, 716, 196, GOOD)
    g += node(720, 380, 180, 70, "Cloud model", WARN, "only with your grant") + arrow(610, 350, 716, 404, WARN, "7 6")
    g += R(650, 362, 26, 22, 5, DEEP, WARN, 1.8) + P("M656 362 v-7 a7 7 0 0 1 14 0 v7", WARN, 2)
    g += T(481, 510, "every product goes through the same gate", 14, MUTED, 400, "middle")
    return g


def core_2():
    g = window(100, 70, 760, 450, "Your grants · everything that may leave this device")
    rows = [("Cloud model", "may receive: this conversation", "active", GOOD, "Revoke"), ("Calendar connector", "may read: events · may send: your login", "active", GOOD, "Revoke"),
            ("News feeds", "may fetch: 3 addresses you listed", "active", GOOD, "Revoke"), ("Mail connector", "may read: headers only", "expired yesterday", MUTED, "Renew")]
    for i, (a, b, st, col, act) in enumerate(rows):
        y = 134 + i * 78
        g += R(126, y, 708, 64, 12, CARD, LINE, 1.1, op=1 if col == GOOD else .6) + C(150, y + 32, 6, col) + T(168, y + 28, a, 16, TEXT, 700) + T(168, y + 48, b, 13, MUTED)
        g += T(660, y + 37, st, 13, col, 600, "end") + button(690, y + 13, 120, act, False, BAD if act == "Revoke" else CYAN)
    g += T(480, 480, "nothing on this list, nothing leaves", 14, MUTED, 400, "middle")
    return g


def core_3():
    g = T(480, 100, "Every decision is written down, and each entry seals the one before it", 17, TEXT, 600, "middle")
    items = [("#41", "allow", "chat → this device", GOOD), ("#42", "deny", "chat → cloud model", BAD), ("#43", "grant", "you allowed it", CYAN), ("#44", "allow", "chat → cloud model", GOOD)]
    for i, (n, d, s, col) in enumerate(items):
        x = 70 + i * 212
        g += R(x, 190, 184, 170, 16, CARD, col, 1.6) + T(x + 18, 224, n, 14, MUTED, 700) + T(x + 18, 262, d, 24, col, 700) + T(x + 18, 290, s, 13, TEXT)
        g += T(x + 18, 334, "seal " + ["7a1c…", "e03b…", "49fd…", "7073…"][i], 12.5, MUTED, font=MONO)
        if i < 3:
            g += R(x + 180, 262, 36, 22, 11, "none", MUTED, 3) + R(x + 196, 262, 36, 22, 11, "none", TEXT, 3)
    g += R(300, 420, 360, 60, 14, "#16163c", GOOD, 1.6) + C(336, 450, 12, DEEP, GOOD, 2) + P("M329 450 l5 6 l10 -12", GOOD, 2.6) + T(360, 446, "Verified: 44 entries, none missing", 15, TEXT, 700) + T(360, 466, "remove or edit one and the chain breaks", 12.5, MUTED)
    return g


def hub_1():
    g = window(120, 80, 720, 420, "terminal")
    lines = [("$ docker compose up -d", TEXT), ("", TEXT), ("✔ rafiq qalb            started", GOOD), ("✔ model server          started", GOOD), ("✔ database              started", GOOD), ("", TEXT),
             ("listening on this machine only", MUTED), ("no account needed · no secrets in the config", MUTED), ("", TEXT), ("$ ", TEXT)]
    for i, (s, col) in enumerate(lines):
        g += T(156, 156 + i * 30, s, 16, col, 500, font=MONO)
    g += cursor(180, 412, 18)
    return g


def hub_2():
    g = P("M210 300 L480 110 L750 300", VIOLET, 4, op=.7) + R(250, 300, 460, 220, 6, "none", VIOLET, 3, op=.7)
    g += R(420, 340, 120, 110, 14, "#16163c", CYAN, 2) + T(480, 388, "Markaz", 17, TEXT, 700, "middle") + C(450, 424, 4, GOOD) + C(466, 424, 4, GOOD) + R(480, 421, 44, 6, 3, LINE) + pulse(480, 318, 5, CYAN)
    devs = [(290, 350, "laptop"), (290, 450, "phone"), (670, 350, "TV"), (670, 450, "tablet")]
    for x, y, s in devs:
        g += node(x - 50, y - 22, 100, 44, s, VIOLET) + L(x + (50 if x < 480 else -50), y, 420 if x < 480 else 540, 395, CYAN, 2, "5 6")
    g += T(480, 80, "One small server. Everything stays inside the house.", 18, TEXT, 600, "middle")
    g += P("M790 250 q40 -40 80 0 q30 0 30 30 q0 28 -30 28 h-80 q-30 0 -30 -28 q0 -30 30 -30", MUTED, 2, op=.5) + L(770, 220, 890, 330, BAD, 3, op=.8) + T(830, 360, "no cloud required", 13, MUTED, 400, "middle")
    return g


def hub_3():
    g = R(380, 90, 200, 90, 16, "#16163c", CYAN, 2) + T(480, 132, "One Markaz", 20, TEXT, 700, "middle") + T(480, 156, "one model, shared", 13, MUTED, 400, "middle")
    for i, (s, col) in enumerate([("Maya", CYAN), ("Leo", PINK), ("Sam", VIOLET)]):
        x = 110 + i * 270
        g += L(480, 182, x + 100, 250, col, 2, "5 6") + R(x, 252, 200, 220, 16, CARD, col, 1.6) + C(x + 100, 306, 30, DEEP, col, 2) + T(x + 100, 317, s[0], 26, col, 700, "middle")
        g += T(x + 100, 370, s, 17, TEXT, 700, "middle") + T(x + 100, 396, "own memory", 13, MUTED, 400, "middle") + T(x + 100, 416, "own permissions", 13, MUTED, 400, "middle")
        g += R(x + 88, 436, 24, 20, 5, DEEP, GOOD, 1.8) + P(f"M{x + 94} 436 v-6 a6 6 0 0 1 12 0 v6", GOOD, 2)
    g += T(480, 520, "a household, a class or a team, each person with their own key", 14, MUTED, 400, "middle")
    return g


def study_4():
    g = window(80, 50, 800, 500, "For parents · this week")
    for i, (name, col, pct, sub, due) in enumerate([("Leo · Year 8", PINK, .72, "Maths, Science, History", "Maths test Thursday"), ("Maya · Year 5", CYAN, .9, "Reading, Maths", "Reading log due Friday")]):
        x = 104 + i * 388
        g += R(x, 106, 364, 190, 14, CARD, col, 1.4) + C(x + 62, 170, 38, "none", LINE, 8)
        import math
        a = 2 * math.pi * pct
        ex, ey = x + 62 + 38 * math.sin(a), 170 - 38 * math.cos(a)
        g += P(f"M{x + 62} 132 A38 38 0 {1 if pct > .5 else 0} 1 {ex:.1f} {ey:.1f}", col, 8) + T(x + 62, 177, f"{int(pct * 100)}%", 17, TEXT, 700, "middle")
        g += T(x + 122, 150, name, 18, TEXT, 700) + T(x + 122, 174, sub, 13, MUTED) + T(x + 122, 198, "of this week's plan done", 12.5, MUTED)
        g += pills(x + 18, 246, [(due, WARN)], size=12.5)
    g += T(104, 336, "Leo's plan", 15, TEXT, 700) + T(868, 336, "made from his syllabus and the family calendar", 12.5, MUTED, 400, "end")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    cells = [("Fractions", GOOD, 1), ("Forces", GOOD, 1), ("Fractions quiz", CYAN, 0), ("Test", WARN, 0), ("History notes", MUTED, 0)]
    for i, (d, (s2, col, done)) in enumerate(zip(days, cells)):
        x = 104 + i * 152
        g += T(x + 70, 366, d, 12.5, MUTED, 600, "middle") + R(x, 376, 140, 58, 10, CARD, col, 1.3) + T(x + 70, 410, s2, 13.5, TEXT, 600, "middle")
        if done:
            g += C(x + 124, 390, 8, DEEP, GOOD, 1.5) + P(f"M{x + 120} 390 l3 3 l6 -7", GOOD, 1.8)
    g += pills(104, 466, [("Fractions are not sticking yet", PINK), ("Explain it to me so I can help", CYAN)], size=12.5)
    g += T(868, 520, "Leo sees exactly what you see", 12.5, GOOD, 600, "end")
    return g


def home_1():
    g = window(80, 50, 800, 500, "Dar")
    g += T(110, 124, "Good evening", 22, TEXT, 700) + T(110, 148, "Everyone is home. All doors locked.", 14, GOOD)
    tiles = [("Living room", "Lights on · 40%", WARN), ("Heating", "21° · holding", PINK), ("Front door", "Locked", GOOD), ("Washer", "Done 10 min ago", CYAN),
             ("Kitchen", "Lights off", MUTED), ("Power", "Solar 2.1 kW · battery 86%", GOOD), ("Garage", "Closed", GOOD), ("Study", "Quiet hours until 19:00", VIOLET)]
    for i, (a, b, col) in enumerate(tiles):
        x, y = 110 + (i % 4) * 186, 176 + (i // 4) * 112
        g += R(x, y, 172, 98, 14, CARD, col if col != MUTED else LINE, 1.4) + C(x + 26, y + 30, 10, col, op=.9) + T(x + 16, y + 64, a, 15, TEXT, 700) + T(x + 16, y + 84, b, 11.5, MUTED)
    g += R(110, 412, 730, 54, 14, "#14143a", VIOLET, 1.5) + C(140, 439, 9, "url(#brand)") + T(162, 444, "turn everything off downstairs except the hall light", 15.5, TEXT, 600) + cursor(162 + tw("turn everything off downstairs except the hall light", 15.5) - 14, 430, 17)
    g += pills(110, 486, [("runs on your Markaz", GOOD), ("works with the devices you already have", MUTED)], size=12)
    return g


def home_2():
    g = T(480, 84, "Power, right now", 20, TEXT, 700, "middle")
    g += node(90, 150, 170, 80, "Solar", WARN, "2.1 kW") + node(90, 370, 170, 80, "Grid", MUTED, "0 kW · idle")
    g += R(390, 230, 180, 140, 18, "#16163c", CYAN, 2) + T(480, 290, "Home", 20, TEXT, 700, "middle") + T(480, 316, "using 1.3 kW", 14, MUTED, 400, "middle")
    g += node(700, 150, 170, 80, "Battery", GOOD, "86% · charging") + node(700, 370, 170, 80, "Car charger", VIOLET, "waiting for 13:00")
    g += arrow(264, 200, 386, 270, WARN) + arrow(574, 270, 696, 200, GOOD) + arrow(264, 400, 386, 340, MUTED, "6 6") + arrow(574, 340, 696, 400, VIOLET, "6 6")
    g += R(250, 474, 460, 100, 16, CARD, CYAN, 1.5) + T(274, 508, "Suggestion", 12.5, CYAN, 700) + T(274, 534, "Run the dishwasher at 13:00, when solar peaks.", 15.5, TEXT, 600) + T(274, 558, "In an outage: fridge, router and lights for 9 hours.", 13.5, MUTED)
    g += pulse(325, 235, 5, WARN)
    return g


def home_3():
    g = R(70, 80, 430, 440, 18, PANEL, LINE, 1.5) + T(94, 118, "Cameras", 17, TEXT, 700) + T(476, 118, "stored at home", 12.5, GOOD, 600, "end")
    for i, (name, n) in enumerate([("Front door", 2), ("Garden", 0), ("Driveway", 3), ("Garage", 1)]):
        x, y = 94 + (i % 2) * 196, 136 + (i // 2) * 150
        g += R(x, y, 184, 112, 10, f"url(#poster{n + 1})", op=.55) + P(f"M{x} {y + 86} Q{x + 60} {y + 50} {x + 110} {y + 80} T{x + 184} {y + 70} V{y + 112} H{x} Z", "none", 0, DEEP, .5) + T(x + 6, y + 130, name, 12.5, MUTED)
        g += C(x + 170, y + 14, 4, BAD)
    g += R(94, 136, 184, 112, 10, "none", WARN, 2.5) + R(150, 176, 34, 60, 6, "none", WARN, 2) + T(104, 156, "Person · 14:02", 12, WARN, 700)
    g += pills(94, 462, [("no face recognition unless you turn it on", MUTED)], size=11.5)
    g += R(540, 80, 350, 440, 18, PANEL, LINE, 1.5) + T(564, 118, "Groceries", 17, TEXT, 700)
    for i, (s2, sub, col) in enumerate([("Milk", "runs out Thursday", WARN), ("Eggs", "2 left", WARN), ("Rice", "plenty", GOOD), ("Coffee", "runs out next week", MUTED)]):
        g += row(564, 136 + i * 56, 302, s2, sub, TEXT, None, col)
    g += T(564, 386, "Shopping list", 13, MUTED, 600)
    for i, s2 in enumerate(["Milk", "Eggs", "Tomatoes"]):
        g += R(564 + i * 100, 398, 92, 34, 17, DEEP, CYAN, 1.2) + T(610 + i * 100, 420, s2, 13, CYAN, 600, "middle")
    g += T(564, 470, "Tonight: you have everything for a vegetable curry.", 12.5, MUTED) + T(564, 492, "Rafiq writes the list. You do the buying.", 12.5, MUTED)
    return g


def finance_1():
    g = window(80, 50, 800, 500, "Your money · this month")
    g += R(104, 106, 300, 150, 14, "#16163c", VIOLET, 1.5) + T(124, 140, "Net worth", 13, MUTED, 600) + T(124, 184, "84,210", 34, TEXT, 700) + T(124, 212, "up 1,340 this month", 13.5, GOOD, 600)
    g += P("M124 244 l30 -6 l30 2 l30 -10 l30 -2 l30 -12 l30 -4 l30 -10 l30 -6", GOOD, 2.5)
    for i, (a, b, col) in enumerate([("Current account", "3,480", TEXT), ("Savings", "12,900", TEXT), ("Credit card", "-640", BAD), ("Car loan", "-9,200 · ends Mar 2029", WARN)]):
        g += row(104, 276 + i * 54, 300, a, b, TEXT, None, col)
    g += T(440, 124, "Where it went", 15, TEXT, 700)
    for i, (a, v, col) in enumerate([("Housing", 1.0, VIOLET), ("Groceries", .52, CYAN), ("Transport", .34, PINK), ("Subscriptions", .2, WARN), ("Everything else", .44, MUTED)]):
        y = 150 + i * 52
        g += T(440, y + 14, a, 13.5, TEXT, 600) + R(440, y + 24, 400, 12, 6, LINE) + R(440, y + 24, 400 * v, 12, 6, col)
    g += R(440, 420, 400, 70, 12, CARD, WARN, 1.3) + T(458, 448, "Noticed", 12, WARN, 700) + T(458, 472, "Two streaming subscriptions went unused for 3 months.", 13.5, TEXT)
    g += pills(104, 500, [("kept on your device, encrypted", GOOD)], size=12)
    return g


def finance_2():
    g = window(100, 50, 760, 500, "Ask before you buy")
    b, h = bubble(430, 110, 400, ["Should I buy the 1,200 laptop now?"], True)
    g += b
    y = 110 + h + 20
    g += R(130, y, 620, 330, 16, "#16163c", CYAN, 1.6) + T(154, y + 40, "Wait about six weeks", 24, TEXT, 700) + T(154, y + 66, "Here is the working, from your own numbers.", 13.5, MUTED)
    for i, (label, text, col) in enumerate([("THIS MONTH", "It would leave 310 before the car loan payment on the 28th.", BAD), ("YOUR GOALS", "Your emergency fund is at 2.4 months; you set 3.", WARN),
                                           ("COST PER USE", "About 0.80 a day over four years. Reasonable for work.", GOOD), ("IF YOU WAIT", "After the bonus on the 15th it fits without touching savings.", CYAN)]):
        yy = y + 96 + i * 46
        g += T(154, yy, label, 11, col, 700) + T(274, yy, text, 13.5, TEXT) + L(154, yy + 16, 726, yy + 16, LINE, 1)
    g += button(154, y + 276, 150, "Remind me then", True) + button(316, y + 276, 190, "Show cheaper options")
    g += T(726, y + 300, "explains; never decides for you", 12, MUTED, 400, "end")
    return g


def finance_3():
    g = R(80, 80, 440, 440, 18, PANEL, LINE, 1.5) + T(106, 122, "Goals", 18, TEXT, 700)
    for i, (a, v, sub, col) in enumerate([("Emergency fund", .8, "2.4 of 3 months · on track for February", GOOD), ("Summer holiday", .45, "1,350 of 3,000", CYAN), ("Car loan paid off", .62, "March 2029 · overpay 60 a month to finish 5 months early", VIOLET)]):
        y = 150 + i * 110
        g += T(106, y + 14, a, 15.5, TEXT, 700) + R(106, y + 28, 388, 14, 7, LINE) + R(106, y + 28, 388 * v, 14, 7, col) + T(106, y + 66, sub, 12.5, MUTED)
    g += pills(106, 476, [("projections use your real spending", MUTED)], size=12)
    g += R(550, 80, 340, 300, 18, PANEL, LINE, 1.5) + T(576, 122, "Coming up", 18, TEXT, 700)
    for i, (a, b, col) in enumerate([("28th · Car loan", "410", TEXT), ("1st · Rent", "1,150", TEXT), ("3rd · Electricity", "about 96", MUTED), ("9th · Low balance likely", "top up 200", WARN)]):
        g += row(576, 140 + i * 56, 290, a, b, TEXT, None, col)
    g += R(550, 400, 340, 120, 18, "#16163c", GOOD, 1.6) + R(576, 432, 30, 26, 6, DEEP, GOOD, 2) + P("M583 432 v-8 a8 8 0 0 1 16 0 v8", GOOD, 2.2)
    g += T(622, 444, "Read-only by design", 16, TEXT, 700) + T(622, 466, "Rafiq can see your accounts.", 12.5, MUTED) + T(622, 484, "It can never move your money.", 12.5, MUTED)
    return g


SCENES = {
    "chat": [chat_1, chat_2, chat_3], "study": [study_1, study_2, study_3, study_4], "assistant": [assistant_1, assistant_2, assistant_3],
    "mobile": [mobile_1, mobile_2, mobile_3], "lamha": [lamha_1, lamha_2, lamha_3], "manzar": [manzar_1, manzar_2, manzar_3],
    "os": [os_1, os_2, os_3], "firewall": [firewall_1, firewall_2, firewall_3], "car": [car_1, car_2, car_3],
    "tv": [tv_1, tv_2, tv_3], "home": [home_1, home_2, home_3], "finance": [finance_1, finance_2, finance_3],
    "core": [core_1, core_2, core_3], "hub": [hub_1, hub_2, hub_3],
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for k, (slug, fns) in enumerate(SCENES.items()):
        for i, fn in enumerate(fns, 1):
            svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">{DEFS}{backdrop(k * 3 + i)}{fn()}</svg>\n'
            (OUT / f"{slug}-{i}.svg").write_text(svg, encoding="utf-8")
            n += 1
    print("drew", n, "scenes")


if __name__ == "__main__":
    main()
