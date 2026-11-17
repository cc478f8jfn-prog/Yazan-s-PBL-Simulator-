#!/usr/bin/env python3
"""Clean and extend the case bank.

  * strip leftover source markers ("[cite: 5]") and filler closing sentences
  * repair the duplicate-option defect
  * turn the ten placeholder embryology entries into real question stems
  * merge the clinical MCQ files (data/clinical/*.json) into the quiz region
  * regenerate CAT_META from the actual data and register the track lists
"""
import json
import os
import random
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "data", "cases.json")
META = os.path.join(ROOT, "data", "meta.json")

FILLER = re.compile(r"\s*(confirmed by [a-z ]+\.|observed via [a-z ]+\.|confirmed by [a-z ]+ studies\.)", re.I)
CITE = re.compile(r"\s*\[cite:\s*\d+\]")

CLINICAL = [
    ("medicine", "Internal Medicine"),
    ("surgery", "Surgery"),
    ("pediatrics", "Pediatrics"),
    ("obgyn", "Obstetrics & Gynaecology"),
    ("psychiatry", "Psychiatry"),
]


def clean_text(text):
    if not isinstance(text, str):
        return text
    text = CITE.sub("", text)
    text = FILLER.sub("", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    if text and text[-1] not in ".?!":
        text += "."
    return text


def main():
    data = json.load(open(CASES, encoding="utf-8"))
    meta = json.load(open(META, encoding="utf-8"))
    report = {"cite": 0, "filler": 0, "dupfix": 0, "stemified": 0, "clinical": 0}

    for region, cats in data.items():
        for cat, levels in cats.items():
            for lvl, arr in levels.items():
                for case in arr:
                    for key in ("mechanism", "exam", "diagnostic", "explanation", "stem", "block"):
                        if key in case:
                            before = case[key]
                            after = clean_text(before)
                            if after != before:
                                if "[cite" in before:
                                    report["cite"] += 1
                                else:
                                    report["filler"] += 1
                                case[key] = after
                    # duplicate options
                    opts = case.get("options", [])
                    if len(opts) != len(set(opts)):
                        seen, fixed = set(), []
                        for o in opts:
                            if o in seen:
                                for alt in ("Gastrula", "Amniotic cavity", "Chorion", "Yolk sac"):
                                    if alt not in opts and alt not in seen:
                                        o = alt
                                        break
                            seen.add(o)
                            fixed.append(o)
                        case["options"] = fixed
                        report["dupfix"] += 1
                    # placeholder embryology entries become question stems
                    if case.get("mechanism", "").startswith("is an embryonic developmental stage"):
                        detail = case.get("exam", "")
                        detail = detail.replace("characterized by hallmark morphological milestones.", "").strip()
                        detail = detail[:1].upper() + detail[1:] if detail else detail
                        case["stem"] = "Embryology practical: " + detail.rstrip(".") + ". Which stage is shown?"
                        for key in ("mechanism", "exam", "diagnostic"):
                            case.pop(key, None)
                        report["stemified"] += 1

    # clinical MCQs
    quiz = data.setdefault("quiz", {})
    for cat, label in CLINICAL:
        path = os.path.join(ROOT, "data", "clinical", cat + ".json")
        if not os.path.exists(path):
            continue
        payload = json.load(open(path, encoding="utf-8"))
        questions = payload["questions"]
        levels = {}
        for q in questions:
            q = dict(q)
            lvl = str(q.pop("level", q.get("difficulty", 1)))
            opts = q["options"]
            # rotate options so the answer is not always index 0
            shift = random.Random(hash(q["stem"]) & 0xFFFF).randrange(4)
            rot = opts[shift:] + opts[:shift]
            q["options"] = rot
            q["answer"] = (q["answer"] - shift) % 4
            q["difficulty"] = int(q.get("difficulty", lvl))
            q["id"] = "quiz-%s-%s-%d" % (cat, lvl, len(levels.get(lvl, [])) + 1)
            q["stem"] = clean_text(q["stem"])
            q["explanation"] = clean_text(q["explanation"])
            levels.setdefault(lvl, []).append(q)
        quiz[cat] = {k: levels[k] for k in sorted(levels)}
        meta["CATEGORY_TITLES"].setdefault("quiz", {})[cat] = label
        report["clinical"] += len(questions)

    # CAT_META straight from the data
    cat_meta = {}
    for region, cats in data.items():
        for cat, levels in cats.items():
            total = sum(len(v) for v in levels.values())
            unit = "questions" if region == "quiz" else "cases"
            cat_meta["%s/%s" % (region, cat)] = "%d levels &middot; %d %s" % (len(levels), total, unit)
    meta["CAT_META"] = cat_meta

    meta["TRACKS"] = {
        "videos": {
            "basic": {"label": "Basic Sciences", "subjects": [
                "anatomy", "embryology", "histology", "physiology", "biochemistry"]},
            "clinical": {"label": "Clinical", "subjects": [
                "pathology", "pharmacology", "microbiology", "immunology",
                "medicine", "surgery", "pediatrics", "obgyn", "psychiatry"]},
        },
        "quiz": {
            "basic": {"label": "Basic Sciences", "categories": [
                "msk", "neuro", "cardio", "resp", "renal", "git", "endocrine", "repro",
                "blood_immune", "development"]},
            "clinical": {"label": "Clinical", "categories": [
                "medicine", "surgery", "pediatrics", "obgyn", "psychiatry"]},
        },
    }

    json.dump(data, open(CASES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(meta, open(META, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    total = sum(len(v) for cats in data.values() for levels in cats.values() for v in levels.values())
    print(report, "total entries:", total)
    print("quiz categories:", list(quiz.keys()))


if __name__ == "__main__":
    main()
