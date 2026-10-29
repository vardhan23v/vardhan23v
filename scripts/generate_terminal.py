#!/usr/bin/env python3
"""Generate the "Fremen Terminal" card (assets/terminal.svg): a fake shell that
types commands and prints answers line by line on a loop. SMIL clip rects do
the typing, opacity animations reveal output. Edit SCRIPT and rerun:

    python3 scripts/generate_terminal.py
"""
from common import (EMBER, GOLD, GOLD_HI, LBL_FONT, MONO_FONT, NIGHT, ORANGE, SAND, CREAM,
                    esc, mono_width, reduced_motion, write_svg)

W = 920
FS = 13.5          # font size
LH = 22            # line height
PAD_X, TOP = 30, 74
LOOP = 30.0        # seconds for the whole script
CHAR_T = 0.055     # seconds per typed character
PROMPT = "fremen@arrakis:~$ "

# ("cmd", text)  -> typed with the prompt
# ("out", text)  -> printed instantly after the previous command finishes
# ("gap", "")    -> blank line
SCRIPT = [
    ("cmd", "whoami"),
    ("out", "Sree Vardhan V  ·  full-stack developer  ·  generative-AI builder"),
    ("gap", ""),
    ("cmd", "cat stillsuit.cfg"),
    ("out", "stack   = typescript · next.js · node · python · java"),
    ("out", "ai      = agents · mcp · crewai · gemini · groq · llama"),
    ("out", "data    = postgres · mysql · prisma · redis · socket.io"),
    ("gap", ""),
    ("cmd", "./harvest --status"),
    ("out", "▸ building  AI-powered web apps, dev tools, realtime systems"),
    ("out", "▸ shipping  on vercel · railway · aws"),
    ("out", "▸ open to   internships · collaborations · freelance"),
    ("gap", ""),
    ("cmd", "echo $MOTTO"),
    ("out", "“The spice must flow.”"),
]


def build():
    lines = []
    t = 1.0
    y = TOP
    cw = mono_width("x", FS)
    for kind, text in SCRIPT:
        if kind == "gap":
            y += LH * 0.6
            continue
        if kind == "cmd":
            px = PAD_X + mono_width(PROMPT, FS)
            w = mono_width(text, FS) + 4
            dur_type = len(text) * CHAR_T
            t_end = t + dur_type
            kt = [0, t / LOOP, t_end / LOOP, (LOOP - 0.8) / LOOP, 1]
            kts = ";".join(f"{k:.4f}" for k in kt)
            cid = f"c{len(lines)}"
            lines.append(
                # prompt appears when its turn comes
                f'<text x="{PAD_X}" y="{y}" font-family="{MONO_FONT}" font-size="{FS}" fill="{GOLD}" opacity="0">'
                f'<tspan fill="{EMBER}">fremen</tspan><tspan fill="{GOLD}" opacity="0.7">@arrakis</tspan>'
                f'<tspan fill="{SAND}" opacity="0.6">:~$</tspan>'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t / LOOP:.4f};{(t + 0.05) / LOOP:.4f};{(LOOP - 0.8) / LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/>'
                f'</text>'
                f'<clipPath id="{cid}"><rect x="{px:.1f}" y="{y - 15}" width="0" height="20">'
                f'<animate attributeName="width" values="0;0;{w:.0f};{w:.0f};0" keyTimes="{kts}" calcMode="linear" dur="{LOOP}s" repeatCount="indefinite"/>'
                f'</rect></clipPath>'
                f'<g clip-path="url(#{cid})"><text x="{px:.1f}" y="{y}" font-family="{MONO_FONT}" font-size="{FS}" fill="{CREAM}">{esc(text)}</text></g>'
                # block cursor rides along while typing, then parks until the output prints
                f'<rect x="{px:.1f}" y="{y - 12}" width="{cw:.1f}" height="16" fill="{GOLD_HI}" opacity="0">'
                f'<animate attributeName="x" values="{px:.1f};{px:.1f};{px + w - 4:.1f};{px + w - 4:.1f};{px:.1f}" keyTimes="{kts}" calcMode="linear" dur="{LOOP}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;0;0.9;0.9;0;0" keyTimes="0;{t / LOOP:.4f};{(t + 0.05) / LOOP:.4f};{(t_end + 0.45) / LOOP:.4f};{(t_end + 0.5) / LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/>'
                f'</rect>'
            )
            t = t_end + 0.55
        else:
            kt_show = t / LOOP
            lines.append(
                f'<text x="{PAD_X + 8}" y="{y}" font-family="{MONO_FONT}" font-size="{FS}" fill="{SAND}" opacity="0">{esc(text)}'
                f'<animate attributeName="opacity" values="0;0;0.92;0.92;0" keyTimes="0;{kt_show:.4f};{kt_show + 0.004:.4f};{(LOOP - 0.8) / LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/>'
                f'</text>'
            )
            t += 0.28
        y += LH
    # final idle prompt with blinking cursor
    lines.append(
        f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t / LOOP:.4f};{(t + 0.05) / LOOP:.4f};{(LOOP - 0.8) / LOOP:.4f};1" dur="{LOOP}s" repeatCount="indefinite"/>'
        f'<text x="{PAD_X}" y="{y}" font-family="{MONO_FONT}" font-size="{FS}"><tspan fill="{EMBER}">fremen</tspan><tspan fill="{GOLD}" opacity="0.7">@arrakis</tspan><tspan fill="{SAND}" opacity="0.6">:~$</tspan></text>'
        f'<rect class="blink" x="{PAD_X + mono_width(PROMPT, FS):.1f}" y="{y - 12}" width="{cw:.1f}" height="16" fill="{GOLD_HI}"/></g>'
    )
    H = int(y + 28)
    return "".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Terminal: whoami, tech stack, status and motto">',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120b06"/><stop offset="1" stop-color="{NIGHT}"/></linearGradient>',
        '<filter id="ember" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>',
        '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" opacity="0.025"/></pattern>',
        '</defs>',
        '<style>'
        '.em{animation:br 6s ease-in-out infinite alternate}@keyframes br{from{opacity:.14}to{opacity:.38}}'
        '.blink{animation:blink 1s steps(1) infinite}@keyframes blink{0%,49%{opacity:.9}50%,100%{opacity:0}}'
        + reduced_motion('.em', '.blink') + '</style>',
        f'<rect class="em" x="6" y="6" width="{W - 12}" height="{H - 12}" rx="14" fill="{ORANGE}" filter="url(#ember)"/>',
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="12" fill="url(#bg)" stroke="{GOLD}" stroke-opacity="0.55"/>',
        # title bar
        f'<path d="M6 18 a12 12 0 0 1 12 -12 h{W - 36} a12 12 0 0 1 12 12 v22 h-{W - 12} z" fill="#1a1109"/>',
        f'<rect x="6" y="40" width="{W - 12}" height="1" fill="{GOLD}" opacity="0.25"/>',
        f'<circle cx="28" cy="23" r="5" fill="#c2422d"/><circle cx="46" cy="23" r="5" fill="{EMBER}"/><circle cx="64" cy="23" r="5" fill="{GOLD}"/>',
        f'<text x="{W / 2}" y="27" text-anchor="middle" font-family="{LBL_FONT}" font-size="10" letter-spacing="3" fill="{GOLD}" opacity="0.8">FREMEN TERMINAL — SIETCH TABR</text>',
        f'<rect x="{W - 42}" y="19" width="8" height="8" transform="rotate(45 {W - 38} 23)" fill="{GOLD}"/>',
        *lines,
        f'<rect x="7" y="41" width="{W - 14}" height="{H - 48}" rx="0" fill="url(#scan)"/>',
        '</svg>',
    ])


if __name__ == "__main__":
    write_svg("terminal.svg", build())
