#!/usr/bin/env python3
"""Generate the README's stats images from the GitHub GraphQL API:

    assets/stats-overview[-mobile]-{light,dark}.svg   numbers + main languages
    assets/stats-activity[-mobile]-{light,dark}.svg   contribution heatmap

Only public, non-fork repositories owned by LOGIN are counted, so the numbers
match what any visitor can check. Needs GITHUB_TOKEN; runs daily in
.github/workflows/stats.yml. Run from the repo root:

    GITHUB_TOKEN=... python3 scripts/generate_stats.py
"""
import datetime as dt
import json
import os
import urllib.request

from glass import THEMES, backdrop, esc, glass, svg, text, write

LOGIN = "vardhan23v"
TOP_LANGS = 6
# Markup, styles and notebooks inflate byte counts without saying much about the code written.
SKIP_LANGS = {"HTML", "CSS", "SCSS", "Jupyter Notebook", "Makefile", "Dockerfile", "Shell", "Batchfile"}

QUERY = """
query($login:String!, $after:String){
  user(login:$login){
    followers{totalCount}
    repositories(first:100, after:$after, privacy:PUBLIC, ownerAffiliations:OWNER, isFork:false){
      totalCount
      pageInfo{hasNextPage endCursor}
      nodes{
        stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{name color} } }
      }
    }
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount } }
      }
    }
  }
}
"""


def gql(variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


def fetch():
    user = gql({"login": LOGIN, "after": None})
    repos = user["repositories"]
    nodes = list(repos["nodes"])
    while repos["pageInfo"]["hasNextPage"]:
        repos = gql({"login": LOGIN, "after": repos["pageInfo"]["endCursor"]})["repositories"]
        nodes += repos["nodes"]

    # Count each repo's main language once. Byte totals let one repo with vendored
    # code (a lab project with 14 MB of framework Java) outweigh everything else.
    langs = {}
    for repo in nodes:
        main = next((e["node"] for e in repo["languages"]["edges"] if e["node"]["name"] not in SKIP_LANGS), None)
        if main:
            n, color = langs.get(main["name"], (0, main["color"] or "#94A3B8"))
            langs[main["name"]] = (n + 1, color)
    total = sum(n for n, _ in langs.values())
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:TOP_LANGS]

    days = [d for w in user["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    return {
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in nodes),
        "followers": user["followers"]["totalCount"],
        "contributions": user["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "langs": [(n, s / total, c) for n, (s, c) in top],
        "days": days,
        **streaks(days),
    }


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    # today may not have contributions yet, so the current streak can end yesterday
    i = len(counts) - 1
    if counts and counts[i] == 0:
        i -= 1
    current = 0
    while i >= 0 and counts[i]:
        current += 1
        i -= 1
    return {"current": current, "longest": longest}


def fmt(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def tiles(s):
    return [
        (fmt(s["contributions"]), "Contributions", "last 12 months"),
        (str(s["repos"]), "Public repos", "excluding forks"),
        (str(s["stars"]), "Stars earned", "on those repos"),
        (f'{s["current"]}d', "Current streak", f'longest {s["longest"]}d'),
    ]


def tile(x, y, w, h, value, label, note, t):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["chip_bg"]}" '
            f'fill-opacity="0.75" stroke="{t["chip_edge"]}"/>'
            + text(x + 16, y + 36, value, 24, t["text"], 700, spacing=-0.4)
            + text(x + 16, y + 56, label, 12.5, t["body"], 600)
            + text(x + 16, y + 73, note, 11.5, t["muted"]))


def lang_bar(x, y, w, langs, t):
    out, cx = [f'<clipPath id="bar"><rect x="{x}" y="{y}" width="{w}" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">'], x
    for _, share, color in langs:
        out.append(f'<rect x="{cx:.1f}" y="{y}" width="{w * share + 0.5:.1f}" height="10" fill="{color}"/>')
        cx += w * share
    out.append(f'<rect x="{cx:.1f}" y="{y}" width="{max(x + w - cx, 0):.1f}" height="10" fill="{t["chip_edge"]}"/></g>')
    return "".join(out)


def lang_legend(x, y, col_w, cols, langs, t):
    out = []
    for i, (name, share, color) in enumerate(langs):
        lx, ly = x + (i % cols) * col_w, y + (i // cols) * 24
        out.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{color}"/>'
                   + text(lx + 16, ly, name, 13, t["text"], 500)
                   + text(lx + col_w - 18, ly, f"{share * 100:.1f}%", 12.5, t["muted"], anchor="end"))
    return "".join(out)


def heading(x, y, label, t):
    return text(x, y, label, 12, t["accent_text"], 650, spacing=1.4)


def overview(s, t):
    W, H = 900, 250
    body = [backdrop(t, W, H, 22, 46, [(80, 30, 130, 0), (840, 230, 140, 1)]), glass(0, 0, W, H, 22, t),
            heading(28, 40, "GITHUB AT A GLANCE", t)]
    for i, tl in enumerate(tiles(s)):
        body.append(tile(28 + (i % 2) * 196, 58 + (i // 2) * 92, 184, 82, *tl, t))
    lx = 450
    body += [heading(lx, 40, "TOP LANGUAGES", t), lang_bar(lx, 62, W - lx - 28, s["langs"], t),
             lang_legend(lx, 104, (W - lx - 28) / 2, 2, s["langs"], t),
             text(lx, 228, "Main language of each public repo; markup and notebooks excluded.", 11.5, t["muted"])]
    return svg(W, H, overview_label(s), "".join(body))


def overview_mobile(s, t):
    W = 340
    rows = (len(s["langs"]) + 1) // 2
    H = 58 + 2 * 92 + 26 + 40 + rows * 24 + 46
    body = [backdrop(t, W, H, 20, 34, [(40, 30, 110, 0), (310, H - 30, 120, 1)]), glass(0, 0, W, H, 20, t),
            heading(20, 36, "GITHUB AT A GLANCE", t)]
    for i, tl in enumerate(tiles(s)):
        body.append(tile(20 + (i % 2) * 154, 52 + (i // 2) * 92, 146, 82, *tl, t))
    y = 52 + 2 * 92 + 24
    body += [heading(20, y, "TOP LANGUAGES", t), lang_bar(20, y + 16, W - 40, s["langs"], t),
             lang_legend(20, y + 56, (W - 40) / 2, 2, s["langs"], t),
             text(20, H - 20, "Main language of each public repo.", 11, t["muted"])]
    return svg(W, H, overview_label(s), "".join(body))


def overview_label(s):
    langs = ", ".join(f"{n} {p * 100:.0f}%" for n, p, _ in s["langs"])
    return (f'{s["contributions"]} contributions in the last 12 months, {s["repos"]} public repositories, '
            f'{s["stars"]} stars, current streak {s["current"]} days, longest {s["longest"]} days. '
            f"Main languages across public repos: {langs}.")


def level(c, peak):
    if c == 0:
        return 0
    return min(4, 1 + int(3 * c / max(peak, 1)))


def heatmap(s, t, weeks, W, cell, gap, pad):
    days = s["days"]
    # group into Sunday-first weeks, keep the last `weeks`
    first = dt.date.fromisoformat(days[0]["date"])
    cols = {}
    for d in days:
        day = dt.date.fromisoformat(d["date"])
        col = ((day - first).days + (first.weekday() + 1) % 7) // 7
        cols.setdefault(col, []).append((day, d["contributionCount"]))
    keys = sorted(cols)[-weeks:]
    shown = [c for k in keys for _, c in cols[k]]
    peak = sorted(shown)[int(len(shown) * 0.95)] if shown else 1
    total = sum(shown)
    step = cell + gap
    narrow = W < 600
    summary = f"{total:,} in the last {'12 months' if weeks >= 52 else f'{weeks} weeks'}"
    gx, gy = pad, 86 if narrow else 66
    H = gy + 7 * step + 46
    body = [backdrop(t, W, H, 20, 40, [(60, 20, 110, 0), (W - 60, H, 120, 1)]), glass(0, 0, W, H, 20, t),
            heading(pad, 34, "CONTRIBUTION ACTIVITY", t),
            # on narrow layouts the summary drops under the heading instead of sharing its line
            text(pad, 56, summary, 12.5, t["body"], 500) if narrow else text(W - pad, 34, summary, 12.5, t["body"], 500, "end")]
    last_label_x = -100
    for i, k in enumerate(keys):
        for day, c in cols[k]:
            row = (day.weekday() + 1) % 7
            body.append(f'<rect x="{gx + i * step}" y="{gy + row * step}" width="{cell}" height="{cell}" rx="2.5" '
                        f'fill="{t["heat"][level(c, peak)]}"><title>{day.isoformat()}: {c}</title></rect>')
        # label the first week that starts in a new month, if there is room since the last label
        first_day = cols[k][0][0]
        x = gx + i * step
        if first_day.day <= 7 and x - last_label_x >= 34 and i < len(keys) - 2:
            body.append(text(x, gy - 10, first_day.strftime("%b"), 11, t["muted"]))
            last_label_x = x
    ly = gy + 7 * step + 22
    lx = W - pad - 5 * (cell + 4) - 34
    body.append(text(lx - 8, ly + cell - 2, "Less", 11, t["muted"], anchor="end"))
    for i, color in enumerate(t["heat"]):
        body.append(f'<rect x="{lx + i * (cell + 4)}" y="{ly}" width="{cell}" height="{cell}" rx="2.5" fill="{color}"/>')
    body.append(text(lx + 5 * (cell + 4) + 4, ly + cell - 2, "More", 11, t["muted"]))
    label = f"Contribution heatmap: {total} contributions over the last {weeks} weeks."
    return svg(W, H, label, "".join(body))


def main():
    s = fetch()
    for mode, t in THEMES.items():
        write(f"stats-overview-{mode}.svg", overview(s, t))
        write(f"stats-overview-mobile-{mode}.svg", overview_mobile(s, t))
        write(f"stats-activity-{mode}.svg", heatmap(s, t, 53, 900, 12, 3, 28))
        write(f"stats-activity-mobile-{mode}.svg", heatmap(s, t, 18, 340, 13, 3, 20))
    print({k: v for k, v in s.items() if k != "days"})


if __name__ == "__main__":
    main()
