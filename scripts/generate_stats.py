#!/usr/bin/env python3
"""Generate Dune-themed GitHub stats cards (assets/spice-github-stats.svg,
assets/spice-langs.svg) from the GitHub GraphQL API.

Needs GITHUB_TOKEN in the environment. Stdlib only, so it runs directly
in GitHub Actions. Run from the repo root.
"""
import json
import os
import urllib.request

LOGIN = "vardhan23v"
OUT_DIR = "assets"

QUERY = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    repositories(first:100, ownerAffiliations:OWNER, isFork:false){
      totalCount
      nodes{
        stargazerCount
        languages(first:8, orderBy:{field:SIZE,direction:DESC}){
          edges{size node{name color}}
        }
      }
    }
    contributionsCollection{
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar{totalContributions}
    }
  }
}
"""

GOLD = "#D4A574"
EMBER = "#E8833A"
ORANGE = "#C2622D"
BROWN = "#3D2312"
SAND = "#E8DCC4"
LBL_FONT = "Copperplate, 'Trajan Pro', Georgia, serif"
VAL_FONT = "Georgia, 'Times New Roman', serif"


def fetch():
    token = os.environ["GITHUB_TOKEN"]
    body = json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    return data["data"]["user"]


def fmt(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 10_000:
        return f"{n/1000:.0f}K"
    if n >= 1_000:
        return f"{n/1000:.1f}K"
    return str(n)


CARD_HEAD = (
    '<defs>'
    '<linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#16100a"/><stop offset="1" stop-color="#0A0A0A"/>'
    '</linearGradient>'
    '<filter id="ember" x="-30%" y="-30%" width="160%" height="160%">'
    '<feGaussianBlur stdDeviation="8"/></filter>'
    '</defs>'
    '<style>'
    '.in{opacity:0;animation:in .8s ease-out .15s forwards}'
    '@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}'
    '.em{animation:br 6s ease-in-out infinite alternate}'
    '@keyframes br{from{opacity:.14}to{opacity:.38}}'
    '.bar{transform:scaleX(0);transform-origin:24px 0;'
    'animation:gr 1.2s cubic-bezier(.2,.7,.3,1) .5s forwards}'
    '@keyframes gr{to{transform:scaleX(1)}}'
    '</style>'
)


def panel(w, h):
    return (
        f'<rect class="em" x="6" y="6" width="{w-12}" height="{h-12}" rx="14" '
        f'fill="{ORANGE}" filter="url(#ember)"/>'
        f'<rect x="6" y="6" width="{w-12}" height="{h-12}" rx="12" '
        f'fill="url(#cardGrad)" stroke="{GOLD}" stroke-opacity="0.55"/>'
    )


def title(x, y, text):
    return (
        f'<text x="{x}" y="{y}" font-family="{LBL_FONT}" font-size="13" '
        f'letter-spacing="3" fill="{GOLD}">{text}</text>'
        f'<rect x="{x}" y="{y+8}" width="120" height="1" fill="{GOLD}" opacity="0.35"/>'
    )


def diamond(cx, cy, s, fill=GOLD, opacity="1"):
    return (
        f'<rect x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" '
        f'transform="rotate(45 {cx} {cy})" fill="{fill}" opacity="{opacity}"/>'
    )


def stats_card(u):
    W, H = 460, 190
    cc = u["contributionsCollection"]
    contribs = cc["contributionCalendar"]["totalContributions"]
    commits = cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
    stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
    grid = [
        ("COMMITS", fmt(commits)),
        ("SIETCHES", fmt(u["repositories"]["totalCount"])),
        ("FREMEN", fmt(u["followers"]["totalCount"])),
        ("STARS", fmt(stars)),
    ]
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="GitHub stats">',
        CARD_HEAD,
        panel(W, H),
        '<g class="in">',
        title(28, 38, "SPICE HARVEST DATA"),
        diamond(418, 33, 8),
        # hero: contributions this cycle
        f'<text x="28" y="112" font-family="{VAL_FONT}" font-weight="bold" '
        f'font-size="46" fill="{SAND}">{fmt(contribs)}</text>',
        f'<text x="28" y="136" font-family="{LBL_FONT}" font-size="10" '
        f'letter-spacing="2.5" fill="{GOLD}">CONTRIBUTIONS</text>',
        f'<text x="28" y="152" font-family="{LBL_FONT}" font-size="10" '
        f'letter-spacing="2.5" fill="{GOLD}" opacity="0.6">THIS CYCLE</text>',
        f'<rect x="222" y="66" width="1" height="96" fill="{GOLD}" opacity="0.22"/>',
    ]
    for i, (lbl, val) in enumerate(grid):
        x = 252 + (i % 2) * 105
        y = 96 + (i // 2) * 52
        p.append(diamond(x - 10, y - 7, 5, GOLD, "0.65"))
        p.append(
            f'<text x="{x}" y="{y}" font-family="{VAL_FONT}" font-weight="bold" '
            f'font-size="22" fill="{SAND}">{val}</text>'
        )
        p.append(
            f'<text x="{x}" y="{y+17}" font-family="{LBL_FONT}" font-size="9.5" '
            f'letter-spacing="2" fill="{GOLD}" opacity="0.85">{lbl}</text>'
        )
    p.append('</g></svg>')
    return ''.join(p)


def langs_card(u):
    W, H = 460, 190
    agg = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            cur = agg.setdefault(name, [0, e["node"]["color"] or GOLD])
            cur[0] += e["size"]
    total = sum(v[0] for v in agg.values()) or 1
    top = sorted(agg.items(), key=lambda kv: -kv[1][0])[:4]
    rest = total - sum(v[0] for _, v in top)
    rows = [(n, v[0] / total, v[1]) for n, v in top]
    if rest > 0:
        rows.append(("Other", rest / total, BROWN))

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="Most used languages">',
        CARD_HEAD,
        panel(W, H),
        '<g class="in">',
        title(28, 38, "TONGUES OF THE IMPERIUM"),
        diamond(418, 33, 8),
    ]
    # stacked bar
    bx, bw, by, bh = 28, W - 56, 62, 12
    x = float(bx)
    p.append(f'<g class="bar">')
    for i, (name, frac, color) in enumerate(rows):
        w = bw * frac
        p.append(
            f'<rect x="{x:.1f}" y="{by}" width="{max(w - 2, 1.5):.1f}" height="{bh}" '
            f'rx="3" fill="{color}"/>'
        )
        x += w
    p.append('</g>')
    # legend, two columns
    for i, (name, frac, color) in enumerate(rows):
        cx = 28 + (i % 2) * 216
        cy = 106 + (i // 2) * 30
        p.append(f'<circle cx="{cx+5}" cy="{cy-5}" r="5" fill="{color}"/>')
        p.append(
            f'<text x="{cx+20}" y="{cy}" font-family="{VAL_FONT}" '
            f'font-size="14" fill="{SAND}">{name}</text>'
        )
        p.append(
            f'<text x="{cx+196}" y="{cy}" text-anchor="end" font-family="{LBL_FONT}" '
            f'font-size="12" letter-spacing="1" fill="{GOLD}">{frac*100:.1f}%</text>'
        )
    p.append('</g></svg>')
    return ''.join(p)


CAL_QUERY = """
query($login:String!, $from:DateTime!, $to:DateTime!){
  user(login:$login){
    contributionsCollection(from:$from, to:$to){
      contributionCalendar{
        weeks{contributionDays{date contributionCount}}
      }
    }
  }
}
"""


def gql(query, variables):
    token = os.environ["GITHUB_TOKEN"]
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]


def fetch_daily_series():
    """Every (date, count) day from account creation until today."""
    import datetime as dt

    created = dt.date(2024, 9, 16)
    today = dt.date.today()
    days = {}
    start = created
    while start <= today:
        stop = min(start + dt.timedelta(days=364), today)
        d = gql(CAL_QUERY, {
            "login": LOGIN,
            "from": f"{start.isoformat()}T00:00:00Z",
            "to": f"{stop.isoformat()}T23:59:59Z",
        })
        weeks = d["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        for w in weeks:
            for day in w["contributionDays"]:
                date = dt.date.fromisoformat(day["date"])
                if created <= date <= today:
                    days[date] = day["contributionCount"]
        start = stop + dt.timedelta(days=1)
    return sorted(days.items()), created, today


def compute_streaks(series, today):
    import datetime as dt

    total = sum(c for _, c in series)
    counts = dict(series)
    # current streak: run ending today (or yesterday when today is still empty)
    cur = 0
    cur_start = None
    probe = today if counts.get(today, 0) > 0 else today - dt.timedelta(days=1)
    d = probe
    while counts.get(d, 0) > 0:
        cur += 1
        cur_start = d
        d -= dt.timedelta(days=1)
    # longest streak
    best, best_range = 0, (None, None)
    run, run_start = 0, None
    for date, c in series:
        if c > 0:
            if run == 0:
                run_start = date
            run += 1
            if run > best:
                best, best_range = run, (run_start, date)
        else:
            run = 0
    return {
        "total": total,
        "current": cur,
        "current_range": (cur_start, probe if cur else None),
        "longest": best,
        "longest_range": best_range,
    }


def _d(date):
    return date.strftime("%b %-d").upper() if date else ""


def streak_card(st, created, today):
    W, H = 460, 190
    cols = [
        (fmt(st["total"]), "TOTAL", f"{_d(created)} {created.year} · PRESENT"),
        (str(st["current"]), "CURRENT STREAK",
         f"{_d(st['current_range'][0])} · {_d(st['current_range'][1])}" if st["current"] else "THE DESERT WAITS"),
        (str(st["longest"]), "LONGEST STREAK",
         f"{_d(st['longest_range'][0])} · {_d(st['longest_range'][1])}" if st["longest"] else ""),
    ]
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="Contribution streaks">',
        CARD_HEAD,
        '<style>.ring{stroke-dasharray:264;stroke-dashoffset:264;'
        'animation:ring 1.4s cubic-bezier(.2,.7,.3,1) .4s forwards}'
        '@keyframes ring{to{stroke-dashoffset:0}}</style>',
        panel(W, H),
        '<g class="in">',
    ]
    centers = [82, 230, 378]
    for i, (val, lbl, sub) in enumerate(cols):
        cx = centers[i]
        if i == 1:
            # hero ring
            p.append(
                f'<circle cx="{cx}" cy="82" r="42" fill="none" stroke="{BROWN}" stroke-width="3"/>'
                f'<circle class="ring" cx="{cx}" cy="82" r="42" fill="none" stroke="{GOLD}" '
                f'stroke-width="3" stroke-linecap="round" transform="rotate(-90 {cx} 82)"/>'
                f'<text x="{cx}" y="94" text-anchor="middle" font-family="{VAL_FONT}" '
                f'font-weight="bold" font-size="34" fill="{SAND}">{val}</text>'
            )
        else:
            p.append(
                f'<text x="{cx}" y="94" text-anchor="middle" font-family="{VAL_FONT}" '
                f'font-weight="bold" font-size="30" fill="{SAND}">{val}</text>'
            )
        p.append(
            f'<text x="{cx}" y="{147 if i == 1 else 130}" text-anchor="middle" '
            f'font-family="{LBL_FONT}" font-size="10" letter-spacing="2" fill="{GOLD}">{lbl}</text>'
        )
        p.append(
            f'<text x="{cx}" y="{164 if i == 1 else 147}" text-anchor="middle" '
            f'font-family="{LBL_FONT}" font-size="8.5" letter-spacing="1.5" '
            f'fill="{GOLD}" opacity="0.55">{sub}</text>'
        )
    for cx in (156, 304):
        p.append(f'<rect x="{cx}" y="52" width="1" height="86" fill="{GOLD}" opacity="0.22"/>')
    p.append('</g></svg>')
    return ''.join(p)


def main():
    u = fetch()
    series, created, today = fetch_daily_series()
    st = compute_streaks(series, today)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "spice-github-stats.svg"), "w") as f:
        f.write(stats_card(u))
    with open(os.path.join(OUT_DIR, "spice-langs.svg"), "w") as f:
        f.write(langs_card(u))
    with open(os.path.join(OUT_DIR, "spice-streak.svg"), "w") as f:
        f.write(streak_card(st, created, today))
    print("wrote spice-github-stats.svg, spice-langs.svg, spice-streak.svg")
    print("streaks:", st["total"], "total /", st["current"], "current /", st["longest"], "longest")


if __name__ == "__main__":
    main()
