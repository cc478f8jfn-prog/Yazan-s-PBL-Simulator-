#!/usr/bin/env python3
"""Rebuild data/videos.json from the doctor catalogues in data/sources/.

Rules requested by the owner:
  anatomy, histology : Dr Ayman Khanfour + Ninja Nerd only
  physiology         : Dr Nagi Iskandar + Ninja Nerd only
  biochemistry       : Dr Hesham Esmat only
  pharmacology       : Dr Abdelmoteal Foda only
  other subjects     : existing library kept, re-split into Arabic / English
Every section is stored as {name, ar: [...], en: [...]} where a video is
[id, title, channel, "ar"|"en", "exp"|""] and "exp" marks revision or
explanation lectures that sit at the top of the block.
"""
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "sources")


def load_catalogue(name):
    path = os.path.join(SRC, name + ".txt")
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if "|" in line:
                vid, title = line.rstrip("\n").split("|", 1)
                out.append((vid, title))
    return out


def norm(title):
    """Fold the mathematical-bold unicode Khanfour uses into plain ASCII."""
    return unicodedata.normalize("NFKC", title)


def hits(title, words):
    t = norm(title).lower()
    return sum(1 for w in words if re.search(w, t))


def pick(catalogue, words, limit=6, exclude=()):
    scored = []
    for vid, title in catalogue:
        if any(re.search(e, norm(title), re.I) for e in exclude):
            continue
        score = hits(title, words)
        if score:
            scored.append((score, title.count("|"), vid, title))
    scored.sort(key=lambda r: (-r[0], -len(r[3])))
    return [(vid, norm(title)) for _, _, vid, title in scored[:limit]]


def main():
    print("curation helper: import me from other scripts")
    for name in ("khanfour", "ninja", "nagi", "aligamal", "foda", "vip", "sigma", "vsacad"):
        print(name, len(load_catalogue(name)))


if __name__ == "__main__":
    main()
