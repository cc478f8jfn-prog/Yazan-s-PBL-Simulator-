#!/usr/bin/env python3
"""Rewrite the templated case openers into case-specific vignettes.

The generated case bank reused five openers ("presented with systemic fluid,
electrolyte, or hematologic imbalance" and friends) and a generic examination
lead ("exhibits structural features of organogenesis disruption."). This script
replaces both with the specific finding that is already stored in the record.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "data", "cases.json")

GENERIC_MECH = re.compile(
    r"^(was evaluated during neonatal screening for congenital anomalies|"
    r"presented with complex embryological malformation or syndrome|"
    r"presented with systemic fluid, electrolyte, or hematologic imbalance|"
    r"presented with neurological or neuromuscular transmission disorder|"
    r"presented with immune-mediated pathology or immunodeficiency|"
    r"presented with acute (upper|lower) extremity pathology following trauma or overuse|"
    r"presented with acute (upper|lower) extremity injury or chronic overload syndrome|"
    r"presented with characteristic clinical signs)\b", re.I)

GENERIC_LEAD = re.compile(
    r"^(exhibits|shows|demonstrates|presents with)\s+"
    r"(structural features of organogenesis disruption|clinical signs of physiological dysfunction|"
    r"characteristic clinical signs|clinical manifestations of immune dysfunction|"
    r"characteristic anatomical malformations|features of advanced pathology|"
    r"signs of neuromuscular dysfunction|characteristic (clinical|anatomical) features)\b[.,;]?\s*",
    re.I)


def tidy(text):
    text = re.sub(r"\s{2,}", " ", text or "").strip()
    return text


def lower_first(text):
    return text[:1].lower() + text[1:] if text else text


def rewrite(case):
    mech = tidy(case.get("mechanism", ""))
    exam = tidy(case.get("exam", ""))
    diag = tidy(case.get("diagnostic", ""))
    if not GENERIC_MECH.match(mech) and not GENERIC_LEAD.match(exam):
        return False

    specific = GENERIC_LEAD.sub("", exam).strip(" .;,")
    if not specific:
        return False
    # the specific part can hold two clauses: keep both, drop the generic one
    clause = specific
    case["mechanism"] = "presents with " + lower_first(clause).rstrip(".")

    prefix, _, body = diag.partition(":")
    if body and prefix.lower().strip() in ("clinical observation", "physical exam", "clinical", "examination"):
        case["exam"] = lower_first(body.strip().rstrip("."))
        case["diagnostic"] = ""
    else:
        case["exam"] = ""
    return True


def main():
    data = json.load(open(CASES, encoding="utf-8"))
    changed = 0
    for region, cats in data.items():
        if region == "quiz":
            continue
        for cat, levels in cats.items():
            for lvl, arr in levels.items():
                for case in arr:
                    if rewrite(case):
                        changed += 1
    json.dump(data, open(CASES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("rewritten cases:", changed)


if __name__ == "__main__":
    main()
