#!/usr/bin/env python3
"""Generate the Dune-themed tech-stack card (assets/tech-stillsuit.svg).

Pure Python, no dependencies. Edit SECTIONS and rerun from the repo root:
    python3 scripts/generate_tech.py
"""
import os

OUT = os.path.join("assets", "tech-stillsuit.svg")

GOLD = "#D4A574"
EMBER = "#C2622D"
SAND = "#E8DCC4"
CREAM = "#F6E7C8"
BROWN = "#3D2312"
PILL_FILL = "#160D06"
LBL_FONT = "Copperplate, 'Trajan Pro', Georgia, serif"
VAL_FONT = "Georgia, 'Times New Roman', serif"

SECTIONS = [
    ("◈", "LANGUAGES", ["TypeScript", "JavaScript", "Python", "HTML", "CSS", "SQL"]),
    ("⚔", "FRAMEWORKS", ["React", "Next.js", "TanStack Start", "Node.js", "Express", "Tailwind",
                         "Vite", "Prisma", "Socket.IO", "NextAuth", "Zustand", "Zod",
                         "Vitest", "Jest", "Playwright"]),
    ("☵", "DATA & CLOUD", ["PostgreSQL", "MySQL", "MongoDB", "Supabase", "Redis", "Kafka",
                           "RabbitMQ", "AWS", "Vercel", "Railway", "Cloudinary"]),
    ("👁", "AI / LLM", ["Groq · Llama 3.3", "Gemini 2.0 Flash", "GPT-4o Mini", "Claude API",
                       "MCP Protocol"]),
    ("⚙", "TOOLS", ["VS Code", "Git", "GitHub", "Linux", "Docker", "Figma", "Postman"]),
]

W = 920
PAD = 36
PILL_H = 32
PILL_R = 16
PILL_PAD_X = 15
PILL_GAP = 10
ROW_GAP = 11
PILL_FONT = 14
HEAD_FONT = 11
SECTION_GAP = 24
TOP = 74  # y where the first section heading baseline sits


def text_width(s, size=PILL_FONT):
    """Rough Georgia width estimate: wide enough that text never overflows."""
    w = 0.0
    for ch in s:
        if ch == " ":
            w += 0.30
        elif ch in ".·,'":
            w += 0.30
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
    return w * size


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def layout():
    """Return (elements, total_height)."""
    els = []
    y = TOP
    delay = 0.25
    for icon, name, items in SECTIONS:
        # heading + rule
        label = f"{icon}  {name}"
        els.append(
            f'<text x="{PAD}" y="{y}" class="head" font-family="{LBL_FONT}" '
            f'font-size="{HEAD_FONT}" letter-spacing="3.5" fill="{GOLD}">{esc(label)}</text>'
        )
        rule_x = PAD + text_width(name, HEAD_FONT) * 1.35 + 44
        els.append(
            f'<rect x="{rule_x:.0f}" y="{y - 4}" width="{W - PAD - rule_x:.0f}" height="1" '
            f'fill="url(#rule)"/>'
        )
        # pills
        x = PAD
        py = y + 16
        for i, item in enumerate(items):
            pw = text_width(item) + PILL_PAD_X * 2
            if x + pw > W - PAD:
                x = PAD
                py += PILL_H + ROW_GAP
            begin = 0.4 + (i % 7) * 0.9
            els.append(
                f'<g class="pill" style="animation-delay:{delay:.2f}s">'
                f'<rect x="{x:.1f}" y="{py}" width="{pw:.1f}" height="{PILL_H}" rx="{PILL_R}" '
                f'fill="{PILL_FILL}" stroke="{GOLD}" stroke-opacity="0.6">'
                f'<animate attributeName="stroke" values="{GOLD};{EMBER};{GOLD}" dur="9s" '
                f'begin="{begin:.1f}s" repeatCount="indefinite"/></rect>'
                f'<text x="{x + pw / 2:.1f}" y="{py + 21}" text-anchor="middle" '
                f'font-family="{VAL_FONT}" font-size="{PILL_FONT}" fill="{SAND}">{esc(item)}</text>'
                f'</g>'
            )
            x += pw + PILL_GAP
            delay += 0.045
        y = py + PILL_H + SECTION_GAP + 14
    return els, y + 8


def particles():
    out = []
    seeds = [(96, 10.9, 1.2), (388, 8.3, 7.3), (541, 12.0, 3.4), (702, 9.6, 5.1),
             (833, 11.4, 0.6), (250, 13.2, 8.8), (640, 10.1, 2.2)]
    for cx, dur, begin in seeds:
        out.append(
            f'<circle cx="{cx}" cy="0" r="1.4" fill="{GOLD}" opacity="0">'
            f'<animate attributeName="cy" values="H;-20" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.6;0.25;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{cx};{cx - 40}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    return out


def build():
    els, H = layout()
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Tech stack: languages, frameworks, data and cloud, AI and LLM, tools">',
        '<defs>',
        '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',
        '<stop offset="0" stop-color="#16100a"/><stop offset="1" stop-color="#0A0A0A"/>',
        '</linearGradient>',
        f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0" stop-color="{GOLD}" stop-opacity="0.45"/>',
        f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>',
        '</linearGradient>',
        '<radialGradient id="glow" cx="0.5" cy="1" r="0.9">',
        f'<stop offset="0" stop-color="{EMBER}" stop-opacity="0.22"/>',
        f'<stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>',
        '</radialGradient>',
        '<filter id="ember" x="-30%" y="-30%" width="160%" height="160%">',
        '<feGaussianBlur stdDeviation="8"/></filter>',
        '</defs>',
        '<style>',
        '.in{opacity:0;animation:in .8s ease-out .15s forwards}',
        '@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}',
        '.em{animation:br 6s ease-in-out infinite alternate}',
        '@keyframes br{from{opacity:.14}to{opacity:.38}}',
        '.pill{opacity:0;animation:up .8s cubic-bezier(.16,1,.3,1) forwards}',
        '@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}',
        '.head{animation:pulse 4s ease-in-out infinite}',
        '@keyframes pulse{0%,100%{opacity:.78}50%{opacity:1}}',
        '@media (prefers-reduced-motion:reduce){.in,.pill{animation:none;opacity:1}'
        '.em,.head{animation:none}}',
        '</style>',
        # panel (same construction as the stat cards)
        f'<rect class="em" x="6" y="6" width="{W - 12}" height="{H - 12}" rx="14" fill="{EMBER}" filter="url(#ember)"/>',
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="12" fill="url(#bg)" stroke="{GOLD}" stroke-opacity="0.55"/>',
        f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" rx="12" fill="url(#glow)"/>',
        '<g class="in">',
        # title row, matching the stat cards
        f'<text x="28" y="38" font-family="{LBL_FONT}" font-size="13" letter-spacing="3" fill="{GOLD}">FREMEN SURVIVAL GEAR</text>',
        f'<rect x="28" y="46" width="120" height="1" fill="{GOLD}" opacity="0.35"/>',
        f'<text x="{W - 28}" y="38" text-anchor="end" font-family="{LBL_FONT}" font-size="9" '
        f'letter-spacing="2.5" fill="{GOLD}" opacity="0.6">EVERY TOOL A FREMEN NEEDS TO CROSS THE DESERT</text>',
        f'<rect x="{W - 42}" y="29" width="8" height="8" transform="rotate(45 {W - 38} 33)" fill="{GOLD}" opacity="0"/>',
        *els,
        '</g>',
        *[p.replace('values="H;', f'values="{H};') for p in particles()],
        '</svg>',
    ]
    return "".join(parts), H


if __name__ == "__main__":
    svg, H = build()
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({W}x{H}, {len(svg)} bytes)")
