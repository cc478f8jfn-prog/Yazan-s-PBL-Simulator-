# Build pipeline

`index.html` is generated. Edit the sources, then rebuild.

    source ~/.venvs/pdfenv/bin/activate
    python3 tools/build.py          # writes index.html from tools/template.html + data/*.json

## Files

| file | what it is |
| --- | --- |
| `tools/template.html` | markup, CSS and the engine (JS) with `__CASES__`, `__VIDEOS__`, `__TRACKS__` slots |
| `tools/engine.js` | reference copy of the engine; splice it into the template after editing |
| `data/cases.json` | PBL cases plus the quiz bank, keyed `region -> category -> level -> [items]` |
| `data/videos.json` | video library, keyed `subject -> section -> {name, ar[], en[]}` |
| `data/meta.json` | region and category titles, `CAT_META` counters, `TRACKS` (basic / clinical split) |
| `data/sources/*.{txt}` | doctor catalogues (`videoId|title`) pulled with `yt-dlp --flat-playlist` |
| `data/kept_videos.json` | snapshot of the subjects that were not re-curated |
| `data/clinical/*.json` | clinical MCQ source files |
| `data/clinical_videos.json` | generated clinical video sections |

## Video curation

    python3 tools/clinical_videos.py     # rebuild clinical sections from data/sources
    cp /tmp/videos_old.json data/videos.json   # baseline for kept subjects (only needed for a full rebuild)
    python3 tools/videos_build.py        # rebuild data/videos.json with the channel rules
    python3 tools/build.py

Channel rules live at the top of `tools/videos_build.py`:

* anatomy, histology: Dr Ayman Khanfour + Ninja Nerd
* physiology: Dr Nagi Iskandar + Ninja Nerd
* biochemistry: Dr Hesham Esmat
* pharmacology: Dr Abdelmoteal Foda

Histology keeps Dr Iman Nabil because neither of those two channels teaches
histology and Ninja Nerd has a single lecture on it.

A video entry is `[id, title, channel, "ar"|"en", "exp"|""]`. The engine renders the
Arabic block first and the English block underneath, and `exp` marks the
explanation / revision lecture that is pinned to the top of its block.

## Refreshing a catalogue

    yt-dlp --flat-playlist --print "%(id)s|%(title)s" <channel /videos url> > data/sources/<name>.txt
