"""Shared palette, fonts and helpers for every generated asset. Stdlib only."""
import os
import random

# Arrakis palette
GOLD = "#D4A574"
GOLD_HI = "#E9BE84"
EMBER = "#E8833A"
ORANGE = "#C2622D"
BROWN = "#3D2312"
SAND = "#E8DCC4"
CREAM = "#F6E7C8"
NIGHT = "#0A0A0A"
PANEL_TOP = "#16100a"
PILL_FILL = "#160D06"

LBL_FONT = "Copperplate, 'Trajan Pro', Georgia, serif"
VAL_FONT = "Georgia, 'Times New Roman', serif"
MONO_FONT = "'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace"

ASSETS = "assets"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def text_width(s, size, spacing=0.0):
    """Rough serif width estimate, wide enough that text never overflows."""
    w = 0.0
    for ch in s:
        if ch == " ":
            w += 0.30
        elif ch in ".·,'-/:":
            w += 0.32
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
    return w * size + spacing * max(len(s) - 1, 0)


def mono_width(s, size):
    return len(s) * size * 0.602


def rng(seed):
    return random.Random(seed)


def reduced_motion(*classes):
    """CSS rule that disables animation for the given classes."""
    return "@media (prefers-reduced-motion:reduce){" + ",".join(classes) + "{animation:none}}"


def panel(w, h, glow_id="ember", grad_id="cardGrad", inset=6):
    """Standard ember-glow card panel used by the stat cards."""
    return (
        f'<rect class="em" x="{inset}" y="{inset}" width="{w - 2 * inset}" height="{h - 2 * inset}" '
        f'rx="14" fill="{ORANGE}" filter="url(#{glow_id})"/>'
        f'<rect x="{inset}" y="{inset}" width="{w - 2 * inset}" height="{h - 2 * inset}" rx="12" '
        f'fill="url(#{grad_id})" stroke="{GOLD}" stroke-opacity="0.55"/>'
    )


CARD_DEFS = (
    '<defs>'
    '<linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{PANEL_TOP}"/><stop offset="1" stop-color="{NIGHT}"/>'
    '</linearGradient>'
    '<filter id="ember" x="-30%" y="-30%" width="160%" height="160%">'
    '<feGaussianBlur stdDeviation="8"/></filter>'
    '</defs>'
)

CARD_STYLE = (
    '<style>'
    '.in{animation:in .8s ease-out .15s both}'
    '@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}'
    '.em{animation:br 6s ease-in-out infinite alternate}'
    '@keyframes br{from{opacity:.14}to{opacity:.38}}'
    '</style>'
)


def title(x, y, text, size=13):
    return (
        f'<text x="{x}" y="{y}" font-family="{LBL_FONT}" font-size="{size}" '
        f'letter-spacing="3" fill="{GOLD}">{esc(text)}</text>'
        f'<rect x="{x}" y="{y + 8}" width="120" height="1" fill="{GOLD}" opacity="0.35"/>'
    )


def diamond(cx, cy, s, fill=GOLD, opacity="1", extra=""):
    return (
        f'<rect x="{cx - s / 2}" y="{cy - s / 2}" width="{s}" height="{s}" '
        f'transform="rotate(45 {cx} {cy})" fill="{fill}" opacity="{opacity}"{extra}/>'
    )


def write_svg(name, svg):
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with open(path, "w") as f:
        f.write(svg)
    print(f"wrote {path} ({len(svg):,} bytes)")
    return path
