#!/usr/bin/env python3
"""Build index.html (the file GitHub Pages serves) from tools/template.html + data/*.json.

Run:  python3 tools/build.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "tools", "template.html")
OUT = os.path.join(ROOT, "index.html")


def load(name):
    with open(os.path.join(ROOT, "data", name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def main():
    html = open(TPL, encoding="utf-8").read()
    meta = load("meta")
    slots = {
        "CASES": dump(load("cases")),
        "VIDEOS": dump(load("videos")),
        "REGION_TITLES": dump(meta["REGION_TITLES"]),
        "CATEGORY_TITLES": dump(meta["CATEGORY_TITLES"]),
        "CAT_META": dump(meta["CAT_META"]),
        "TRACKS": dump(meta.get("TRACKS", {})),
        "EXPLAIN": dump(meta.get("EXPLAIN", {})),
        "FLASH": dump(load("flashcards")),
    }
    for key, value in slots.items():
        token = "__" + key + "__"
        if token in html:
            html = html.replace(token, value)
    left = [t for t in ("__CASES__", "__VIDEOS__", "__META__") if t in html]
    if left:
        sys.exit("unreplaced slots: %s" % left)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("built %s (%.2f MB)" % (OUT, os.path.getsize(OUT) / 1e6))


if __name__ == "__main__":
    main()
