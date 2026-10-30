#!/usr/bin/env python3
"""Generate the soft-glassmorphism SVGs used by README.md.

Each image is written twice, *-light.svg and *-dark.svg, and the README picks
one with <picture> + prefers-color-scheme. Static SVG, system fonts, no JS, so
GitHub renders it as-is. Stdlib only. Edit HEADER / PROJECTS and rerun from
the repo root:

    python3 scripts/generate_glass.py
"""
import os

ASSETS = "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

THEMES = {
    "light": {
        "bg0": "#EEF5FF", "bg1": "#F8FBFF",
        "glass": "#FFFFFF", "glass_op": 0.55, "edge_op": 0.95,
        "border": "#C9DCF5",
        "title": "#0F2744", "sub": "#2F5C9E", "body": "#4A6488", "muted": "#6E86A8",
        "chip_bg": "#E3F1FF", "chip_text": "#1E4F8F", "chip_edge": "#BFD9F7",
        "blob_op": 0.55,
    },
    "dark": {
        "bg0": "#0A1630", "bg1": "#0D1F3E",
        "glass": "#FFFFFF", "glass_op": 0.07, "edge_op": 0.22,
        "border": "#2A4470",
        "title": "#EAF2FF", "sub": "#8EC5FF", "body": "#B4C6E2", "muted": "#8197BA",
        "chip_bg": "#16305A", "chip_text": "#BFE3FF", "chip_edge": "#2D4E80",
        "blob_op": 0.45,
    },
}

BLUE, CYAN, INDIGO, SKY = "#5B8DEF", "#22D3EE", "#A5B4FC", "#7DD3FC"

HEADER = {
    "name": "Vardhan V",
    "role": "Full-Stack Developer  ·  Generative AI Builder",
    "line": "Production-ready web apps, real-time systems and AI-powered developer tools",
    "pill": "Open to internships · collaborations · freelance",
}

# (slug, kicker, title, description, chips, blob colours)
PROJECTS = [
    ("campus-compass", "FULL-STACK · WEB", "Campus Compass",
     "College discovery and comparison for Indian students: search, filter, compare and review, with smart recommendations.",
     ["Next.js", "PostgreSQL", "Prisma", "NextAuth"], (BLUE, SKY)),
    ("ipl-auction", "REAL-TIME", "IPL Auction",
     "Live multiplayer auction rooms. Share a code, claim franchises and bid in real time from any phone.",
     ["Next.js", "Socket.IO", "Prisma", "MySQL"], (CYAN, BLUE)),
    ("trustlens-ai", "AI · AGENTS", "TrustLens AI",
     "Checks screenshots, messages and viral claims, and returns an explainable, evidence-backed trust report.",
     ["Python", "CrewAI", "Gemini"], (INDIGO, CYAN)),
    ("chitchain", "WEB3 · AI", "ChitChain",
     "A trust-minimised chit fund. The pot lives in a smart contract and an AI risk engine prices collateral.",
     ["TypeScript", "Smart contracts", "AI agents"], (SKY, INDIGO)),
]


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def text_width(s, size):
    """Rough sans-serif width estimate, erring wide."""
    w = 0.0
    for ch in s:
        if ch == " ":
            w += 0.28
        elif ch in ".,·:'-/()":
            w += 0.30
        elif ch in "mwMW":
            w += 0.86
        elif ch in "iljtfrI":
            w += 0.32
        elif ch.isupper() or ch.isdigit():
            w += 0.64
        else:
            w += 0.54
    return w * size


def wrap(s, size, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if text_width(trial, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def defs(t, blur, blobs):
    """Background gradient, blur filter, glass sheen and the blobs behind the glass."""
    return (
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>'
        f'<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{t["edge_op"] * 0.35:.3f}"/>'
        f'<stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{blur}"/></filter>'
        "</defs>"
        + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{t["blob_op"]}" filter="url(#blur)"/>'
                  for x, y, r, c in blobs)
    )


def glass(x, y, w, h, rx, t):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#sheen)"/>'
        f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" '
        f'stroke="#FFFFFF" stroke-opacity="{t["edge_op"]}"/>'
    )


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(label)}">{body}</svg>')


def header(t):
    W, H = 1000, 270
    blobs = [(170, 50, 150, BLUE), (850, 230, 160, CYAN), (560, -10, 120, INDIGO), (60, 260, 90, SKY)]
    pill = HEADER["pill"]
    pw = text_width(pill, 13) + 56
    body = (
        f'<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/>'
        f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="28"/></clipPath>'
        f'<g clip-path="url(#clip)">{defs(t, 46, blobs)}</g>'
        + glass(56, 40, W - 112, H - 80, 24, t)
        + f'<text x="{W / 2}" y="104" text-anchor="middle" font-family="{FONT}" font-size="44" font-weight="650" '
          f'letter-spacing="-0.5" fill="{t["title"]}">{esc(HEADER["name"])}</text>'
        + f'<text x="{W / 2}" y="138" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="500" '
          f'fill="{t["sub"]}">{esc(HEADER["role"])}</text>'
        + f'<text x="{W / 2}" y="166" text-anchor="middle" font-family="{FONT}" font-size="14.5" '
          f'fill="{t["body"]}">{esc(HEADER["line"])}</text>'
        + f'<rect x="{W / 2 - pw / 2}" y="184" width="{pw}" height="28" rx="14" fill="{t["chip_bg"]}" '
          f'stroke="{t["chip_edge"]}"/>'
        + f'<circle cx="{W / 2 - pw / 2 + 16}" cy="198" r="3.5" fill="#22C55E"/>'
        + f'<text x="{W / 2 + 9}" y="202.5" text-anchor="middle" font-family="{FONT}" font-size="13" '
          f'fill="{t["chip_text"]}">{esc(pill)}</text>'
    )
    return svg(W, H, f'{HEADER["name"]} — {HEADER["role"]}', body)


def card(p, t):
    _, kicker, title, desc, chips, (c1, c2) = p
    W, H = 480, 230
    blobs = [(70, 40, 110, c1), (430, 210, 120, c2)]
    pad = 28
    lines = wrap(desc, 14.5, W - 2 * pad)[:3]
    parts = [
        f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>',
        f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{defs(t, 38, blobs)}</g>',
        glass(0, 0, W, H, 22, t),
        f'<text x="{pad}" y="44" font-family="{FONT}" font-size="11" font-weight="600" letter-spacing="1.6" '
        f'fill="{t["sub"]}">{esc(kicker)}</text>',
        f'<text x="{pad}" y="76" font-family="{FONT}" font-size="23" font-weight="650" letter-spacing="-0.3" '
        f'fill="{t["title"]}">{esc(title)}</text>',
        f'<text x="{W - pad}" y="76" text-anchor="end" font-family="{FONT}" font-size="20" '
        f'fill="{t["muted"]}">↗</text>',
    ]
    for i, ln in enumerate(lines):
        parts.append(f'<text x="{pad}" y="{106 + i * 21}" font-family="{FONT}" font-size="14.5" '
                     f'fill="{t["body"]}">{esc(ln)}</text>')
    x, y = pad, H - 50
    for c in chips:
        cw = text_width(c, 12.5) + 24
        parts.append(f'<rect x="{x}" y="{y}" width="{cw:.1f}" height="26" rx="13" fill="{t["chip_bg"]}" '
                     f'stroke="{t["chip_edge"]}"/>'
                     f'<text x="{x + cw / 2:.1f}" y="{y + 17.5}" text-anchor="middle" font-family="{FONT}" '
                     f'font-size="12.5" font-weight="500" fill="{t["chip_text"]}">{esc(c)}</text>')
        x += cw + 8
    return svg(W, H, f"{title}: {desc} Stack: {', '.join(chips)}", "".join(parts))


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"wrote {path} ({len(content):,} bytes)")


def main():
    for mode, t in THEMES.items():
        write(f"header-{mode}.svg", header(t))
        for p in PROJECTS:
            write(f"card-{p[0]}-{mode}.svg", card(p, t))


if __name__ == "__main__":
    main()
