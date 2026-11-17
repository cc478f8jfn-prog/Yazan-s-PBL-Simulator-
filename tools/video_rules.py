#!/usr/bin/env python3
"""Build data/videos.json from the doctor catalogues.

Output model (per section):
    {"name": "Upper Limb", "ar": [[id, title, channel, "ar", tag], ...], "en": [...]}
tag is "exp" for revision / MCQ / summary lectures, otherwise "".
Sections are rendered Arabic block first, English block second.
"""
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

EXP = re.compile(r"revision|rev\.|review|mcq|crash|summary|recap|سؤال|مراجعة|ملخص|امتحان|quiz|"
                 r"introduction|basics|overview|approach|explained|understanding|practical|"
                 r"questions|clinical medicine|cases", re.I)


def norm(t):
    return unicodedata.normalize("NFKC", t).replace("|", "-").strip()


def load(name):
    path = os.path.join(ROOT, "data", "sources", name + ".txt")
    out = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if "|" in line:
                vid, title = line.rstrip("\n").split("|", 1)
                out.append((vid, norm(title)))
    return out


def is_arabic(text):
    return bool(re.search(r"[\u0600-\u06FF]", text))


def match(title, pattern):
    return bool(re.search(pattern, title, re.I))


def entry(vid, title, channel, lang):
    return [vid, title, channel, lang, "exp" if EXP.search(title) else ""]


def assign(catalogue, channel_label, lang, sections, skip=()):
    """sections: list of (key, name, regex) or (key, regex). First match wins."""
    sections = [(s[0], s[1] if len(s) == 3 else s[0], s[-1]) for s in sections]
    buckets = {k: [] for k, _, _ in sections}
    leftovers = []
    used = set()
    for key, name, pattern in sections:
        for vid, title in catalogue:
            if vid in used:
                continue
            if any(re.search(s, title, re.I) for s in skip):
                continue
            if match(title, pattern):
                buckets[key].append(entry(vid, title, channel_label, lang))
                used.add(vid)
    for vid, title in catalogue:
        if vid not in used and not any(re.search(s, title, re.I) for s in skip):
            leftovers.append((vid, title))
    return buckets, leftovers
