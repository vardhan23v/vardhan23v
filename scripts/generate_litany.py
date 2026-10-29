#!/usr/bin/env python3
"""Generate the Litany band (assets/litany.svg): the Bene Gesserit line typed
out letter by letter with an animated clip rect, held, then wiped. Pure SMIL
+ CSS so it survives GitHub's SVG sandbox.

    python3 scripts/generate_litany.py
"""
from common import EMBER, GOLD, GOLD_HI, LBL_FONT, NIGHT, ORANGE, SAND, VAL_FONT, esc, reduced_motion, rng, text_width, write_svg

W, H = 1200, 96
QUOTE = "“I must not fear. Fear is the mind-killer.”"
ATTRIB = "BENE GESSERIT LITANY AGAINST FEAR"
CYCLE = 16.0   # seconds for type + hold + wipe
TYPE_T = 4.2
HOLD_END = 13.6


def embers(n=14, seed=23):
    r = rng(seed)
    out = []
    for _ in range(n):
        cx = r.uniform(40, W - 40)
        dur = r.uniform(7, 12)
        delay = r.uniform(0, 9)
        rad = r.uniform(1, 2)
        out.append(
            f'<circle cx="{cx:.0f}" cy="{H + 6}" r="{rad:.1f}" fill="{GOLD}" opacity="0">'
            f'<animate attributeName="cy" values="{H + 6};-10" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;.7;.3;0" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{cx:.0f};{cx - 30:.0f}" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return "".join(out)


def build():
    size = 21
    qw = text_width(QUOTE, size) * 1.04 + 10
    x0 = 600 - qw / 2
    y = 44
    kt = [0, TYPE_T / CYCLE, HOLD_END / CYCLE, (HOLD_END + 0.6) / CYCLE, 1]
    kts = ";".join(f"{k:.4f}" for k in kt)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{esc(QUOTE)} {esc(ATTRIB.title())}">',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140c06"/><stop offset="1" stop-color="{NIGHT}"/></linearGradient>',
        f'<linearGradient id="rl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0.7"/></linearGradient>',
        f'<linearGradient id="rr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.7"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>',
        f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{ORANGE}" stop-opacity="0.28"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>',
        f'<clipPath id="type"><rect x="{x0:.1f}" y="{y - 26}" width="0" height="36">'
        f'<animate attributeName="width" values="0;{qw:.0f};{qw:.0f};0;0" keyTimes="{kts}" calcMode="linear" dur="{CYCLE}s" repeatCount="indefinite"/>'
        '</rect></clipPath>',
        '</defs>',
        '<style>'
        '.att{animation:att 1.2s ease-out 4.4s both}@keyframes att{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}'
        '.cur{animation:blink 1s steps(1) infinite}@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}'
        '.gl{animation:gl 7s ease-in-out infinite alternate}@keyframes gl{from{opacity:.5}to{opacity:1}}'
        + reduced_motion('.att', '.cur', '.gl') +
        '</style>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="url(#bg)" stroke="{GOLD}" stroke-opacity="0.35"/>',
        f'<ellipse class="gl" cx="600" cy="{H / 2}" rx="420" ry="{H}" fill="url(#glow)"/>',
        # side rules with diamonds
        f'<rect x="40" y="{H / 2 - 0.5}" width="{x0 - 70:.0f}" height="1" fill="url(#rl)"/>',
        f'<rect x="{x0 + qw + 30:.0f}" y="{H / 2 - 0.5}" width="{W - 40 - (x0 + qw + 30):.0f}" height="1" fill="url(#rr)"/>',
        f'<rect x="{x0 - 26:.0f}" y="{H / 2 - 4}" width="8" height="8" transform="rotate(45 {x0 - 22:.0f} {H / 2})" fill="{EMBER}"/>',
        f'<rect x="{x0 + qw + 14:.0f}" y="{H / 2 - 4}" width="8" height="8" transform="rotate(45 {x0 + qw + 18:.0f} {H / 2})" fill="{EMBER}"/>',
        # typed quote
        f'<g clip-path="url(#type)"><text x="600" y="{y}" text-anchor="middle" font-family="{VAL_FONT}" '
        f'font-style="italic" font-size="{size}" fill="{SAND}">{esc(QUOTE)}</text></g>',
        # cursor rides the clip edge
        f'<rect class="cur" x="{x0:.1f}" y="{y - 17}" width="2" height="22" fill="{GOLD_HI}">'
        f'<animate attributeName="x" values="{x0:.1f};{x0 + qw - 8:.1f};{x0 + qw - 8:.1f};{x0:.1f};{x0:.1f}" keyTimes="{kts}" calcMode="linear" dur="{CYCLE}s" repeatCount="indefinite"/>'
        '</rect>',
        f'<text class="att" x="600" y="{y + 28}" text-anchor="middle" font-family="{LBL_FONT}" font-size="9.5" '
        f'letter-spacing="3.5" fill="{GOLD}" opacity="0.75">{esc(ATTRIB)}</text>',
        embers(),
        '</svg>',
    ]
    return "".join(svg)


if __name__ == "__main__":
    write_svg("litany.svg", build())
