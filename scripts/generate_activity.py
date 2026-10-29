#!/usr/bin/env python3
"""Generate the "Spice Production" live-activity ticker (assets/activity.svg)
from the user's latest public GitHub events. A marquee strip that scrolls
right-to-left forever (SMIL translate), refreshed daily by the workflow.

Needs GITHUB_TOKEN (optional locally; raises the rate limit). Stdlib only.
    python3 scripts/generate_activity.py
"""
import datetime as dt
import json
import os
import urllib.request

from common import EMBER, GOLD, GOLD_HI, LBL_FONT, NIGHT, ORANGE, SAND, VAL_FONT, esc, reduced_motion, text_width, write_svg

LOGIN = "vardhan23v"
W, H = 1200, 64
MAX_ITEMS = 8
SPEED = 70  # px per second


def fetch_events():
    req = urllib.request.Request(
        f"https://api.github.com/users/{LOGIN}/events/public?per_page=60",
        headers={"Accept": "application/vnd.github+json", "User-Agent": LOGIN},
    )
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"bearer {tok}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def ago(iso):
    t = dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    s = (dt.datetime.now(dt.timezone.utc) - t).total_seconds()
    for unit, n in (("d", 86400), ("h", 3600), ("m", 60)):
        if s >= n:
            return f"{int(s // n)}{unit} ago"
    return "just now"


def describe(ev):
    """Return (glyph, verb, repo, when) or None for events we don't show."""
    t = ev["type"]
    repo = ev["repo"]["name"].split("/")[-1]
    p = ev.get("payload", {})
    when = ago(ev["created_at"])
    if t == "PushEvent":
        n = len(p.get("commits", [])) or p.get("size", 1)
        return ("◈", f"pushed {n} commit{'s' if n != 1 else ''} to", repo, when)
    if t == "PullRequestEvent":
        return ("⚔", f"{p.get('action', 'opened')} a pull request in", repo, when)
    if t == "CreateEvent":
        kind = p.get("ref_type", "repository")
        return ("☀", f"created {kind} in" if kind != "repository" else "founded sietch", repo, when)
    if t == "WatchEvent":
        return ("★", "starred", repo, when)
    if t == "ForkEvent":
        return ("⑂", "forked", repo, when)
    if t == "IssuesEvent":
        return ("◆", f"{p.get('action', 'opened')} an issue in", repo, when)
    if t == "ReleaseEvent":
        return ("▲", "released", repo, when)
    if t == "PullRequestReviewEvent":
        return ("👁", "reviewed a pull request in", repo, when)
    return None


def items():
    try:
        evs = fetch_events()
    except Exception as e:  # keep the workflow green even if the API blips
        print("activity fetch failed:", e)
        evs = []
    out, seen = [], set()
    for ev in evs:
        d = describe(ev)
        if not d:
            continue
        key = (d[1], d[2])
        if key in seen:
            continue
        seen.add(key)
        out.append(d)
        if len(out) >= MAX_ITEMS:
            break
    if not out:
        out = [("◈", "the harvest continues on", "Arrakis", "always")]
    return out


def build(entries):
    size = 14
    y = H / 2 + 5
    # lay the entries out once, measure, then duplicate for a seamless loop
    frag, x = [], 0.0
    for glyph, verb, repo, when in entries:
        frag.append(f'<text x="{x:.0f}" y="{y}" font-family="{VAL_FONT}" font-size="{size + 2}" fill="{EMBER}">{esc(glyph)}</text>')
        x += 24
        frag.append(f'<text x="{x:.0f}" y="{y}" font-family="{VAL_FONT}" font-size="{size}" fill="{SAND}" opacity="0.85">{esc(verb)}</text>')
        x += text_width(verb, size) + 8
        frag.append(f'<text x="{x:.0f}" y="{y}" font-family="{VAL_FONT}" font-size="{size}" font-weight="bold" fill="{GOLD_HI}">{esc(repo)}</text>')
        x += text_width(repo, size) * 1.08 + 10
        frag.append(f'<text x="{x:.0f}" y="{y}" font-family="{LBL_FONT}" font-size="9" letter-spacing="1.5" fill="{GOLD}" opacity="0.55">{esc(when.upper())}</text>')
        x += text_width(when, 9, 1.5) + 26
        frag.append(f'<rect x="{x:.0f}" y="{y - 8}" width="5" height="5" transform="rotate(45 {x + 2.5:.0f} {y - 5.5})" fill="{GOLD}" opacity="0.5"/>')
        x += 32
    span = max(x, W - 150)
    dur = span / SPEED
    one = "".join(frag)
    return "".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Recent GitHub activity ticker">',
        '<defs>',
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140c06"/><stop offset="1" stop-color="{NIGHT}"/></linearGradient>',
        f'<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#120b06"/><stop offset="1" stop-color="#120b06" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0c0704" stop-opacity="0"/><stop offset="1" stop-color="#0c0704"/></linearGradient>',
        f'<clipPath id="strip"><rect x="150" y="0" width="{W - 150}" height="{H}"/></clipPath>',
        '</defs>',
        '<style>.live{animation:live 1.4s ease-in-out infinite}@keyframes live{0%,100%{opacity:1}50%{opacity:.25}}'
        + reduced_motion('.live') + '</style>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="url(#bg)" stroke="{GOLD}" stroke-opacity="0.35"/>',
        # label block
        f'<rect x="1" y="1" width="150" height="{H - 2}" rx="12" fill="#1a1109"/>',
        f'<rect x="138" y="1" width="12" height="{H - 2}" fill="#1a1109"/>',
        f'<circle class="live" cx="26" cy="{H / 2}" r="4" fill="{EMBER}"/>',
        f'<circle class="live" cx="26" cy="{H / 2}" r="8" fill="{EMBER}" opacity="0.25"/>',
        f'<text x="40" y="{H / 2 - 2}" font-family="{LBL_FONT}" font-size="10" letter-spacing="3" fill="{GOLD}">SPICE</text>',
        f'<text x="40" y="{H / 2 + 12}" font-family="{LBL_FONT}" font-size="10" letter-spacing="3" fill="{GOLD}">PRODUCTION</text>',
        f'<rect x="150" y="12" width="1" height="{H - 24}" fill="{GOLD}" opacity="0.35"/>',
        '<g clip-path="url(#strip)">',
        '<g transform="translate(150,0)">',
        f'<animateTransform attributeName="transform" type="translate" from="150 0" to="{150 - span:.0f} 0" dur="{dur:.1f}s" repeatCount="indefinite"/>',
        one,
        f'<g transform="translate({span:.0f},0)">{one}</g>',
        '</g></g>',
        f'<rect x="150" y="1" width="60" height="{H - 2}" fill="url(#fadeL)"/>',
        f'<rect x="{W - 61}" y="1" width="60" height="{H - 2}" fill="url(#fadeR)"/>',
        '</svg>',
    ])


if __name__ == "__main__":
    write_svg("activity.svg", build(items()))
