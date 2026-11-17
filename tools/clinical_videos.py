#!/usr/bin/env python3
"""Build the clinical half of the video library (data/clinical_videos.json).

Sources are catalogues of established teaching channels. Each subject gets
three sections; every section carries an "explanation" set (approach / review /
cases videos) plus topic lectures, split into Arabic and English blocks.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from video_rules import entry, load, norm  # noqa: E402

CAP = 12
SKIP = re.compile(r"podcast|trailer|shorts|teaser|live stream|q&a|unboxing|nursing|nclex|level up rn|registerednurse|ai in healthcare|practice laws|interview", re.I)

SOURCES = [
    ("ninja", "Ninja Nerd", "en"),
    ("osmosis", "Osmosis", "en"),
    ("ztf", "Zero To Finals", "en"),
    ("mattmike", "Dr Matt & Dr Mike", "en"),
    ("dirty", "Dirty Medicine", "en"),
    ("rhesus", "Rhesus Medicine", "en"),
    ("medicosis", "Medicosis", "en"),
    ("batenia", "Internal Medicine (Arabic)", None),  # language from the title
]

CLINICAL = {
    "medicine": ("Internal Medicine", {
        "cardio": ("Cardiology", [
            r"heart failure", r"myocardial infarct", r"angina", r"\becg\b", r"arrhythm", r"atrial fibrillation",
            r"valvular|valve disease|mitral|aortic stenosis", r"hypertens", r"endocarditis", r"pericarditis",
            r"cardiomyopath", r"shock\b", r"cardiac arrest",
        ]),
        "resp": ("Respiratory", [
            r"asthma", r"copd", r"pneumonia", r"tuberculosis", r"pulmonary embol", r"pleural effusion",
            r"pneumothorax", r"respiratory failure", r"bronchiectasis", r"lung cancer", r"spirometr",
            r"sleep apnoea|sleep apnea",
        ]),
        "endo": ("Endocrinology & Metabolism", [
            r"diabet", r"ketoacidosis|\bdka\b", r"thyroid|hypothyroid|hyperthyroid|graves", r"adrenal|addison|cushing",
            r"pituitary|acromegaly|prolactin", r"hypercalc|hypocalc|parathyr", r"obesity", r"dyslipidaemia|dyslipidemia",
            r"hypoglyc",
        ]),
    }),
    "surgery": ("Surgery", {
        "general": ("General Surgery", [
            r"appendicitis", r"bowel obstruction|intestinal obstruction", r"hernia", r"cholecystitis|gallstone",
            r"pancreatitis", r"peritonitis", r"colorectal|colon cancer", r"breast (cancer|lump)",
            r"acute abdomen", r"piles|haemorrhoid|hemorrhoid|anal fissure|fistula", r"stoma|colectomy",
        ]),
        "trauma": ("Trauma & Emergency", [
            r"trauma", r"\batls\b", r"primary survey", r"fractur", r"\bburns?\b", r"head injury",
            r"(haemorrhagic|hemorrhagic) shock|exsanguinat", r"tension pneumothorax|chest trauma", r"abdominal trauma",
            r"spinal injury|cervical spine",
        ]),
        "urology": ("Urology", [
            r"renal stone|kidney stone|urolithiasis|ureteric colic", r"\bbph\b|benign prostatic",
            r"prostate cancer", r"urinary retention", r"hydrocele|varicocele", r"testicular torsion",
            r"bladder cancer", r"catheter", r"haematuria|hematuria",
        ]),
    }),
    "pediatrics": ("Pediatrics", {
        "neonatal": ("Neonatology", [
            r"neonat", r"newborn", r"neonatal jaundice|physiological jaundice", r"preterm|premature (birth|infant|baby)",
            r"apgar|birth asphyxia", r"neonatal sepsis", r"breastfeed", r"respiratory distress syndrome",
        ]),
        "resp": ("Paediatric Respiratory", [
            r"bronchiolitis", r"croup|laryngotracheobronchitis", r"paediatric asthma|pediatric asthma|childhood asthma",
            r"cystic fibrosis", r"epiglottitis", r"foreign body aspiration",
        ]),
        "growth": ("Growth & Development", [
            r"growth chart|growth (retardation|failure)|short stature", r"developmental milestone|milestones",
            r"immuni[sz]ation schedule|vaccination schedule", r"malnutrition|kwashiorkor|marasmus|wasting",
            r"rickets", r"puberty", r"failure to thrive", r"infant growth",
        ]),
    }),
    "obgyn": ("Obstetrics & Gynaecology", {
        "obstetrics": ("Obstetrics", [
            r"antenatal|prenatal care", r"pre-?eclampsia|eclampsia", r"stages of labou?r|onset of labou?r",
            r"caesarean|cesarean|instrumental delivery", r"placenta (praevia|previa|abruption)",
            r"multiple pregnancy|pregnancy induced hypertension|normal pregnancy",
        ]),
        "gynaecology": ("Gynaecology", [
            r"menorrhagia|abnormal uterine bleeding", r"ovarian (cyst|cancer)", r"fibroid|leiomyoma",
            r"endometriosis", r"\bpcos\b|polycystic ovarian", r"infertil", r"cervical cancer", r"contracept",
            r"menopaus", r"pelvic inflammatory",
        ]),
        "emergencies": ("Obstetric Emergencies", [
            r"postpartum (haemorrhage|hemorrhage)|atonic uterus", r"shoulder dystocia", r"cord prolapse",
            r"uterine rupture", r"ectopic pregnancy", r"miscarriage|spontaneous abortion", r"obstructed labou?r",
            r"puerperal sepsis", r"retained placenta|vasa praevia|amniotic fluid embolism",
        ]),
    }),
    "psychiatry": ("Psychiatry", {
        "psychotic": ("Psychotic Disorders", [
            r"schizophren", r"psychosis|psychotic", r"delusion|hallucinat", r"catatonia",
        ]),
        "mood": ("Mood & Anxiety Disorders", [
            r"depress", r"bipolar", r"anxiety", r"\bocd\b|obsessive", r"panic", r"\bptsd\b|post.?traumatic",
            r"suicid", r"eating disorder|anorexia|bulimia",
        ]),
        "pharm": ("Psychopharmacology", [
            r"antidepress|ssri", r"antipsychotic", r"lithium", r"benzodiazepine", r"psychopharmacolog",
            r"mood stabil",
        ]),
    }),
}

EXCLUDE = re.compile(r"year of the zebra|advancing|keynote|conference|symposium|healthcare providers|"
                     r"burnout|\bAMA -|OMM/COMLEX|interview|grand rounds|webinar|panel discussion|"
                     r"medical school|residency|match day|post.?traumatic stress|\bST (elevation|depression)\b", re.I)

RANK = {"Ninja Nerd": 0, "Zero To Finals": 1, "Dr Matt & Dr Mike": 2, "Osmosis": 3,
        "Rhesus Medicine": 4, "Dirty Medicine": 5, "Internal Medicine (Arabic)": 6,
        "Medicosis": 7}

EXPLAIN = re.compile(r"approach|overview|summary|review|crash|in (a|under) \d+ minutes|made easy|explained|"
                     r"basics|introduction|clinical skills|interpretation|understanding|stages of|"
                     r"pathophysiology|causes, symptoms, diagnosis", re.I)


def build():
    catalogues = []
    for key, label, lang in SOURCES:
        for vid, title in load(key):
            if SKIP.search(title) or EXCLUDE.search(title) or len(title) < 12:
                continue
            catalogues.append((vid, title, label, lang))
    out = {}
    used = set()
    for subj, (subj_name, secs) in CLINICAL.items():
        out[subj] = {}
        for sec_key, (sec_name, patterns) in secs.items():
            ar, en = [], []
            ordered = sorted(catalogues, key=lambda c: (RANK.get(c[2], 9), len(c[1])))
            for vid, title, label, fixed in ordered:
                if vid in used:
                    continue
                if not any(re.search(p, title, re.I) for p in patterns):
                    continue
                lang = fixed or ("ar" if re.search(r"[\u0600-\u06FF]", title) else "en")
                block = ar if lang == "ar" else en
                if len(block) >= CAP:
                    continue
                e = entry(vid, title, label, lang)
                if EXPLAIN.search(title):
                    e[4] = "exp"
                block.append(e)
                used.add(vid)
            out[subj][sec_key] = {"name": sec_name, "ar": ar, "en": en}
    return out


def main():
    data = build()
    with open(os.path.join(ROOT, "data", "clinical_videos.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    total = 0
    for subj, secs in data.items():
        n = sum(len(s["ar"]) + len(s["en"]) for s in secs.values())
        total += n
        print("\n%s (%d)" % (subj, n))
        for k, s in secs.items():
            print("   %-14s ar=%-3d en=%-3d exp=%d" % (
                k, len(s["ar"]), len(s["en"]), sum(1 for v in s["ar"] + s["en"] if v[4] == "exp")))
            for v in s["en"][:3]:
                print("        ", v[1][:78])
    print("\nclinical total:", total)


if __name__ == "__main__":
    main()
