#!/usr/bin/env python3
"""Builds the animated "profile scan" panel (assets/scan.svg).

  python3 tools/build_scan.py                       # live data from GitHub API
  python3 tools/build_scan.py --sample              # offline, placeholder numbers
  python3 tools/build_scan.py --out dist/scan.svg   # custom output (used by the Action)

Portrait: put a photo at tools/portrait.jpg (or .png). It is converted to ASCII.
Without a photo a neutral silhouette is used.
Env: GITHUB_TOKEN (optional, needed for contributions / active days).
"""
import argparse
import json
import os
import urllib.request
import xml.dom.minidom
from html import escape

# ───────────── CONFIG ─────────────
USERNAME = "pinaaa23"
SUBJECT = "Refina Kusuma"
ROLE = "Frontend Developer · UI/UX"
STATUS = "Building | Learning | Designing"
CONTACT = "itsrefif.my.id"
FALLBACK_LANGS = "JavaScript, HTML, CSS"
# ──────────────────────────────────

HERE = os.path.dirname(os.path.abspath(__file__))
COLS, ROWS = 73, 49
CW, CH = 3.7, 5.5          # ascii cell size in px
RAMP = " .'`^:;-~+=*xoO#%@"


# ───────────────────────── data ─────────────────────────
def http(url, token=None, data=None):
    h = {"User-Agent": "profile-scan", "Accept": "application/vnd.github+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=h, data=data)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def fetch(user):
    tok = os.environ.get("GITHUB_TOKEN")
    u = http(f"https://api.github.com/users/{user}", tok)
    repos, page = [], 1
    while page <= 5:
        chunk = http(f"https://api.github.com/users/{user}/repos?per_page=100&type=owner&page={page}", tok)
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    own = [r for r in repos if not r.get("fork")]
    langs = {}
    for r in own:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    top = ", ".join(k for k, _ in sorted(langs.items(), key=lambda kv: -kv[1])[:3]) or FALLBACK_LANGS
    d = dict(repos=u.get("public_repos", len(own)), followers=u.get("followers", 0),
             stars=sum(r.get("stargazers_count", 0) for r in own), langs=top,
             contrib="—", days="—")
    if tok:
        q = {"query": 'query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount}}}}}}',
             "variables": {"l": user}}
        try:
            g = http("https://api.github.com/graphql", tok, json.dumps(q).encode())
            cal = g["data"]["user"]["contributionsCollection"]["contributionCalendar"]
            d["contrib"] = f'{cal["totalContributions"]:,}'
            d["days"] = str(sum(1 for w in cal["weeks"] for x in w["contributionDays"] if x["contributionCount"] > 0))
        except Exception as e:  # keep going without these two numbers
            print("graphql skipped:", e)
    return d


SAMPLE = dict(repos=12, followers=7, stars=3, langs=FALLBACK_LANGS, contrib="214", days="96")


# ───────────────────────── ascii portrait ─────────────────────────
CROP = (0.078, 0.048, 0.922, 0.903)   # (left, top, right, bottom) as fractions of the photo


def load_portrait(path=None, crop=None):
    crop = crop or CROP
    """Returns (luma 0..1, alpha 0..1) PIL images, cropped. Transparent background = empty."""
    from PIL import Image, ImageDraw, ImageFilter
    path = path or next((os.path.join(HERE, n) for n in ("portrait.png", "portrait.jpg", "portrait.jpeg")
                         if os.path.exists(os.path.join(HERE, n))), None)
    if path:
        im = Image.open(path).convert("RGBA")
        w, h = im.size
        im = im.crop((int(w * crop[0]), int(h * crop[1]), int(w * crop[2]), int(h * crop[3])))
        return im.convert("L"), im.getchannel("A")
    im = Image.new("L", (400, 480), 0)
    d = ImageDraw.Draw(im)
    d.ellipse((130, 70, 270, 250), fill=215)
    d.ellipse((50, 250, 350, 560), fill=150)
    im = im.filter(ImageFilter.GaussianBlur(5))
    return im, im.point(lambda v: 255 if v > 40 else 0)


USER_CROP = None
CROP_DISC = (0.056, 0.0, 0.944, 0.96)   # square crop: head down to the chest (relative to tools/portrait.png)
HOLE = 0.20      # tones darker than this stay empty (eyes, mouth, hijab, shadows)


def ascii_layers(path=None):
    """Two aligned layers inside a circle: (background texture, subject)."""
    from PIL import Image, ImageFilter, ImageOps
    L, A = load_portrait(path, USER_CROP or CROP_DISC)
    L = L.filter(ImageFilter.UnsharpMask(radius=4, percent=170, threshold=2))
    L = Image.blend(ImageOps.autocontrast(L, cutoff=1), ImageOps.equalize(L), 0.5)
    L = L.resize((COLS, ROWS), Image.BOX)
    A = A.resize((COLS, ROWS), Image.BOX)
    lp, ap = L.load(), A.load()
    ramp = ".:-=+*#%@"
    cx, cy = COLS / 2, ROWS / 2
    bg, fg = [], []
    for r in range(ROWS):
        b_row, f_row = "", ""
        for c in range(COLS):
            # circle test in px space (cells are not square)
            dx, dy = (c + .5 - cx) * CW, (r + .5 - cy) * CH
            if dx * dx + dy * dy > (min(COLS * CW, ROWS * CH) / 2 - 1) ** 2:
                b_row += " "; f_row += " "
                continue
            if ap[c, r] < 110:                      # empty space -> texture
                b_row += ":"; f_row += " "
                continue
            v = lp[c, r] / 255
            if v < HOLE:                            # dark feature -> hole
                b_row += " "; f_row += " "
                continue
            t = (v - HOLE) / (1 - HOLE)
            b_row += " "
            f_row += ramp[min(len(ramp) - 1, int(t ** 0.7 * len(ramp)))]
        bg.append(b_row); fg.append(f_row)
    return bg, fg


PORTRAIT = None
STYLE = "ascii"

def photo_data_uri(path=None, size=(560, 520)):
    """Duotone (purple) cut-out of the photo as a small base64 PNG."""
    import base64, io
    from PIL import Image, ImageOps
    path = path or next((os.path.join(HERE, n) for n in ("portrait.png", "portrait.jpg", "portrait.jpeg")
                         if os.path.exists(os.path.join(HERE, n))), None)
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    im = im.crop((int(w * CROP[0]), int(h * CROP[1]), int(w * CROP[2]), int(h * CROP[3])))
    im.thumbnail(size, Image.LANCZOS)
    a = im.getchannel("A")
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    g = g.point(lambda v: int(255 * (v / 255) ** 0.8))
    lo, hi = (38, 32, 72), (214, 200, 255)
    duo = ImageOps.colorize(g, lo, hi, mid=(120, 96, 214), midpoint=128).convert("RGBA")
    duo.putalpha(a)
    q = duo.quantize(colors=96, method=Image.FASTOCTREE, dither=Image.NONE)
    buf = io.BytesIO()
    q.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.size


# ───────────────────────── svg ─────────────────────────
def build(data):
    W, H = 1000, 400
    px0, py0, pw, ph = 28, 64, 400, 308     # left panel
    rx0, rw = 448, 524                      # right panel
    ax = px0 + (pw - CW * COLS) / 2
    ay = py0 + 32
    scan_dur = 7.0
    sweep = 0.24 * scan_dur                 # seconds the first pass takes
    start = 0.45

    rows_svg = ""
    if STYLE == "photo":
        uri, (iw, ih) = photo_data_uri(PORTRAIT)
        box_h = ph - 56
        box_w = box_h * iw / ih
        if box_w > pw - 24:
            box_w, box_h = pw - 24, (pw - 24) * ih / iw
        bx, by = px0 + (pw - box_w) / 2, py0 + 40 + (ph - 56 - box_h)
        rows_svg = (f'<image class="ph" href="{uri}" x="{bx:.1f}" y="{by:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" '
                    f'preserveAspectRatio="xMidYMid meet" style="animation-delay:{start + 0.13:.2f}s"/>')
    if STYLE != "photo":
        bg, fg = ascii_layers(PORTRAIT)
        for i in range(ROWS):
            d = start + 0.13 + (i / ROWS) * sweep
            for cls, line in (("b", bg[i]), ("a", fg[i])):
                if line.strip():
                    rows_svg += (f'<text class="{cls}" x="{ax:.1f}" y="{ay + i * CH + 4.4:.1f}" textLength="{CW * COLS:.1f}" '
                                 f'lengthAdjust="spacing" xml:space="preserve" style="animation-delay:{d:.2f}s">{escape(line)}</text>')

    fields = [
        ("SUBJECT", SUBJECT), ("HANDLE", "@" + USERNAME), ("ROLE", ROLE), ("STATUS", STATUS),
        ("LANGUAGES", data["langs"]), ("REPOSITORIES", str(data["repos"])),
        ("CONTRIBUTIONS", str(data["contrib"])), ("STARS", str(data["stars"])),
        ("FOLLOWERS", str(data["followers"])), ("ACTIVE DAYS", str(data["days"])), ("CONTACT", CONTACT),
    ]
    f_svg, t = "", 0.9
    fy = py0 + 62
    for i, (k, v) in enumerate(fields):
        y = fy + i * 21
        n = max(1, len(v))
        dur = min(0.9, 0.05 * n + 0.15)
        f_svg += (f'<g class="r" style="animation-delay:{t:.2f}s"><text class="k" x="{rx0 + 24}" y="{y}">{k}</text>'
                  f'<text class="v" x="{rx0 + 196}" y="{y}" style="animation-delay:{t:.2f}s;animation-duration:{dur:.2f}s;'
                  f'animation-timing-function:steps({n},end)">{escape(v)}</text></g>')
        t += 0.3
    done = t + 0.2
    css = f"""
text{{font-family:'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace}}
.a{{font-size:6.1px;fill:#e6deff;white-space:pre}}
.b{{font-size:6.1px;fill:#8b7be0;fill-opacity:.42;white-space:pre}}
.k{{font-size:11.5px;fill:#7d7a99;letter-spacing:1px}}
.v{{font-size:12.5px;fill:#ececf1;font-weight:600}}
.h{{font-size:11px;fill:#a78bfa;letter-spacing:2px}}
.t{{font-size:12px;fill:#8d8da0}}
.win{{animation:win .6s cubic-bezier(.2,.7,.2,1) both}}
.a,.b{{animation:fade .12s linear backwards}}
.ph{{animation:wipe {sweep:.2f}s linear backwards}}
@keyframes wipe{{from{{clip-path:inset(0 0 100% 0)}}to{{clip-path:inset(0 0 0 0)}}}}
.r{{animation:fade .25s ease-out backwards}}
.v{{animation-name:type;animation-fill-mode:backwards}}
.scan{{animation:scan {scan_dur}s linear {start}s infinite}}
.done{{animation:fade .3s ease-out {done:.2f}s backwards}}
.cur{{opacity:0;animation:blink 1s steps(1) {done:.2f}s infinite}}
@keyframes win{{from{{opacity:0;transform:translateY(12px) scale(.985)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes type{{from{{clip-path:inset(-4px 100% -4px 0)}}to{{clip-path:inset(-4px 0 -4px 0)}}}}
@keyframes scan{{0%{{transform:translateY(0);opacity:0}}2%{{opacity:1}}26%{{transform:translateY({CH * ROWS:.0f}px);opacity:1}}28%{{opacity:0}}100%{{transform:translateY({CH * ROWS:.0f}px);opacity:0}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""
    body = f"""
<defs>
 <linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a78bfa" stop-opacity="0"/><stop offset="1" stop-color="#a78bfa" stop-opacity=".55"/></linearGradient>
 <clipPath id="ac"><rect x="{px0}" y="{ay - 6}" width="{pw}" height="{CH * ROWS + 12:.0f}"/></clipPath>
</defs>
<g class="win">
 <rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="#08080d" stroke="#2c2644"/>
 <circle cx="26" cy="24" r="5.5" fill="#ff5f57"/><circle cx="46" cy="24" r="5.5" fill="#febc2e"/><circle cx="66" cy="24" r="5.5" fill="#28c840"/>
 <text class="t" x="500" y="28" text-anchor="middle">{USERNAME}@github ~ $ ./profile-scan --live</text>
 <line x1="0" y1="44" x2="{W}" y2="44" stroke="#1d1a2e"/>

 <rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" rx="12" fill="#0c0b14" stroke="#2c2644"/>
 <text class="h" x="{px0 + 20}" y="{py0 + 26}">VISUAL.MAP</text>
 {rows_svg}
 <circle cx="{px0 + pw / 2:.1f}" cy="{ay + ROWS * CH / 2:.1f}" r="{min(COLS * CW, ROWS * CH) / 2 + 3:.1f}" fill="none" stroke="#2c2644" stroke-dasharray="2 5"/>
 <g clip-path="url(#ac)"><rect class="scan" x="{px0}" y="{ay - 6 - 22}" width="{pw}" height="22" fill="url(#sg)"/></g>

 <rect x="{rx0}" y="{py0}" width="{rw}" height="{ph}" rx="12" fill="#0c0b14" stroke="#2c2644"/>
 <text class="h" x="{rx0 + 24}" y="{py0 + 26}">SYSTEM.INFO</text>
 <circle cx="{rx0 + rw - 56}" cy="{py0 + 22}" r="3.5" fill="#28c840"/><text class="t" x="{rx0 + rw - 46}" y="{py0 + 26}" style="font-size:10px;letter-spacing:1.5px">LIVE</text>
 {f_svg}
 <g class="done"><text class="t" x="{rx0 + 24}" y="{py0 + ph - 14}"><tspan fill="#a78bfa">›</tspan> scan complete</text></g>
 <rect class="cur" x="{rx0 + 142}" y="{py0 + ph - 25}" width="7" height="13" fill="#a78bfa"/>
</g>
"""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Profile scan for {escape(USERNAME)}"><title>Profile scan: {escape(SUBJECT)}</title>'
           f'<style>{css}</style>{body}</svg>')
    xml.dom.minidom.parseString(svg)
    return svg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--portrait", default=None)
    ap.add_argument("--style", choices=["photo", "ascii"], default=None)
    ap.add_argument("--crop", default=None, help="l,t,r,b fractions, e.g. 0.1,0.1,0.9,0.7")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "assets", "scan.svg"))
    a = ap.parse_args()
    global CROP, PORTRAIT, STYLE
    if a.style:
        STYLE = a.style
    global USER_CROP
    if a.crop:
        CROP = USER_CROP = tuple(float(x) for x in a.crop.split(","))
    PORTRAIT = a.portrait
    if a.sample:
        data = SAMPLE
    else:
        try:
            data = fetch(USERNAME)
        except Exception as e:
            print("GitHub API unavailable, using sample data:", e)
            data = SAMPLE
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(build(data))
    print("wrote", a.out, data)


if __name__ == "__main__":
    main()
