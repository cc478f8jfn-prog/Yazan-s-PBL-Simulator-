#!/usr/bin/env python3
"""Build data/videos.json applying the owner's channel rules.

  anatomy, histology : Dr Ayman Khanfour + Ninja Nerd
  physiology         : Dr Nagi Iskandar + Ninja Nerd
  biochemistry       : Dr Hesham Esmat
  pharmacology       : Dr Abdelmoteal Foda
  embryology / pathology / microbiology / immunology : existing library kept
  clinical subjects  : data/clinical_videos.json when present

Section shape: {"name": ..., "ar": [[id, title, channel, "ar", tag], ...], "en": [...]}
A "exp" tag marks revision / MCQ / explanation lectures and sorts to the top.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from video_rules import EXP, entry, load, norm  # noqa: E402

KHANFOUR = "Dr Ayman Khanfour"
NINJA = "Ninja Nerd"
NAGI = "Dr Nagi Iskandar"
ESMAT = "Dr Hesham Esmat"
FODA = "Dr Abdelmoteal Foda"
IMAN = "Dr Iman Nabil"

SKIP = re.compile(r"clinical medicine|podcast|nursing|pharmacolog|\btrivia\b|"
                  r"general chemistry|organic chemistry|^biochemistry \|", re.I)


def first_match(title, sections):
    for key in sections:
        if re.search(sections[key][1], title, re.I):
            return key
    return None


# ---------------------------------------------------------------- anatomy
ANATOMY = {
    "upper_limb": ("Upper Limb",
        r"upper limb|upper ext|axilla|pectoral|brachial plexus|forearm|\barm\b|\bhand\b|shoulder|elbow|"
        r"cubital|carpal|scapula|clavicle|humerus|\bradius\b|\bulna\b|deltoid|clavipectoral|intermuscular|"
        r"metacarpal|phalan|thenar|wrist|biceps|triceps|rotator cuff|snuff"),
    "lower_limb": ("Lower Limb",
        r"lower limb|lower ext|gluteal|\bthigh\b|popliteal|\bleg\b|\bfoot\b|\bankle\b|lumbo|tibia|fibula|"
        r"femur|patella|hip bone|arches\b|gastrocnemius|soleus|sciatic|femoral triangle|adductor|"
        r"hamstring|quadriceps|tarsal|plantar|knee joint|hip joint|bones of the foot"),
    "thorax": ("Thorax",
        r"thorax|thoracic (cage|wall|inlet|spine)|lung|pleura|mediastinum|\bheart\b|pericard|diaphragm|"
        r"intercostal|\bribs\b|sternum|azygos"),
    "abdomen": ("Abdomen",
        r"abdominal wall|abdomen|peritoneum|stomach|spleen|intestin|liver|biliary|gallbladder|pancrea|"
        r"portal|gastrointestinal|oesophagus|esophagus|celiac|mesenter|duoden|jejun|ileum|colon|appendix"),
    "pelvis": ("Pelvis & Perineum",
        r"pelvi|perineum|perineal|bladder|urethra|rectum|anal canal|prostate|uterus|vagina|ovar|testis|"
        r"scrotum|ischio|pudendal|broad ligament"),
    "head_neck": ("Head & Neck",
        r"\bskull\b|scalp|\bface\b|parotid|salivary|oral cavity|tongue|pharynx|larynx|\bnose\b|nasal|orbit|"
        r"eyeball|cranial nerve|thyroid gland|infratemporal|pterygopalatine|temporal fossa|mastoid|"
        r"carotid|jugular|submandibular|sublingual|platysma|sternomastoid|pterion|mouth|sinus"),
    "neuroanatomy": ("Neuroanatomy",
        r"neuro|cerebr|cortex|brain ?stem|basal ganglia|thalamus|diencephal|ventricle|\bcsf\b|mening|"
        r"spinal cord|reticular|hypothalam|limbic|internal capsule|white matter|ascending tract|"
        r"descending tract|fourth ventricle"),
}

# Ninja Nerd anatomy titles start with "Anatomy ..."; keep only those.
NINJA_ANATOMY = re.compile(r"^anatomy|anatomy of|skull anatomy|anatomage|brachial plexus|"
                           r"cranial nerves|muscles of the|anatomy & function|thoracic anatomy|"
                           r"^circulatory system|^ascending tracts", re.I)


def build_anatomy(ninja):
    kh = [(v, t) for v, t in load("khanfour")
          if not re.match(r"^(what|why|how|when|which)\b", t, re.I)
          and not re.search(r"embryo|pregnan|fetal|development of", t, re.I)]
    out = {k: {"name": v[0], "ar": [], "en": []} for k, v in ANATOMY.items()}
    for vid, title in kh:
        key = first_match(title, ANATOMY)
        if key:
            out[key]["ar"].append(entry(vid, title, KHANFOUR, "ar"))
    for vid, title in ninja:
        if SKIP.search(title) or not NINJA_ANATOMY.search(title):
            continue
        key = first_match(title, ANATOMY)
        if key:
            out[key]["en"].append(entry(vid, title, NINJA, "en"))
    return out


# ------------------------------------------------------------- physiology
PHYSIOLOGY = {
    "cell": ("Cell & Membrane",
        r"cell membrane|cell biology|body fluid|membrane transport|transport across|osmosis|"
        r"resting membrane|action potential|cell physiology|diffusion|homeostasis"),
    "nerve_muscle": ("Nerve & Muscle",
        r"\bnerve\b|\bnerve\b|neuron|neuromuscular|\bmuscle\b|spindle|motor unit|sarcomere|"
        r"contraction|excitation contraction"),
    "blood": ("Blood & Body Fluids",
        r"\bblood\b|haemat|hemat|erythro|anaemi|anemi|coagulat|haemostas|hemostas|platelet|"
        r"blood group|transfus|plasma|leucocyte|leukocyte"),
    "immune": ("Immunity",
        r"immun|antigen|antibod|lymphocyt|complement|hypersensitiv"),
    "cardio": ("Cardiovascular",
        r"\bcvs\b|cardiac|heart|ecg|electrocardio|circulat|arterial blood pressure|vascular|"
        r"coronary|shock|pacemaker|myocardial"),
    "resp": ("Respiratory",
        r"respiration|respiratory|lung|spirometr|hypoxia|cyanosis|oxygen|hypoxaemia|surfactant|"
        r"compliance|ventilation|breathing"),
    "renal": ("Renal & Acid-Base",
        r"renal|kidney|nephron|\bgfr\b|clearance|tubular|acid.?base|diuretic|micturition|urine"),
    "git": ("Gastrointestinal",
        r"\bgit\b|gastro|digest|saliva|gastric|pancrea|bile|biliary|liver|intestin|motility|"
        r"absorption|swallow|deglutition"),
    "endocrine": ("Endocrine",
        r"endocrine|pituitary|thyroid|adrenal|insulin|glucagon|diabet|calcium homeostasis|"
        r"parathyr|hormone|prolactin|growth hormone|metabolism"),
    "repro": ("Reproductive",
        r"female|male \(|male \(|ovar|menstru|spermatogen|testosteron|pregnan|labour|parturition|"
        r"lactation|placenta|fertiliz"),
    "general": ("Full Physiology Course",
        r"\bcns\b|special sense|vision|hearing|taste|smell|biophysics|practical|crash course|"
        r"revision|mcq|autonom|\bans\b|temperature|exercise|altitude|diving|sleep|memory|\beeg\b|"
        r"thalamus|pain|sensory|motor"),
}

# Ninja Nerd physiology is filed under clean playlist prefixes.
NINJA_PHYS = [
    (r"^cell biology", "cell"),
    (r"^hematology", "blood"),
    (r"^immunology", "immune"),
    (r"^circulatory system|^cardiovascular|^rate and rhythm|^ecg", "cardio"),
    (r"^respiratory", "resp"),
    (r"^renal", "renal"),
    (r"^gastrointestinal", "git"),
    (r"^endocrinology|^metabolism", "endocrine"),
    (r"^musculoskeletal system", "nerve_muscle"),
    (r"^special senses", "general"),
    (r"^neurology", "general"),
]
NINJA_NEURO_OVERRIDE = [
    (r"neuron anatomy|neuromuscular junction|action potential|muscle spindle|synapse", "nerve_muscle"),
]


def build_physiology(ninja):
    nagi = [(v, t) for v, t in load("aligamal")
            if re.search(r"nagi|nagy", t, re.I) and re.search(r"physiolog", t, re.I)]
    nagi += [(v, t) for v, t in load("nagi") if not re.search(r"instructions for mcqs", t, re.I)]
    out = {k: {"name": v[0], "ar": [], "en": []} for k, v in PHYSIOLOGY.items()}
    for vid, title in nagi:
        if re.search(r"introduction|introductory", title, re.I):
            key = "cell"
        else:
            key = first_match(title, PHYSIOLOGY)
        if key:
            out[key]["ar"].append(entry(vid, title, NAGI, "ar"))
    for vid, title in ninja:
        if SKIP.search(title):
            continue
        key = None
        for pattern, k in NINJA_NEURO_OVERRIDE:
            if re.search(pattern, title, re.I):
                key = k
                break
        if key is None:
            for pattern, k in NINJA_PHYS:
                if re.search(pattern, title, re.I):
                    key = k
                    break
        if key:
            out[key]["en"].append(entry(vid, title, NINJA, "en"))
    return out


# ------------------------------------------------------------ biochemistry
BIOCHEM_PICKS = {
    "carbs": ("Carbohydrate Metabolism", [
        ("f5FBYRI5y-o", "Bio 102 lecture 1: Carbohydrates from the start"),
        ("s6lR9RW3Tjg", "CHO 2: Glycolysis, part 1"),
        ("JbbuCFm3kWM", "CHO 2: monosaccharide classification, part 2"),
        ("UKICBhVf1jc", "Chapter revision: Carbohydrates, part 3"),
        ("PtRFDPKSurA", "Revision: Glycolysis and the fate of pyruvate"),
        ("vNDzivyW9fY", "Biochemistry crash course, part 1"),
        ("sW4bICiGP6Q", "Biochemistry crash course, part 2"),
    ]),
    "lipids": ("Lipid Metabolism", [
        ("yTu-8yITwlo", "Lipid chapter, lecture 1"),
        ("wR9e2W3QoeA", "Chapter revision: Lipids, part 1"),
        ("TETRJp5Eklg", "Chapter revision: Lipids, part 2"),
    ]),
    "proteins": ("Proteins, Enzymes & Vitamins", [
        ("3alnrV032_8", "Amino acids, lecture 1: introduction and classification"),
        ("6zhXBZXg16E", "Amino acids, lecture 2"),
        ("JJ9mlo90d2s", "Amino acid metabolism: glycine"),
        ("l8En_hzKHdc", "Proteins, lecture 1"),
        ("sJzcT-HC9pc", "Protein chemistry, part 1"),
        ("zy4gHSskzgk", "Revision: Amino acids"),
        ("T56O1p0_ols", "Revision: Proteins, part 1"),
        ("EcSDdEdKhfg", "Revision: Haemoproteins, part 2"),
        ("oKCTTAvRvog", "Revision: Enzymes, part 1"),
        ("wlsW_R_V_Fg", "Revision: Enzymes, part 2"),
    ]),
    "molecular": ("Molecular Biology & Genetics", [
        ("QRdOwfRv-aw", "DNA structure"),
        ("ZLFVSzTseuo", "Transcription explained in 15 minutes"),
    ]),
}


def build_biochem():
    out = {}
    for key, (name, picks) in BIOCHEM_PICKS.items():
        out[key] = {"name": name,
                    "ar": [entry(v, t, ESMAT, "ar") for v, t in picks],
                    "en": []}
    return out


# ----------------------------------------------------------- pharmacology
PHARM = [
    ("general", "General Principles", r"^general principle|^pharmacokinetic|^pharmacodynamic|^lecture 0"),
    ("autonomic", "Autonomic Pharmacology", r"^autonomic|^ans pharmacology|^autacoid|^lecture 0[5-8]"),
    ("cvs", "Cardiovascular Drugs", r"^cardiovascular"),
    ("cns", "CNS Drugs", r"^cns pharmacology"),
    ("antimicrobials", "Antimicrobials", r"^antimicrobial|^antiviral"),
    ("endocrine", "Endocrine Drugs", r"^endocrine pharmacology|^pharmacology of sex hormone"),
    ("git", "Gastrointestinal Drugs", r"^git pharmacology"),
    ("resp_renal", "Respiratory & Renal Drugs",
     r"^respiratory pharmacology|^renal pharmacology"),
    ("oncology_blood", "Oncology, Blood & Immunomodulators",
     r"^cancer chemotherapy|^short topics|^pharmacology of blood|^pharmacology of the blood"),
]
PHARM_EN = re.compile(r"english version", re.I)


def build_pharm():
    cat = [(v, t) for v, t in load("foda")]
    out = {k: {"name": n, "ar": [], "en": []} for k, n, _ in PHARM}
    leftovers = []
    for vid, title in cat:
        key = None
        for k, name, pattern in PHARM:
            if re.search(pattern, title, re.I):
                key = k
                break
        if key is None:
            leftovers.append((vid, title))
            continue
        lang = "en" if PHARM_EN.search(title) else "ar"
        out[key][lang].append(entry(vid, title, FODA, lang))
    return out, leftovers


# ------------------------------------------------------- kept subjects
KEEP = ("pathology", "microbiology", "immunology")


def build_kept(old):
    out = {}
    for subj in KEEP:
        secs = {}
        for key, sec in old[subj].items():
            ar, en = [], []
            for topic, vids in sec["groups"]:
                for v in vids:
                    e = entry(v[0], norm(v[1]), v[2], "ar" if v[3] == "ar" else "en")
                    (ar if e[3] == "ar" else en).append(e)
            secs[key] = {"name": sec["name"], "ar": ar, "en": en}
        out[subj] = secs
    return out


EMBRYO = {
    "early": ("Early Development", r"general embryolog|fertiliz|implant|gastrul|neurul|folding|first week|second week|third week"),
    "organogenesis": ("Organogenesis", r"branchial|pharyngeal|face|palate|heart|vascular|respiratory|urogenital|urinary|limb|gut"),
    "defects": ("Birth Defects & Placenta", r"teratogen|twin|placenta|fetal circulation|anomal"),
    "general": ("Embryology - full course", r"revision|mcq|practical"),
}


def build_embryology(old):
    secs = {}
    for key, sec in old["embryology"].items():
        ar, en = [], []
        for topic, vids in sec["groups"]:
            for v in vids:
                e = entry(v[0], norm(v[1]), v[2], "ar" if v[3] == "ar" else "en")
                (ar if e[3] == "ar" else en).append(e)
        secs[key] = {"name": sec["name"], "ar": ar, "en": en}
    # Khanfour's embryology lectures join the Arabic side
    for vid, title in load("khanfour"):
        if not re.search(r"embryolog|development of|development|fetal|face development", title, re.I):
            continue
        if re.match(r"^(what|why|how)\b", title, re.I):
            continue
        key = first_match(title, EMBRYO) or "general"
        if key in secs:
            secs[key]["ar"].append(entry(vid, title, KHANFOUR, "ar"))
    return secs


def build_histology(old, ninja):
    """Khanfour teaches no histology and Ninja Nerd has a single lecture, so the
    Arabic histology lectures of Dr Iman Nabil stay; English gets Ninja Nerd."""
    secs = {}
    for key, sec in old["histology"].items():
        ar, en = [], []
        for topic, vids in sec["groups"]:
            for v in vids:
                if v[3] == "ar":
                    ar.append(entry(v[0], norm(v[1]), IMAN, "ar"))
                elif "ninja" in v[2].lower():
                    en.append(entry(v[0], norm(v[1]), NINJA, "en"))
        secs[key] = {"name": sec["name"], "ar": ar, "en": en}
    liver = [(vid, t) for vid, t in ninja if re.search(r"liver histology", t, re.I)]
    if liver:
        secs.setdefault("git_liver", {"name": "GI Tract & Liver", "ar": [], "en": []})
        secs["git_liver"]["en"] = [entry(v, t, NINJA, "en") for v, t in liver]
    return secs


def ensure_explanation(sec):
    """Guarantee one 'start here' video per section."""
    block = sec["ar"] + sec["en"]
    if block and not any(v[4] == "exp" for v in block):
        first = sec["ar"][0] if sec["ar"] else sec["en"][0]
        first[4] = "exp"


def sort_block(videos):
    seen, out = set(), []
    for v in sorted(videos, key=lambda x: (0 if x[4] == "exp" else 1,)):
        if v[0] in seen:
            continue
        seen.add(v[0])
        out.append(v)
    return out


def main():
    old = json.load(open(os.path.join(ROOT, "data", "videos.json"), encoding="utf-8"))
    ninja = [(v, t) for v, t in load("ninja")]

    out = {}
    out["anatomy"] = build_anatomy(ninja)
    out["embryology"] = build_embryology(old)
    out["histology"] = build_histology(old, ninja)
    out["physiology"] = build_physiology(ninja)
    out["biochemistry"] = build_biochem()
    pharm, pharm_left = build_pharm()
    out["pharmacology"] = pharm
    for subj, secs in build_kept(old).items():
        out[subj] = secs

    clinical_path = os.path.join(ROOT, "data", "clinical_videos.json")
    if os.path.exists(clinical_path):
        out.update(json.load(open(clinical_path, encoding="utf-8")))

    # one lecture lives in one section: basic subjects win over clinical ones
    order = ["anatomy", "embryology", "histology", "physiology", "biochemistry",
             "pharmacology", "pathology", "microbiology", "immunology",
             "medicine", "surgery", "pediatrics", "obgyn", "psychiatry"]
    seen = set()
    for subj in [s for s in order if s in out] + [s for s in out if s not in order]:
        for key, sec in out[subj].items():
            for lang in ("ar", "en"):
                keep = []
                for v in sec.get(lang, []):
                    if v[0] in seen:
                        continue
                    seen.add(v[0])
                    keep.append(v)
                sec[lang] = keep

    total = 0
    for subj, secs in out.items():
        for key, sec in secs.items():
            sec["ar"] = sort_block(sec.get("ar", []))
            sec["en"] = sort_block(sec.get("en", []))
            ensure_explanation(sec)
            total += len(sec["ar"]) + len(sec["en"])

    with open(os.path.join(ROOT, "data", "videos.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    print("videos:", total)
    for subj, secs in out.items():
        n = sum(len(s["ar"]) + len(s["en"]) for s in secs.values())
        print("\n%s (%d)" % (subj, n))
        for key, sec in secs.items():
            print("   %-18s ar=%-3d en=%-3d exp=%d" % (
                key, len(sec["ar"]), len(sec["en"]),
                sum(1 for v in sec["ar"] + sec["en"] if v[4] == "exp")))
    if pharm_left:
        print("\npharmacology leftovers:", len(pharm_left))
        for v, t in pharm_left:
            print("   ", t[:90])


if __name__ == "__main__":
    main()
