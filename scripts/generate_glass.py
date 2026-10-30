#!/usr/bin/env python3
"""Generate the static soft-glass images for README.md: the hero, the section
divider and the small category labels on the project cards. Edit HERO /
KICKERS and rerun from the repo root:

    python3 scripts/generate_glass.py

Stats images come from scripts/generate_stats.py instead (needs a token).
"""
from glass import GREEN, THEMES, chip, glass, backdrop, svg, text, text_width, wrap, write

HERO = {
    "name": "Sree Vardhan V",
    "role": ("Full-Stack Developer", "Generative AI Builder"),
    "line": "I build full-stack web apps and AI-powered tools, from the first prototype to a deployed product.",
    "status": "Open to internships and collaborations",
}

# project slug -> category label shown above the card title
KICKERS = {
    "vard-ai": "AI ASSISTANT · MCP",
    "extension-ai": "GENERATIVE AI · DEV TOOL",
    "trustlens-ai": "AGENTIC AI · TRUST",
    "hpl-auction": "REAL-TIME",
    "campus-compass": "FULL-STACK",
    "chitchain": "WEB3 · AI",
}


def hero(t):
    W, H = 1000, 250
    role = "  ·  ".join(HERO["role"])
    lines = wrap(HERO["line"], 15.5, 700)
    y = 154 + (len(lines) - 1) * 22 + 22
    pill, pw = chip(0, 0, HERO["status"], 13, t, dot=GREEN)
    body = [
        backdrop(t, W, H, 26, 50, [(150, 40, 160, 0), (880, 220, 170, 1), (560, -20, 120, 2)]),
        glass(48, 32, W - 96, H - 64, 22, t),
        text(W / 2, 92, HERO["name"], 40, t["text"], 700, "middle", -0.6),
        text(W / 2, 124, role, 17, t["accent_text"], 600, "middle"),
    ]
    body += [text(W / 2, 154 + i * 22, ln, 15.5, t["body"], anchor="middle") for i, ln in enumerate(lines)]
    body.append(f'<g transform="translate({W / 2 - pw / 2:.1f},{y - 4})">{pill}</g>')
    return svg(W, H, f'{HERO["name"]}, {role}. {HERO["line"]} {HERO["status"]}.', "".join(body))


def hero_mobile(t):
    W = 340
    lines = wrap(HERO["line"], 14.5, W - 70)
    y_line = 144
    y_pill = y_line + len(lines) * 20 + 4
    pill, pw = chip(0, 0, HERO["status"], 12, t, dot=GREEN)
    H = y_pill + 26 + 36
    body = [
        backdrop(t, W, H, 22, 36, [(40, 30, 120, 0), (300, H - 20, 130, 1), (220, -10, 80, 2)]),
        glass(14, 14, W - 28, H - 28, 18, t),
        text(W / 2, 74, HERO["name"], 31, t["text"], 700, "middle", -0.5),
    ]
    body += [text(W / 2, 102 + i * 20, r, 15.5, t["accent_text"], 600, "middle") for i, r in enumerate(HERO["role"])]
    body += [text(W / 2, y_line + i * 20, ln, 14.5, t["body"], anchor="middle") for i, ln in enumerate(lines)]
    body.append(f'<g transform="translate({W / 2 - pw / 2:.1f},{y_pill})">{pill}</g>')
    return svg(W, H, f'{HERO["name"]}, {", ".join(HERO["role"])}. {HERO["line"]} {HERO["status"]}.', "".join(body))


def divider(t):
    """Hairline that fades in from both edges, with a small glass dot in the middle."""
    W, H = 1000, 24
    body = (
        '<defs><linearGradient id="line" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{t["accent"]}" stop-opacity="0.55"/>'
        f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient></defs>'
        f'<rect x="0" y="{H / 2 - 0.75}" width="{W}" height="1.5" fill="url(#line)"/>'
        f'<rect x="{W / 2 - 22}" y="{H / 2 - 5}" width="44" height="10" rx="5" fill="{t["chip_bg"]}" '
        f'stroke="{t["accent"]}" stroke-opacity="0.6"/>'
    )
    return svg(W, H, "Section divider", body)


def kicker(label, t):
    size = 11
    w = text_width(label, size) + 1.4 * len(label) + 28
    h = 24
    body = (f'<rect x="0.5" y="0.5" width="{w - 1:.1f}" height="{h - 1}" rx="{h / 2}" fill="{t["chip_bg"]}" '
            f'stroke="{t["chip_edge"]}"/>'
            + text(w / 2, 16, label, size, t["accent_text"], 650, "middle", 1.4))
    return svg(round(w), h, label, body)


def main():
    for mode, t in THEMES.items():
        write(f"hero-{mode}.svg", hero(t))
        write(f"hero-mobile-{mode}.svg", hero_mobile(t))
        write(f"divider-{mode}.svg", divider(t))
        for slug, label in KICKERS.items():
            write(f"kicker-{slug}-{mode}.svg", kicker(label, t))


if __name__ == "__main__":
    main()
