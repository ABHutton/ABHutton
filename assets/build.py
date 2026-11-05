#!/usr/bin/env python3
"""Generates the Tokyo Night "terminal" panels used in the profile README.

Edit the content below, then run from the repo root:

    python3 assets/build.py

Each panel is written as assets/<name>-dark.svg (Tokyo Night) and
assets/<name>-light.svg (Tokyo Night Day). Skill icons are downloaded from
skillicons.dev and embedded, since GitHub won't load external images inside an SVG.
"""
import base64
import pathlib
import urllib.request
from html import escape

# --- Content -----------------------------------------------------------------

NAME = "Alexander"
TAGLINE = "Backend developer · South Africa"

# (text, organisation) — rendered as "text at organisation"
ABOUT = [
    ("Intermediate Software Engineer", "AgrigateOne"),
    ("BEng Mechatronics", "SUN"),
    ("BSc majoring in Physics and Engineering Subjects", "UFS"),
]

# skillicons.dev ids: https://github.com/tandpfun/skill-icons#icons-list
STACK = ["ruby", "postgres", "neovim", "obsidian", "markdown", "linux", "docker", "arduino"]

# --- Theme -------------------------------------------------------------------

THEMES = {
    "dark": dict(  # Tokyo Night
        bg="#1a1b26", border="#292e42", fg="#c0caf5", accent="#7aa2f7", comment="#565f89",
        prompt="#9ece6a", bullet="#bb9af7",
        dots=["#f7768e", "#ff9e64", "#e0af68", "#9ece6a", "#7dcfff", "#7aa2f7", "#bb9af7"],
    ),
    "light": dict(  # Tokyo Night Day
        bg="#e1e2e7", border="#c4c8da", fg="#3760bf", accent="#2e7de9", comment="#848cb5",
        prompt="#587539", bullet="#9854f1",
        dots=["#f52a65", "#b15c00", "#8c6c3e", "#587539", "#007197", "#2e7de9", "#9854f1"],
    ),
}

WIDTH = 830
PAD_X = 32
FONT = 'ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace'
OUT = pathlib.Path(__file__).parent


def panel(t, height, body, command=None):
    prompt = ""
    if command:
        prompt = (f'<text x="{PAD_X}" y="38" font-size="14" fill="{t["comment"]}">'
                  f'<tspan fill="{t["prompt"]}">❯</tspan> {escape(command)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <style>text {{ font-family: {FONT}; }}</style>
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>
  {prompt}
  {body}
</svg>
'''


def header(t):
    mid = WIDTH // 2
    dots = "".join(f'<circle cx="{mid - 42 + i * 14}" cy="128" r="4" fill="{c}"/>' for i, c in enumerate(t["dots"]))
    body = f'''<text x="{mid}" y="38" text-anchor="middle" font-size="14" fill="{t["comment"]}"><tspan fill="{t["prompt"]}">❯</tspan> whoami</text>
  <text x="{mid}" y="80" text-anchor="middle" font-size="32" font-weight="bold" fill="{t["fg"]}">Hi, I'm <tspan fill="{t["accent"]}">{escape(NAME)}</tspan></text>
  <text x="{mid}" y="106" text-anchor="middle" font-size="15" fill="{t["comment"]}">{escape(TAGLINE)}</text>
  {dots}'''
    return panel(t, 150, body)


def about(t):
    lines = []
    for i, (text, org) in enumerate(ABOUT):
        y = 72 + i * 28
        lines.append(f'<text x="{PAD_X}" y="{y}" font-size="15" fill="{t["fg"]}">'
                     f'<tspan fill="{t["bullet"]}">-</tspan> {escape(text)} '
                     f'<tspan fill="{t["comment"]}">at</tspan> <tspan fill="{t["accent"]}">{escape(org)}</tspan></text>')
    return panel(t, 72 + (len(ABOUT) - 1) * 28 + 32, "\n  ".join(lines), "cat about.txt")


def fetch_icon(name, theme):
    url = f"https://skillicons.dev/icons?i={name}&theme={theme}"
    # skillicons.dev rejects urllib's default User-Agent
    request = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return base64.b64encode(response.read()).decode()


def stack(t, theme):
    size, gap, top = 48, 16, 58
    items = []
    for i, name in enumerate(STACK):
        x = PAD_X + i * (size + gap)
        items.append(f'<image x="{x}" y="{top}" width="{size}" height="{size}" '
                     f'href="data:image/svg+xml;base64,{fetch_icon(name, theme)}"/>')
        items.append(f'<text x="{x + size / 2}" y="{top + size + 20}" text-anchor="middle" '
                     f'font-size="11" fill="{t["comment"]}">{escape(name)}</text>')
    return panel(t, top + size + 40, "\n  ".join(items), "ls ~/stack")


if __name__ == "__main__":
    for theme, t in THEMES.items():
        for name, svg in (("header", header(t)), ("about", about(t)), ("stack", stack(t, theme))):
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(svg)
            print(f"wrote {path.relative_to(OUT.parent)}")
