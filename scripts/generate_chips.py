#!/usr/bin/env python3
"""Generate the themed contact chips under the header
(assets/chip-portfolio.svg, assets/chip-linkedin.svg). Stdlib only."""
import os

GOLD = "#D4A574"
EMBER = "#C2622D"
SAND = "#E8DCC4"
LBL_FONT = "Copperplate, 'Trajan Pro', Georgia, serif"
VAL_FONT = "Georgia, 'Times New Roman', serif"

CHIPS = [
    ("chip-portfolio.svg", "PORTFOLIO", "vardhan-v-portfilo.vercel.app", "Portfolio: vardhan-v-portfilo.vercel.app"),
    ("chip-linkedin.svg", "LINKEDIN", "in/vardhan-v23", "LinkedIn: in/vardhan-v23"),
]

H = 44


def tw(s, size, upper_spacing=0.0):
    w = 0.0
    for ch in s:
        if ch == " ":
            w += 0.30
        elif ch in "./-":
            w += 0.34
        elif ch.isupper():
            w += 0.72
        elif ch.isdigit():
            w += 0.56
        elif ch in "mw":
            w += 0.85
        elif ch in "iljt":
            w += 0.34
        else:
            w += 0.55
    return w * size + upper_spacing * max(len(s) - 1, 0)


def chip(label, value, aria):
    lbl_w = tw(label, 10, 2.5)
    val_w = tw(value, 13)
    x_dia = 22
    x_lbl = 36
    x_val = x_lbl + lbl_w + 12
    W = int(x_val + val_w + 22)
    return "".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{aria}">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
        '<stop offset="0" stop-color="#1a1109"/><stop offset="1" stop-color="#0A0A0A"/>',
        '</linearGradient></defs>',
        '<style>',
        '.in{animation:in .7s ease-out .1s both}',
        '@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}',
        '@media (prefers-reduced-motion:reduce){.in{animation:none}}',
        '</style>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="{(H - 1) / 2}" fill="url(#bg)" '
        f'stroke="{GOLD}" stroke-opacity="0.6">'
        f'<animate attributeName="stroke" values="{GOLD};{EMBER};{GOLD}" dur="9s" repeatCount="indefinite"/></rect>',
        '<g class="in">',
        f'<rect x="{x_dia - 3.5}" y="{H / 2 - 3.5}" width="7" height="7" transform="rotate(45 {x_dia} {H / 2})" fill="{EMBER}"/>',
        f'<text x="{x_lbl}" y="{H / 2 + 4}" font-family="{LBL_FONT}" font-size="10" letter-spacing="2.5" fill="{GOLD}">{label}</text>',
        f'<text x="{x_val:.0f}" y="{H / 2 + 5}" font-family="{VAL_FONT}" font-size="13" fill="{SAND}">{value}</text>',
        '</g></svg>',
    ]), W


if __name__ == "__main__":
    for fname, label, value, aria in CHIPS:
        svg, W = chip(label, value, aria)
        with open(os.path.join("assets", fname), "w") as f:
            f.write(svg)
        print(f"wrote assets/{fname} ({W}x{H})")
