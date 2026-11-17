#!/usr/bin/env python3
"""Split the simulator into two separate simulators: Basic PBL and OSCE."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "tools", "template.html")
html = open(TPL, encoding="utf-8").read()

NAV = """<nav class="main-nav">
            <button class="nav-btn" data-view="landing" onclick="showView('landing')">Home</button>
            <button class="nav-btn" data-view="videos" onclick="showView('videos')">Video Tutorials</button>
            <button class="nav-btn" data-view="pbl" onclick="showView('pbl')">Basic PBL</button>
            <button class="nav-btn" data-view="osce" onclick="showView('osce')">OSCE Simulator</button>
            <button class="nav-btn" data-view="quiz" onclick="showView('quiz')">Quizzes</button>
            <button class="nav-btn" data-view="about" onclick="showView('about')">About</button>
            <button class="nav-btn" data-view="contact" onclick="showView('contact')">Contact Me</button>
        </nav>"""
html = re.sub(r'<nav class="main-nav">.*?</nav>', NAV, html, count=1, flags=re.S)

LANDING_BUTTONS = """            <div class="big-buttons">
                <button class="big-btn" onclick="showView('videos')"><span class="big-icon">&#9654;</span><span class="big-label">Video Tutorials</span></button>
                <button class="big-btn big-btn-primary" onclick="showView('pbl')"><span class="big-icon">&#9889;</span><span class="big-label">Basic PBL Simulator</span></button>
                <button class="big-btn big-btn-primary" onclick="showView('osce')"><span class="big-icon">&#129658;</span><span class="big-label">OSCE Simulator</span></button>
                <button class="big-btn" onclick="showView('quiz')"><span class="big-icon">&#10067;</span><span class="big-label">Quiz Bank</span></button>
            </div>"""
start = html.index('            <div class="big-buttons">')
end = html.index('</div>', html.index('Quiz Bank</span></button>')) + 6
html = html[:start] + LANDING_BUTTONS + html[end:]

# basic PBL header wording
html = html.replace("""            <div class="welcome-text">PBL simulator</div>
            <h1 class="main-title">Choose a System</h1>""",
"""            <div class="welcome-text">Basic PBL simulator</div>
            <h1 class="main-title">Choose a System</h1>
            <p class="section-note">Progressive case triggers, mechanism before diagnosis, progress saved level by level, Socratic hints when you stall.</p>""")

# new OSCE home view, inserted before the quiz view
OSCE_HOME = """    <!-- OSCE SIMULATOR VIEW -->
    <div id="view-osce" class="view" style="display:none;">
        <button class="back-section" onclick="goBack()">&#8592; Back</button>
        <div class="top-header-area">
            <div class="welcome-text">OSCE simulator</div>
            <h1 class="main-title">Choose a Station</h1>
        </div>
        <p class="section-note">A virtual patient, focused examination, investigations, a differential and a plan. Every station ends with an examiner scorecard out of 100, pass mark 60.</p>
        <div id="osce-home-grid" class="osce-home-grid"></div>
    </div>

    <!-- QUIZ VIEW -->"""
html = html.replace("    <!-- QUIZ VIEW -->", OSCE_HOME, 1)

# drop the mode picker markup
start = html.index('    <!-- MODE PICKER -->')
end = html.index('    <!-- OSCE STATION -->')
html = html[:start] + html[end:]

# CSS for the OSCE home grid
html = html.replace("        .case-objective {",
"""        .osce-home-grid { width: 100%; max-width: 1250px; }
        .osce-group { margin-bottom: 22px; }
        .osce-group h3 { color: #3498db; font-size: 1.1rem; margin: 0 0 10px; border-bottom: 1px solid #3a3a3a;
            padding-bottom: 6px; }
        .osce-station { background: #2d2d2d; border: 2px solid #27ae60; color: #f0f2f5; border-radius: 12px;
            padding: 18px 16px; min-height: 104px; display: flex; flex-direction: column; align-items: center;
            justify-content: center; gap: 6px; font-size: 1.02rem; font-weight: 700; cursor: pointer;
            transition: all .2s; text-align: center; }
        .osce-station:hover { background: #27ae60; color: #fff; transform: translateY(-2px); }
        .osce-station .station-meta { font-size: .78rem; font-weight: 400; color: #9fb3c8; }
        .osce-station:hover .station-meta { color: #eafff2; }
        .case-objective {""")

# ---------- JS ----------
old_open = html[html.index("function openCategory(region, category) {"):html.index("function startOSCE(region, category, lvl) {")]
new_open = """function openCategory(region, category) {
  lastRegion = region;
  lastCategory = category;
  if (region === 'quiz') {
    quizTrack = (TRACKS.quiz.clinical.categories.indexOf(category) >= 0) ? 'clinical' : 'basic';
  }
  const lvl = nextLevel(region, category);
  if (lvl === null) { showEnd(region, category); return; }
  startLevel(region, category, lvl);
}

// ---------- OSCE simulator ----------
const OSCE_KEY = 'medplat-osce-v1';
const OSCE_GROUPS = [
  ['Musculoskeletal System', [['msk', 'nerves'], ['msk', 'muscles'], ['msk', 'bones'], ['msk', 'general']]],
  ['Development & Embryology', [['embryology', 'level1'], ['embryology', 'level2'], ['embryology', 'level3'], ['embryology', 'level4']]],
  ['General Pathology', [['pathology', 'general']]],
  ['Physiology, by System', [['physiology', 'cell'], ['physiology', 'nerve_muscle'], ['physiology', 'blood'], ['physiology', 'immune'], ['physiology', 'cardio'], ['physiology', 'resp'], ['physiology', 'renal'], ['physiology', 'git'], ['physiology', 'endocrine'], ['physiology', 'repro']]]
];

function osceProgress() {
  try { return JSON.parse(localStorage.getItem(OSCE_KEY) || '{}'); } catch (e) { return {}; }
}
function osceMark(region, category) {
  const p = osceProgress();
  const k = region + '/' + category;
  p[k] = (p[k] || 0) + 1;
  try { localStorage.setItem(OSCE_KEY, JSON.stringify(p)); } catch (e) {}
}
function renderOsceHome() {
  const root = $('osce-home-grid');
  if (!root) return;
  const prog = osceProgress();
  let html = '';
  OSCE_GROUPS.forEach(group => {
    html += '<div class="osce-group"><h3>' + group[0] + '</h3><div class="cat-grid">';
    group[1].forEach(pair => {
      const region = pair[0], category = pair[1];
      if (!casesData[region] || !casesData[region][category]) return;
      const meta = (CAT_META[region + '/' + category] || '');
      const done = prog[region + '/' + category] || 0;
      html += '<button class="osce-station" onclick="openStation(\\'' + region + '\\',\\'' + category + '\\')">' +
        esc(catTitle(region, category)) +
        '<span class="station-meta">' + meta.replace('&middot;', '\\u00B7') + ' \\u00B7 ' + done + ' station' +
        (done === 1 ? '' : 's') + ' done</span></button>';
    });
    html += '</div></div>';
  });
  root.innerHTML = html;
}

function openStation(region, category) {
  lastRegion = region;
  lastCategory = category;
  const lvl = nextLevel(region, category);
  startOSCE(region, category, lvl === null ? totalLevels(region, category) : lvl);
}

"""
html = html.replace(old_open, new_open, 1)

# osceLeave returns to the OSCE simulator, not the PBL home
html = html.replace("""function osceLeave() {
  osce = null;
  $('osce-screen').style.display = 'none';
  goHome();
}""", """function osceLeave() {
  osce = null;
  $('osce-screen').style.display = 'none';
  NAV.length = 0;
  paint('osce');
}""")

# scorecard marks the station and returns to the OSCE list
html = html.replace("""  osce.scored = sc;""", """  osce.scored = sc;
  osceMark(osce.region, osce.category);""")
html = html.replace("""'<button class="btn-secondary" onclick="goHome()">Back to sections</button></div></div>';""",
                    """'<button class="btn-secondary" onclick="osceLeave()">Back to stations</button></div></div>';""")

# paint() also renders the OSCE home
html = html.replace("  if (name === 'videos') renderVideos();",
                    "  if (name === 'videos') renderVideos();\n  if (name === 'osce') renderOsceHome();")
# viewTarget: 'osce' maps to view-osce automatically
# bootstrap
html = html.replace("renderQuizGrid();\nupdateHomeStatuses();",
                    "renderQuizGrid();\nrenderOsceHome();\nupdateHomeStatuses();")

# about page wording
html = html.replace("Every case runs in two modes: Pre-clinical PBL, or a scored Clinical OSCE station with a virtual patient, focused examination, investigations and an examiner scorecard.",
                    "It ships as two simulators: the Basic PBL Simulator for progressive pre-clinical cases, and the OSCE Simulator, where the same cases become scored stations with a virtual patient, focused examination, investigations, a differential and an examiner scorecard.")

open(TPL, "w", encoding="utf-8").write(html)
print("template split:", len(html), "bytes")
