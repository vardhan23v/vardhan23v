#!/usr/bin/env python3
"""Generate the static soft-glass images for README.md: the hero, the section
divider and the small category labels on the project cards. Edit HERO /
KICKERS and rerun from the repo root:

    python3 scripts/generate_glass.py

Stats images come from scripts/generate_stats.py instead (needs a token).
"""
from glass import GREEN, THEMES, chip, glass, svg, text, text_width, wrap, write

HERO = {
    "name": "Sree Vardhan V",
    "role": ("Full-Stack Developer", "Generative AI Builder"),
    "line": "I build full-stack web apps and AI-powered tools, from the first prototype to a deployed product.",
    "status": "Open to collaborations",
}

# project slug -> category label shown above the card title. Keep them short:
# on phones each card column is ~150 px and a longer label gets scaled down.
KICKERS = {
    "vard-ai": "AI ASSISTANT",
    "extension-ai": "AI DEV TOOL",
    "trustlens-ai": "AGENTIC AI",
    "hpl-auction": "REAL-TIME",
    "campus-compass": "FULL-STACK",
    "chitchain": "WEB3 · AI",
}


# Hero aurora: (base gradient, bands of (from, to) colours, band opacity, grid colour, grid opacity,
# glass fill, glass opacity). The glass is denser than elsewhere so text stays at WCAG AA over the
# brightest band: frosted white in light mode, smoked navy in dark mode.
AURORA = {
    "light": (("#F8FAFC", "#EFF6FF"), (("#60A5FA", "#22D3EE"), ("#A5B4FC", "#93C5FD"), ("#67E8F9", "#38BDF8")),
              0.6, "#0284C7", 0.12, "#FFFFFF", 0.66),
    "dark": (("#070D1A", "#0B1220"), (("#2563EB", "#06B6D4"), ("#4F46E5", "#1D4ED8"), ("#0891B2", "#22D3EE")),
             0.55, "#7DD3FC", 0.10, "#0B1220", 0.45),
}


def aurora(mode, t, W, H, rx, blur, grid):
    """Flowing blurred colour bands over a faint grid that fades out towards the edges."""
    (b0, b1), bands, band_op, grid_color, grid_op, _, _ = AURORA[mode]
    # (centre x, centre y, half-width, half-height, rotation) as fractions of the frame
    shapes = [(0.22, 0.15, 0.42, 0.16, -14), (0.62, 0.05, 0.36, 0.14, 10), (0.80, 0.92, 0.44, 0.18, -8)]
    defs = [
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{b0}"/>'
        f'<stop offset="1" stop-color="{b1}"/></linearGradient>',
        '<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{t["edge_op"] * 0.4:.3f}"/>'
        '<stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>',
        f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{blur}"/></filter>',
        f'<clipPath id="clip"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>',
        f'<pattern id="grid" width="{grid}" height="{grid}" patternUnits="userSpaceOnUse">'
        f'<path d="M {grid} 0 L 0 0 0 {grid}" fill="none" stroke="{grid_color}" stroke-width="1"/></pattern>',
        '<radialGradient id="fade" cx="0.5" cy="0.5" r="0.6"><stop offset="0" stop-color="#FFFFFF"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>',
        f'<mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>',
    ]
    for i, (c0, c1) in enumerate(bands):
        defs.append(f'<linearGradient id="band{i}" x1="0" x2="1"><stop offset="0" stop-color="{c0}"/>'
                    f'<stop offset="1" stop-color="{c1}"/></linearGradient>')
    body = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
            f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity="{grid_op}" mask="url(#gridMask)"/>']
    for i, (cx, cy, rx_, ry_, rot) in enumerate(shapes):
        x, y = cx * W, cy * H
        body.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx_ * W:.0f}" ry="{ry_ * W:.0f}" fill="url(#band{i})" '
                    f'opacity="{band_op}" filter="url(#blur)" transform="rotate({rot} {x:.0f} {y:.0f})"/>')
    return ("<defs>" + "".join(defs) + "</defs>"
            + f'<g clip-path="url(#clip)">{"".join(body)}</g>'
            + f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="{rx}" fill="none" stroke="{t["frame"]}"/>')


def hero_glass(mode, t):
    return {**t, "glass_fill": AURORA[mode][5], "glass_op": AURORA[mode][6]}


def hero(mode, t):
    W, H = 1000, 250
    role = "  ·  ".join(HERO["role"])
    lines = wrap(HERO["line"], 15.5, 700)
    y = 154 + (len(lines) - 1) * 22 + 22
    pill, pw = chip(0, 0, HERO["status"], 13, t, dot=GREEN)
    body = [
        aurora(mode, t, W, H, 26, 42, 28),
        glass(48, 32, W - 96, H - 64, 22, hero_glass(mode, t)),
        text(W / 2, 92, HERO["name"], 40, t["text"], 700, "middle", -0.6),
        text(W / 2, 124, role, 17, t["accent_text"], 600, "middle"),
    ]
    body += [text(W / 2, 154 + i * 22, ln, 15.5, t["body"], anchor="middle") for i, ln in enumerate(lines)]
    body.append(f'<g transform="translate({W / 2 - pw / 2:.1f},{y - 4})">{pill}</g>')
    return svg(W, H, f'{HERO["name"]}, {role}. {HERO["line"]} {HERO["status"]}.', "".join(body))


def hero_mobile(mode, t):
    W = 340
    lines = wrap(HERO["line"], 14.5, W - 70)
    y_line = 144
    y_pill = y_line + len(lines) * 20 + 4
    pill, pw = chip(0, 0, HERO["status"], 12, t, dot=GREEN)
    H = y_pill + 26 + 36
    body = [
        aurora(mode, t, W, H, 22, 26, 22),
        glass(14, 14, W - 28, H - 28, 18, hero_glass(mode, t)),
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
        write(f"hero-{mode}.svg", hero(mode, t))
        write(f"hero-mobile-{mode}.svg", hero_mobile(mode, t))
        write(f"divider-{mode}.svg", divider(t))
        for slug, label in KICKERS.items():
            write(f"kicker-{slug}-{mode}.svg", kicker(label, t))


if __name__ == "__main__":
    main()
