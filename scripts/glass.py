"""Shared palette and SVG helpers for the README's soft-glass images. Stdlib only.

Every image is written in light and dark variants (and most in desktop and
mobile layouts); README.md picks one with <picture> sources on
prefers-color-scheme and max-width.
"""
import os

ASSETS = "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

# Light follows the brand palette: soft blue #DBEAFE, cyan #CFFAFE, white,
# charcoal #1E293B, electric blue #0284C7, slate #F1F5F9. Small accent text
# uses #0369A1 because #0284C7 on white is only 4.1:1. Every text colour is
# at least 4.5:1 against the strongest blob seen through the glass.
THEMES = {
    "light": {
        "bg0": "#FFFFFF", "bg1": "#F1F5F9",
        "blobs": ("#DBEAFE", "#CFFAFE", "#BFDBFE"), "blob_op": 0.9,
        "glass_op": 0.62, "edge": "#FFFFFF", "edge_op": 1.0, "frame": "#E2E8F0",
        "text": "#1E293B", "body": "#475569", "muted": "#5B6B82",
        "accent": "#0284C7", "accent_text": "#0369A1",
        "chip_bg": "#F1F5F9", "chip_edge": "#DBEAFE", "chip_text": "#1E293B",
        "heat": ("#F1F5F9", "#DBEAFE", "#93C5FD", "#38BDF8", "#0284C7"),
    },
    "dark": {
        "bg0": "#0B1220", "bg1": "#0F1B2E",
        "blobs": ("#1D4ED8", "#0891B2", "#1E40AF"), "blob_op": 0.32,
        "glass_op": 0.06, "edge": "#FFFFFF", "edge_op": 0.16, "frame": "#1E293B",
        "text": "#E2E8F0", "body": "#CBD5E1", "muted": "#A1AFC3",
        "accent": "#38BDF8", "accent_text": "#7DD3FC",
        "chip_bg": "#13253F", "chip_edge": "#1E3A5F", "chip_text": "#E2E8F0",
        "heat": ("#1E293B", "#1E3A5F", "#1D4ED8", "#0EA5E9", "#7DD3FC"),
    },
}

GREEN = "#16A34A"


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
    """Gradient frame with blurred pastel blobs; blobs are (x, y, r, palette index)."""
    return (
        "<defs>"
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>'
        '<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{t["edge_op"] * 0.4:.3f}"/>'
        '<stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{blur}"/></filter>'
        f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>'
        "</defs>"
        f'<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="url(#bg)"/>'
        + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["blobs"][i]}" opacity="{t["blob_op"]}" '
                  f'filter="url(#blur)"/>' for x, y, r, i in blobs)
        + "</g>"
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" stroke="{t["frame"]}"/>'
    )


def glass(x, y, w, h, rx, t):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#FFFFFF" fill-opacity="{t["glass_op"]}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#sheen)"/>'
        f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" '
        f'stroke="{t["edge"]}" stroke-opacity="{t["edge_op"]}"/>'
    )


def chip(x, y, label, size, t, dot=None):
    """Rounded pill; returns (svg, width). dot draws a status dot before the label."""
    pad = 14 + (14 if dot else 0)
    w = text_width(label, size) + pad + 20
    h = round(size * 2.1)
    out = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
           f'fill="{t["chip_bg"]}" stroke="{t["chip_edge"]}"/>')
    if dot:
        out += f'<circle cx="{x + 16:.1f}" cy="{y + h / 2:.1f}" r="3.5" fill="{dot}"/>'
    out += text(x + pad, y + h * 0.68, label, size, t["chip_text"], 500)
    return out, w


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h:.0f}" viewBox="0 0 {w} {h:.0f}" '
            f'role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>{body}</svg>')


def write(name, content):
    os.makedirs(ASSETS, exist_ok=True)
    path = os.path.join(ASSETS, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"wrote {path} ({len(content):,} bytes)")
