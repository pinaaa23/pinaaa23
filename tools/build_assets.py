#!/usr/bin/env python3
"""Generates every SVG asset + README.md for the GitHub profile.

Theme: Minimal Dark Modern (one purple accent, lots of space).
Run:  python3 tools/build_assets.py
Edit the CONFIG block below, run again, commit the result.
"""
import os
import re
import xml.dom.minidom

# ───────────────────────── CONFIG ─────────────────────────
USERNAME = "YOUR_USERNAME"          # <- GitHub username (used by the snake)
NAME = "Refina Kusuma"
FIRST, LAST = "Refina", "Kusuma"
ROLE = "Frontend Developer · UI/UX Enthusiast"
PHRASES = [
    "Designing & building aesthetic web experiences",
    "Turning Figma ideas into real interfaces",
    "Crafting responsive, accessible UI",
]
STATUS = "Open to collaboration"
LOCATION = "Yogyakarta, Indonesia"
NOW = "Building projects"
LEARNING = "Next.js · Tailwind CSS"
FOCUS = ["UI/UX", "Responsive Web", "Design System"]
STACK = {
    "Design": ["Figma", "Canva", "UI/UX Design", "Wireframing", "Prototyping"],
    "Frontend": ["HTML / CSS", "JavaScript", "React.js", "Next.js", "Tailwind CSS"],
    "Tools": ["Git / GitHub", "VS Code", "Webpack", "Vercel", "Postman"],
}
LINKS = [  # label, url
    ("Portfolio", "https://itsrefif.my.id/"),
    ("Email", "mailto:kusumarefina@gmail.com"),
    ("LinkedIn", "https://www.linkedin.com/in/YOUR_LINKEDIN"),
    ("Dribbble", "https://dribbble.com/YOUR_DRIBBBLE"),
]
PROJECTS = [  # name, url, description, stack
    ("Project One", "https://github.com/YOUR_USERNAME/project-one", "Short one-line description of what it does.", "React · Tailwind"),
    ("Project Two", "https://github.com/YOUR_USERNAME/project-two", "Short one-line description of what it does.", "Next.js · Figma"),
    ("Project Three", "https://github.com/YOUR_USERNAME/project-three", "Short one-line description of what it does.", "HTML · CSS · JS"),
]
# ──────────────────────────────────────────────────────────

SANS = "Inter,'Segoe UI',system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(bg="#0a0a0f", surface="#12121a", surface2="#181824", border="#252533",
                 text="#ececf1", muted="#8d8da0", acc="#a78bfa", acc2="#7c3aed", glow="0.34"),
    "light": dict(bg="#fbfbfd", surface="#ffffff", surface2="#f3f1fb", border="#e4e2ef",
                  text="#17171f", muted="#6b6b7d", acc="#7c3aed", acc2="#a78bfa", glow="0.20"),
}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tok(s, t):
    for k in sorted(t, key=len, reverse=True):
        s = s.replace("$" + k, t[k])
    return s


def wrap(w, h, title, css, body, t):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
           f'<style>{tok(css, t)}</style>{tok(body, t)}</svg>')
    return svg


def save(name, svg):
    xml.dom.minidom.parseString(svg)  # fail loudly on invalid XML
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def tw(text, size, mono=False):
    return len(text) * size * (0.61 if mono else 0.56)


BASE_CSS = f"""
text{{font-family:{SANS}}}
.m{{font-family:{MONO}}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(2.6);opacity:0}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-9px)}}}}
@keyframes floatb{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(8px)}}}}
@keyframes shimmer{{0%{{opacity:.55}}50%{{opacity:1}}100%{{opacity:.55}}}}
.rise{{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}}
.ring{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


# ───────────────────────── banner ─────────────────────────
def banner(t):
    W, H = 1200, 340
    n = len(PHRASES)
    cyc = 4 * n
    phr = ""
    for i, p in enumerate(PHRASES):
        base = "1" if i == 0 else "0"
        phr += (f'<text class="m ph" x="86" y="268" font-size="20" fill="$text" opacity="{base}" '
                f'style="animation-delay:{i*4}s">{esc(p)}</text>')
    css = BASE_CSS + f"""
@keyframes cyc{{0%{{opacity:0;transform:translateY(8px)}}4%{{opacity:1;transform:none}}28%{{opacity:1;transform:none}}
 33%{{opacity:0;transform:translateY(-8px)}}100%{{opacity:0}}}}
@keyframes orb1{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(-70px,40px)}}}}
@keyframes orb2{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(60px,-50px)}}}}
@keyframes cursor{{0%,100%{{transform:translate(0,0)}}45%{{transform:translate(-92px,52px)}}60%{{transform:translate(-92px,52px) scale(.9)}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.ph{{animation:cyc {cyc}s ease-in-out infinite both}}
.o1{{animation:orb1 14s ease-in-out infinite}}
.o2{{animation:orb2 17s ease-in-out infinite}}
.fl{{animation:float 6s ease-in-out infinite}}
.fb{{animation:floatb 7s ease-in-out infinite}}
.cu{{animation:cursor 7s ease-in-out infinite}}
.sh{{animation:shimmer 3s ease-in-out infinite}}
.bl{{animation:blink 1s steps(1) infinite}}
"""
    pill_w = tw(STATUS, 14) + 58
    body = f"""
<defs>
 <clipPath id="c"><rect width="{W}" height="{H}" rx="22"/></clipPath>
 <filter id="b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
 <pattern id="d" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="$muted" opacity=".28"/></pattern>
 <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="$acc"/><stop offset="1" stop-color="$acc2"/></linearGradient>
 <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="$bg" stop-opacity="0"/><stop offset=".5" stop-color="$bg" stop-opacity="0"/><stop offset="1" stop-color="$bg" stop-opacity="0"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="22" fill="$bg"/>
<g clip-path="url(#c)">
 <rect width="{W}" height="{H}" fill="url(#d)"/>
 <circle class="o1" cx="960" cy="70" r="150" fill="$acc" opacity="$glow" filter="url(#b)"/>
 <circle class="o2" cx="1090" cy="300" r="130" fill="$acc2" opacity="$glow" filter="url(#b)"/>
 <circle class="o1" cx="-10" cy="330" r="110" fill="$acc2" opacity=".14" filter="url(#b)"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="$border"/>

<g class="rise" style="animation-delay:.1s">
 <rect x="60" y="52" width="{pill_w}" height="34" rx="17" fill="$surface" stroke="$border"/>
 <circle cx="82" cy="69" r="4.5" fill="$acc"/>
 <circle class="ring" cx="82" cy="69" r="4.5" fill="$acc"/>
 <text x="98" y="74" font-size="14" fill="$muted">{esc(STATUS)}</text>
</g>
<g class="rise" style="animation-delay:.25s">
 <text x="58" y="168" font-size="64" font-weight="700" letter-spacing="-1.5" fill="$text">{esc(FIRST)} <tspan fill="url(#g)">{esc(LAST)}</tspan></text>
</g>
<g class="rise" style="animation-delay:.4s">
 <text x="60" y="212" font-size="24" fill="$muted">{esc(ROLE)}</text>
</g>
<g class="rise" style="animation-delay:.55s">
 <text class="m" x="60" y="268" font-size="20" fill="$acc" font-weight="700">›</text>
 {phr}
</g>

<g class="fl">
 <rect x="770" y="56" width="360" height="228" rx="16" fill="$surface" stroke="$border"/>
 <circle cx="792" cy="78" r="5" fill="$border"/><circle cx="810" cy="78" r="5" fill="$border"/><circle cx="828" cy="78" r="5" fill="$border"/>
 <line x1="770" y1="98" x2="1130" y2="98" stroke="$border"/>
 <rect class="sh" x="794" y="118" width="170" height="16" rx="8" fill="$acc"/>
 <rect x="794" y="146" width="250" height="9" rx="4.5" fill="$border"/>
 <rect x="794" y="164" width="205" height="9" rx="4.5" fill="$border"/>
 <rect x="794" y="196" width="96" height="66" rx="10" fill="$surface2" stroke="$border"/>
 <rect x="902" y="196" width="96" height="66" rx="10" fill="$surface2" stroke="$border"/>
 <rect x="1010" y="196" width="96" height="66" rx="10" fill="$surface2" stroke="$border"/>
 <circle cx="842" cy="221" r="9" fill="$acc" opacity=".8"/>
 <rect x="812" y="240" width="60" height="6" rx="3" fill="$border"/>
 <rect x="920" y="214" width="60" height="6" rx="3" fill="$border"/>
 <rect x="920" y="228" width="40" height="6" rx="3" fill="$border"/>
 <rect x="1028" y="214" width="60" height="6" rx="3" fill="$border"/>
 <rect x="1028" y="228" width="40" height="6" rx="3" fill="$border"/>
</g>
<g class="fb">
 <rect x="1000" y="112" width="132" height="34" rx="17" fill="url(#g)"/>
 <text class="m" x="1066" y="134" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">Figma → Code</text>
</g>
<g class="fb">
 <rect x="716" y="206" width="104" height="30" rx="15" fill="$surface" stroke="$border"/>
 <text class="m" x="768" y="226" font-size="12" fill="$muted" text-anchor="middle">&lt;/&gt; React</text>
</g>
<g class="cu">
 <path d="M1068 176 l0 24 l7 -6 l5 11 l5 -2 l-5 -11 l9 0 z" fill="$text" stroke="$bg" stroke-width="1.5" stroke-linejoin="round"/>
</g>
"""
    return wrap(W, H, f"{NAME} — {ROLE}", css, body, t)


# ───────────────────────── section header ─────────────────────────
def header(idx, label, t):
    W, H = 1200, 48
    lx = 62 + int(tw(label, 22)) + 22
    css = BASE_CSS + """
@keyframes draw{from{stroke-dashoffset:1200}to{stroke-dashoffset:0}}
.ln{stroke-dasharray:1200;animation:draw 1.6s ease-out both .2s}
"""
    body = f"""
<rect x="0" y="12" width="4" height="24" rx="2" fill="$acc"/>
<text class="m" x="18" y="31" font-size="14" fill="$acc" font-weight="700">{idx}</text>
<text x="56" y="33" font-size="22" font-weight="650" fill="$text" letter-spacing="-.3">{esc(label)}</text>
<line class="ln" x1="{lx}" y1="24" x2="1200" y2="24" stroke="$border" stroke-width="1.2"/>
"""
    return wrap(W, H, label, css, body, t)


# ───────────────────────── about (bento) ─────────────────────────
def tile(x, y, w, h, delay, inner):
    return (f'<g class="rise" style="animation-delay:{delay}s">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="$surface" stroke="$border"/>{inner}</g>')


def chip(x, y, label, size=14, fill="$surface2", stroke="$border", color="$text"):
    w = tw(label, size) + 26
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{x + w/2:.0f}" y="{y+20}" font-size="{size}" fill="{color}" text-anchor="middle">{esc(label)}</text>'), w


def about(t):
    W, H = 1200, 390
    css = BASE_CSS
    lab = lambda x, y, s: f'<text class="m" x="{x}" y="{y}" font-size="12" fill="$muted" letter-spacing="1.5">{s}</text>'
    # A: about
    a = (lab(30, 44, "ABOUT") +
         f'<text x="30" y="96" font-size="30" font-weight="700" fill="$text" letter-spacing="-.5">Designing &amp; building</text>'
         f'<text x="30" y="136" font-size="30" font-weight="700" letter-spacing="-.5"><tspan fill="url(#g)">aesthetic</tspan><tspan fill="$text" dx="9">web experiences.</tspan></text>'
         f'<text x="30" y="176" font-size="15" fill="$muted">I bridge UI/UX design and frontend code, turning ideas into real interfaces.</text>')
    # B: focus
    bx, by = 0, 0
    chips = ""
    cx, cy = 30, 74
    for f_ in FOCUS:
        c, w = chip(cx, cy, f_)
        if cx + w > 410 - 30:
            cx, cy = 30, cy + 40
            c, w = chip(cx, cy, f_)
        chips += c
        cx += w + 10
    b = lab(30, 44, "FOCUS") + chips + \
        f'<text x="30" y="{cy+62}" font-size="14" fill="$muted">Clean interfaces, consistent systems,</text>' \
        f'<text x="30" y="{cy+84}" font-size="14" fill="$muted">and smooth responsive behavior.</text>'
    # C: now
    c_ = (lab(30, 44, "NOW") +
          '<circle cx="36" cy="82" r="5" fill="$acc"/><circle class="ring" cx="36" cy="82" r="5" fill="$acc"/>'
          f'<text x="52" y="88" font-size="18" font-weight="600" fill="$text">{esc(NOW)}</text>'
          f'<text class="m" x="30" y="122" font-size="13" fill="$muted">learning · <tspan fill="$acc">{esc(LEARNING)}</tspan></text>')
    # D: location
    d = (lab(30, 44, "BASED IN") +
         '<path d="M38 70 c-9 0 -15 7 -15 15 c0 11 15 24 15 24 s15 -13 15 -24 c0 -8 -6 -15 -15 -15 z" fill="none" stroke="$acc" stroke-width="2"/>'
         '<circle cx="38" cy="85" r="5" fill="$acc"/>'
         f'<text x="66" y="92" font-size="18" font-weight="600" fill="$text">{esc(LOCATION)}</text>'
         '<text class="m" x="30" y="128" font-size="13" fill="$muted">UTC+07:00</text>')
    # E: open for
    e = (lab(30, 44, "OPEN FOR") +
         '<text x="30" y="90" font-size="18" font-weight="600" fill="$text">Collaboration</text>'
         '<text class="m" x="30" y="122" font-size="13" fill="$muted">design × code projects</text>')

    body = f"""
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="$acc"/><stop offset="1" stop-color="$acc2"/></linearGradient></defs>
{tile(0,0,720,210,.05,a)}
<g transform="translate(740,0)">{tile(0,0,460,210,.15,b)}</g>
<g transform="translate(0,230)">{tile(0,0,380,150,.25,c_)}</g>
<g transform="translate(400,230)">{tile(0,0,390,150,.35,d)}</g>
<g transform="translate(810,230)">{tile(0,0,390,150,.45,e)}</g>
"""
    return wrap(W, H, "About me", css, body, t)


# ───────────────────────── stack ─────────────────────────
def stack(t):
    W = 1200
    tw_, gap = 380, 30
    layouts = {}
    max_rows = 0
    for name, items in STACK.items():
        x, row, placed = 0, 0, []
        for it in items:
            w = tw(it, 14) + 26
            if x + w > tw_ - 60:
                x, row = 0, row + 1
            placed.append((it, x, row, w))
            x += w + 10
        layouts[name] = placed
        max_rows = max(max_rows, row + 1)
    H = 74 + max_rows * 42 + 26
    css = BASE_CSS
    body = ""
    for i, (name, placed) in enumerate(layouts.items()):
        x0 = i * (tw_ + gap)
        inner = f'<text class="m" x="30" y="44" font-size="12" fill="$muted" letter-spacing="1.5">{esc(name.upper())}</text>'
        inner += f'<rect x="{tw_-54}" y="30" width="24" height="3" rx="1.5" fill="$acc"/>'
        for it, x, row, w in placed:
            c, _ = chip(30 + x, 66 + row * 42, it)
            inner += c
        body += f'<g transform="translate({x0},0)">{tile(0,0,tw_,H,.05+i*.12,inner)}</g>'
    return wrap(W, H, "Tech stack", css, body, t)


# ───────────────────────── footer / divider / buttons ─────────────────────────
def footer(t):
    W, H = 1200, 110
    css = BASE_CSS + "@keyframes sweep{from{transform:translateX(-400px)}to{transform:translateX(1200px)}}.sw{animation:sweep 5s linear infinite}"
    body = f"""
<defs><linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="$acc" stop-opacity="0"/><stop offset=".5" stop-color="$acc"/><stop offset="1" stop-color="$acc" stop-opacity="0"/></linearGradient>
<clipPath id="k"><rect x="0" y="20" width="1200" height="2"/></clipPath></defs>
<rect x="0" y="20" width="1200" height="1.2" fill="$border"/>
<g clip-path="url(#k)"><rect class="sw" x="0" y="20" width="400" height="2" fill="url(#s)"/></g>
<text x="600" y="62" font-size="15" fill="$muted" text-anchor="middle">Designed &amp; coded with care by <tspan fill="$text" font-weight="600">{esc(NAME)}</tspan></text>
<text class="m" x="600" y="88" font-size="12" fill="$muted" text-anchor="middle" opacity=".8">thanks for stopping by ✦</text>
"""
    return wrap(W, H, "Footer", css, body, t)


def divider(t):
    W, H = 1200, 24
    css = BASE_CSS + "@keyframes sweep{from{transform:translateX(-300px)}to{transform:translateX(1200px)}}.sw{animation:sweep 6s linear infinite}"
    body = """
<defs>
<linearGradient id="e" x1="0" x2="1"><stop offset="0" stop-color="$border" stop-opacity="0"/><stop offset=".5" stop-color="$border"/><stop offset="1" stop-color="$border" stop-opacity="0"/></linearGradient>
<linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="$acc" stop-opacity="0"/><stop offset=".5" stop-color="$acc"/><stop offset="1" stop-color="$acc" stop-opacity="0"/></linearGradient>
<clipPath id="k"><rect x="0" y="11" width="1200" height="2"/></clipPath></defs>
<rect x="0" y="11.4" width="1200" height="1.2" fill="url(#e)"/>
<g clip-path="url(#k)"><rect class="sw" x="0" y="11" width="300" height="2" fill="url(#s)"/></g>
"""
    return wrap(W, H, "Divider", css, body, t)


def button(label):
    w = int(tw(label, 14) + 62)
    H = 40
    css = BASE_CSS
    body = f"""
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#6d28d9"/></linearGradient></defs>
<rect width="{w}" height="{H}" rx="20" fill="url(#g)"/>
<text x="24" y="25.5" font-size="14" font-weight="600" fill="#fff">{esc(label)}</text>
<text x="{w-26}" y="25.5" font-size="14" font-weight="700" fill="#fff" opacity=".85">↗</text>
"""
    return wrap(w, H, label, css, body, THEMES["dark"]), w


# ───────────────────────── build ─────────────────────────
def main():
    sections = [("01", "About"), ("02", "Tech Stack"), ("03", "Selected Work"), ("04", "Activity"), ("05", "Connect")]
    for mode, t in THEMES.items():
        save(f"banner-{mode}.svg", banner(t))
        save(f"about-{mode}.svg", about(t))
        save(f"stack-{mode}.svg", stack(t))
        save(f"footer-{mode}.svg", footer(t))
        for idx, lab in sections:
            save(f"h-{lab.lower().replace(' ', '-')}-{mode}.svg", header(idx, lab, t))
    save("divider-dark.svg", divider(THEMES["dark"]))
    save("divider-light.svg", divider(THEMES["light"]))
    widths = {}
    for lab, _ in LINKS:
        svg, w = button(lab)
        save(f"btn-{lab.lower()}.svg", svg)
        widths[lab] = w

    def pic(name, alt, width=None, link=None):
        wattr = f' width="{width}"' if width else ""
        p = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
             f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">'
             f'<img src="assets/{name}-dark.svg" alt="{alt}"{wattr}></picture>')
        return f'<a href="{link}">{p}</a>' if link else p

    def head(lab):
        slug = lab.lower().replace(" ", "-")
        return f'<p align="center">{pic("h-" + slug, lab)}</p>'

    btns = "\n".join(f'<a href="{u}"><img src="assets/btn-{l.lower()}.svg" alt="{l}" height="40"></a>' for l, u in LINKS)
    rows = "\n".join(f"| **[{n}]({u})** | {d} | `{s}` |" for n, u, d, s in PROJECTS)
    snake = (f'<picture>'
             f'<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/{USERNAME}/{USERNAME}/output/github-snake-dark.svg">'
             f'<source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/{USERNAME}/{USERNAME}/output/github-snake.svg">'
             f'<img alt="Contribution snake" src="https://raw.githubusercontent.com/{USERNAME}/{USERNAME}/output/github-snake-dark.svg">'
             f'</picture>')

    readme = f"""<p align="center">
{pic("banner", NAME + " — " + ROLE)}
</p>

<p align="center">
{btns}
</p>

<p align="center">{pic("divider", "")}</p>

{head("About")}
<p align="center">{pic("about", "About me")}</p>

{head("Tech Stack")}
<p align="center">{pic("stack", "Tech stack")}</p>

{head("Selected Work")}

| Project | What it is | Stack |
| :-- | :-- | :-- |
{rows}

{head("Activity")}
<p align="center">
{snake}
</p>

<!--
OPTIONAL single stats card (public Vercel instances are often rate-limited and can show broken images,
so it is off by default). Uncomment if you want it:
<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username={USERNAME}&layout=compact&hide_border=true&bg_color=0a0a0f&title_color=a78bfa&text_color=ececf1" alt="Top languages">
</p>
-->

{head("Connect")}
<p align="center">
{btns}
</p>

<p align="center">{pic("footer", "Footer")}</p>
"""
    with open(os.path.join(OUT, "..", "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    print("ok")


if __name__ == "__main__":
    main()
