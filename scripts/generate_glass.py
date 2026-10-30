#!/usr/bin/env python3
"""Generate the soft-glassmorphism SVGs used by README.md.

Every image comes in four variants: desktop and mobile layouts, each light and
dark. The README picks one with <picture> sources on max-width and
prefers-color-scheme, because SVG text scales with the image and a desktop
layout shrunk to a phone column is unreadable. Static SVG, system fonts, no
JS, so GitHub renders it as-is. Stdlib only. Edit HEADER / PROJECTS and rerun
from the repo root:

    python3 scripts/generate_glass.py
"""
import glob
import os

ASSETS = "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

# Text colours meet WCAG AA (4.5:1) against the brightest blob seen through the glass.
THEMES = {
    "light": {
        "bg0": "#EEF5FF", "bg1": "#F8FBFF",
        "glass_op": 0.55, "edge_op": 0.95,
        "title": "#0F2744", "sub": "#2F5C9E", "body": "#4A6488", "muted": "#6E86A8",
        "chip_bg": "#E3F1FF", "chip_text": "#1E4F8F", "chip_edge": "#BFD9F7",
        "blob_op": 0.55,
    },
    "dark": {
        "bg0": "#0A1630", "bg1": "#0D1F3E",
        "glass_op": 0.07, "edge_op": 0.22,
        "title": "#EAF2FF", "sub": "#A9D6FF", "body": "#D3DEEF", "muted": "#8197BA",
        "chip_bg": "#16305A", "chip_text": "#BFE3FF", "chip_edge": "#2D4E80",
        "blob_op": 0.30,
    },
}

BLUE, CYAN, INDIGO, SKY = "#5B8DEF", "#22D3EE", "#A5B4FC", "#7DD3FC"

HEADER = {
    "name": "Vardhan V",
    "role": ("Full-Stack Developer", "Generative AI Builder"),
    "line": "Production-ready web apps, real-time systems and AI-powered developer tools",
    "pill": "Open to internships · collaborations · freelance",
}

# (slug, kicker, title, description, chips, blob colours)
PROJECTS = [
    ("campus-compass", "FULL-STACK · WEB", "Campus Compass",
     "College discovery and comparison for Indian students: search, filter, compare and review, with smart recommendations.",
     ["Next.js", "PostgreSQL", "Prisma", "NextAuth"], (BLUE, SKY)),
    ("hpl-auction", "REAL-TIME", "HPL Auction",
     "Live cricket auction for a hostel league: WebSocket bidding, a server-authoritative timer and purse engine, and captain dashboards.",
     ["Next.js", "Socket.IO", "Prisma", "MySQL"], (CYAN, BLUE)),
    ("trustlens-ai", "AI · AGENTS", "TrustLens AI",
     "Checks screenshots, messages and viral claims, and returns an explainable, evidence-backed trust report.",
     ["Python", "CrewAI", "Gemini"], (INDIGO, CYAN)),
    ("chitchain", "WEB3 · AI", "ChitChain",
     "A trust-minimised chit fund. The pot lives in a smart contract and an AI risk engine prices collateral.",
     ["TypeScript", "Smart contracts", "AI agents"], (SKY, INDIGO)),
]

# Layout per variant. Desktop is drawn for the ~800 px README column, mobile for ~280 px.
LAYOUTS = {
    "": {"card_w": 900, "pad": 32, "kicker": 12, "title": 26, "body": 16, "lh": 23, "chip": 13.5},
    "-mobile": {"card_w": 340, "pad": 22, "kicker": 11, "title": 21, "body": 15, "lh": 21, "chip": 12.5},
}


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


def text(x, y, s, size, fill, weight=400, anchor="start", spacing=0):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{spacing}" fill="{fill}">{esc(s)}</text>')


def backdrop(t, w, h, rx, blur, blobs):
    """Gradient background with blurred colour blobs, clipped to the rounded frame."""
    return (
        "<defs>"
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>'
        '<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{t["edge_op"] * 0.35:.3f}"/>'
        '<stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{blur}"/></filter>'
        f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
        "</defs>"
        f'<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="url(#bg)"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{t["blob_op"]}" filter="url(#blur)"/>'
                  for x, y, r, c in blobs)
        + "</g>"
    )


def glass(x, y, w, h, rx, t):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#FFFFFF" fill-opacity="{t["glass_op"]}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#sheen)"/>'
        f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" '
        f'stroke="#FFFFFF" stroke-opacity="{t["edge_op"]}"/>'
    )


def pill(cx, y, label, size, t):
    """Status pill with a green dot, centred on cx."""
    pw = text_width(label, size) + 56
    x = cx - pw / 2
    return (f'<rect x="{x:.1f}" y="{y}" width="{pw:.1f}" height="{size * 2.15:.1f}" rx="{size * 1.07:.1f}" '
            f'fill="{t["chip_bg"]}" stroke="{t["chip_edge"]}"/>'
            f'<circle cx="{x + 16:.1f}" cy="{y + size * 1.07:.1f}" r="3.5" fill="#22C55E"/>'
            + text(cx + 9, y + size * 1.45, label, size, t["chip_text"], anchor="middle"))


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h:.0f}" viewBox="0 0 {w} {h:.0f}" '
            f'role="img" aria-label="{esc(label)}">{body}</svg>')


def header(t):
    W, H = 1000, 270
    blobs = [(170, 50, 150, BLUE), (850, 230, 160, CYAN), (560, -10, 120, INDIGO), (60, 260, 90, SKY)]
    role = "  ·  ".join(HEADER["role"])
    body = (
        backdrop(t, W, H, 28, 46, blobs)
        + glass(56, 40, W - 112, H - 80, 24, t)
        + text(W / 2, 104, HEADER["name"], 44, t["title"], 650, "middle", -0.5)
        + text(W / 2, 138, role, 18, t["sub"], 500, "middle")
        + text(W / 2, 166, HEADER["line"], 14.5, t["body"], anchor="middle")
        + pill(W / 2, 184, HEADER["pill"], 13, t)
    )
    return svg(W, H, f'{HEADER["name"]}, {role}', body)


def header_mobile(t):
    W = 340
    lines = wrap(HEADER["line"], 14, W - 64)
    y_line = 150
    y_pill = y_line + len(lines) * 19 + 8
    H = y_pill + 26 + 40
    blobs = [(40, 30, 110, BLUE), (310, H - 20, 120, CYAN), (230, -10, 80, INDIGO)]
    body = [backdrop(t, W, H, 24, 34, blobs), glass(14, 14, W - 28, H - 28, 20, t),
            text(W / 2, 74, HEADER["name"], 36, t["title"], 650, "middle", -0.5)]
    for i, r in enumerate(HEADER["role"]):
        body.append(text(W / 2, 104 + i * 21, r, 16, t["sub"], 500, "middle"))
    for i, ln in enumerate(lines):
        body.append(text(W / 2, y_line + i * 19, ln, 14, t["body"], anchor="middle"))
    body.append(pill(W / 2, y_pill, HEADER["pill"], 11.5, t))
    return svg(W, H, f'{HEADER["name"]}, {", ".join(HEADER["role"])}', "".join(body))


def body_lines(desc, lay):
    return wrap(desc, lay["body"], lay["card_w"] - 2 * lay["pad"])


def card(p, t, lay, n_lines):
    """n_lines reserves the same body height on every card so a stack lines up."""
    _, kicker, title, desc, chips, (c1, c2) = p
    W, pad = lay["card_w"], lay["pad"]
    lines = body_lines(desc, lay)
    y_title = pad + lay["kicker"] + 8 + lay["title"]
    y_body = y_title + lay["lh"] + 8
    # chips wrap onto extra rows on narrow layouts
    ch_h, gap = lay["chip"] * 2, 8
    rows, row, x = [], [], 0.0
    for c in chips:
        cw = text_width(c, lay["chip"]) + 24
        if row and x + cw > W - 2 * pad:
            rows.append(row)
            row, x = [], 0.0
        row.append((c, cw, x))
        x += cw + gap
    rows.append(row)
    y_chips = y_body + (max(n_lines, len(lines)) - 1) * lay["lh"] + 22
    H = y_chips + len(rows) * (ch_h + gap) - gap + pad - 4

    parts = [
        backdrop(t, W, H, 22, 38, [(70, 40, 110, c1), (W - 50, H - 20, 120, c2)]),
        glass(0, 0, W, H, 22, t),
        text(pad, pad + lay["kicker"], kicker, lay["kicker"], t["sub"], 600, spacing=1.6),
        text(pad, y_title, title, lay["title"], t["title"], 650, spacing=-0.3),
        text(W - pad, y_title, "↗", lay["title"] - 4, t["muted"], anchor="end"),
    ]
    for i, ln in enumerate(lines):
        parts.append(text(pad, y_body + i * lay["lh"], ln, lay["body"], t["body"]))
    for r, row in enumerate(rows):
        y = y_chips + r * (ch_h + gap)
        for c, cw, cx in row:
            parts.append(f'<rect x="{pad + cx:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch_h}" rx="{ch_h / 2}" '
                         f'fill="{t["chip_bg"]}" stroke="{t["chip_edge"]}"/>')
            parts.append(text(pad + cx + cw / 2, y + ch_h * 0.68, c, lay["chip"], t["chip_text"], 500, "middle"))
    return svg(W, H, f"{title}: {desc} Stack: {', '.join(chips)}.", "".join(parts))


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"wrote {path} ({len(content):,} bytes)")


def main():
    # drop cards for projects no longer in PROJECTS
    keep = {p[0] for p in PROJECTS}
    for path in glob.glob(os.path.join(ASSETS, "card-*.svg")):
        slug = os.path.basename(path)[5:].rsplit("-", 1)[0].removesuffix("-mobile")
        if slug not in keep:
            os.remove(path)
            print(f"removed {path}")
    for mode, t in THEMES.items():
        write(f"header-{mode}.svg", header(t))
        write(f"header-mobile-{mode}.svg", header_mobile(t))
        for suffix, lay in LAYOUTS.items():
            n_lines = max(len(body_lines(p[3], lay)) for p in PROJECTS)
            for p in PROJECTS:
                write(f"card-{p[0]}{suffix}-{mode}.svg", card(p, t, lay, n_lines))


if __name__ == "__main__":
    main()
