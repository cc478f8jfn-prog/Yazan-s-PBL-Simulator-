#!/usr/bin/env python3
"""Rewrite tools/template.html: new CSS, track tabs, new engine.

Run once; build.py then injects the data files.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "tools", "template.html")
ENGINE = open(os.path.join(ROOT, "tools", "engine.js"), encoding="utf-8").read()

CSS = """
        /* ---- tracks, bigger video buttons, language blocks ---- */
        .track-tabs { display:flex; gap:12px; justify-content:center; margin:20px 0 12px; flex-wrap:wrap; }
        .track-tab { background:#252525; border:2px solid #3f3f3f; color:#cfd8dc; border-radius:12px;
            padding:14px 34px; font-size:1.05rem; font-weight:700; letter-spacing:.4px; cursor:pointer;
            transition:all .2s; }
        .track-tab:hover { border-color:#3498db; color:#fff; }
        .track-tab.active { background:#3498db; border-color:#3498db; color:#fff; }
        .videos-menu { display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:16px;
            width:100%; max-width:1080px; margin:18px auto 0; }
        .vid-sub-btn { display:block; width:100%; background:#2d2d2d; border:2px solid #3498db; color:#fff;
            border-radius:12px; padding:22px 20px; font-size:1.1rem; font-weight:700; cursor:pointer;
            text-align:center; transition:all .2s; }
        .vid-sub-btn:hover { background:#3498db; transform:translateY(-2px); }
        .vid-sub-btn .vid-count { display:block; font-size:.8rem; font-weight:400; color:#9fb3c8; margin-top:6px; }
        .vid-sub-btn:hover .vid-count { color:#eaf4ff; }
        .lang-block { width:100%; max-width:1120px; margin:28px auto 0; }
        .lang-title { display:flex; align-items:center; gap:10px; color:#fff; font-size:1.15rem;
            font-weight:700; border-bottom:2px solid #3498db; padding-bottom:8px; }
        .lang-title .lang-tag { font-size:.72rem; letter-spacing:1px; padding:3px 10px; border-radius:20px; }
        .lang-ar .lang-tag { background:#1f5c3f; color:#d6f5e4; }
        .lang-en .lang-tag { background:#1f4560; color:#d6e9f7; }
        .chip-exp { background:#7a4a1f; color:#ffe6cc; }
        .vid-empty { color:#8c9ba5; font-size:.9rem; margin:12px 0 0; }
"""

QUIZ_VIEW = """    <!-- QUIZ VIEW -->
    <div id="view-quiz" class="view" style="display:none;">
        <button class="back-section" onclick="goBack()">&#8592; Back</button>
        <h2 class="section-title">Quiz Bank</h2>
        <p class="section-note">MCQs by system, split into levels that unlock as you finish. The clinical half covers the subjects you meet on the wards.</p>
        <div class="track-tabs">
            <button class="track-tab active" data-track="basic" onclick="setQuizTrack('basic', this)">Basic Sciences</button>
            <button class="track-tab" data-track="clinical" onclick="setQuizTrack('clinical', this)">Clinical</button>
        </div>
        <div id="quiz-grid" class="cat-grid"></div>
    </div>
"""

VIDEOS_VIEW = """    <!-- VIDEO TUTORIALS VIEW -->
    <div id="view-videos" class="view" style="display:none;">
        <button class="back-section" onclick="goBack()">&#8592; Back</button>
        <h2 class="section-title">Video Tutorials</h2>
        <div class="track-tabs">
            <button class="track-tab active" data-track="basic" onclick="setVideoTrack('basic', this)">Basic Sciences</button>
            <button class="track-tab" data-track="clinical" onclick="setVideoTrack('clinical', this)">Clinical</button>
        </div>
        <div id="videos-root"></div>
    </div>
"""

NAV = """<nav class="main-nav">
            <button class="nav-btn" data-view="landing" onclick="showView('landing')">Home</button>
            <button class="nav-btn" data-view="videos" onclick="showView('videos')">Video Tutorials</button>
            <button class="nav-btn" data-view="pbl" onclick="showView('pbl')">PBL Simulator</button>
            <button class="nav-btn" data-view="quiz" onclick="showView('quiz')">Quizzes</button>
            <button class="nav-btn" data-view="about" onclick="showView('about')">About</button>
            <button class="nav-btn" data-view="contact" onclick="showView('contact')">Contact Me</button>
        </nav>"""


def cut(text, start_marker, end_marker):
    i = text.index(start_marker)
    j = text.index(end_marker, i)
    return i, j


html = open(TPL, encoding="utf-8").read()

# 1. CSS
html = html.replace("    </style>", CSS + "    </style>", 1)

# 2. quiz view
i, j = cut(html, "    <!-- QUIZ VIEW -->", "    <!-- VIDEO TUTORIALS VIEW -->")
html = html[:i] + QUIZ_VIEW + "\n" + html[j:]

# 3. videos view
i, j = cut(html, "    <!-- VIDEO TUTORIALS VIEW -->", "    <!-- ABOUT VIEW -->")
html = html[:i] + VIDEOS_VIEW + "\n" + html[j:]

# 4. nav
html = re.sub(r'<nav class="main-nav">.*?</nav>', NAV, html, count=1, flags=re.S)

# 5. engine
start = html.index("const genders = ")
end = html.index("\nupdateHomeStatuses();", start) + len("\nupdateHomeStatuses();")
head = """const genders = [{ id: 'male', pro: 'He', pos: 'his' }, { id: 'female', pro: 'She', pos: 'her' }];
const occupations = ['software engineer', 'medical student', 'construction worker', 'teacher', 'professional athlete',
  'barista', 'mechanic', 'carpenter', 'nurse', 'delivery driver'];
const sides = ['right', 'left'];
const TRACKS = __TRACKS__;

let SAVE = loadSave();
let current = null;
let lastRegion = null;
let lastCategory = null;

"""
html = html[:start] + head + ENGINE.strip() + html[end:]

open(TPL, "w", encoding="utf-8").write(html)
print("template patched, %d bytes" % len(html))
print("slots:", [s for s in ("__CASES__", "__VIDEOS__", "__TRACKS__", "__CAT_META__") if s in html])
