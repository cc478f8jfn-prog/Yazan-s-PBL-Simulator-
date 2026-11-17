#!/usr/bin/env python3
"""Add the dual-mode simulator UI (mode picker, OSCE station) and the layout fixes."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "tools", "template.html")
OSCE = open(os.path.join(ROOT, "tools", "osce.js"), encoding="utf-8").read()

CSS = """
        /* ---- larger, organised section buttons ---- */
        .cat-grid { grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 16px; }
        .start-box { min-height: 104px; display: flex; flex-direction: column; align-items: center;
            justify-content: center; gap: 6px; padding: 18px 16px; font-size: 1.05rem; border-radius: 12px; }
        .start-box .cat-meta { font-size: .8rem; }
        .start-box .cat-status { font-size: .78rem; }
        .limb-column .start-box { min-height: 84px; }
        .limb-column h2 { font-size: 1.25rem; }

        /* ---- centred case text ---- */
        .clinical-history { text-align: center; max-width: 820px; margin: 0 auto; font-size: 1.08rem; line-height: 1.75; }
        .diagnostic-viewer { text-align: center; max-width: 820px; margin: 12px auto 0; }
        .sim-header { text-align: center; }
        .options-grid { max-width: 980px; margin: 0 auto; }

        /* ---- mode picker ---- */
        .mode-overlay { position: fixed; inset: 0; background: rgba(8, 10, 12, .88); z-index: 2400;
            display: flex; align-items: center; justify-content: center; padding: 20px; }
        .mode-box { background: #1c1f22; border: 1px solid #3498db; border-radius: 16px; padding: 26px;
            width: 100%; max-width: 760px; text-align: center; }
        .mode-box h2 { margin: 0 0 6px; color: #fff; font-size: 1.3rem; }
        .mode-box p { color: #9fb3c8; margin: 0 0 20px; font-size: .95rem; }
        .mode-choices { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
        .mode-card { background: #24282c; border: 2px solid #3a4147; border-radius: 14px; padding: 22px 18px;
            color: #e8eaed; cursor: pointer; text-align: center; display: flex; flex-direction: column;
            gap: 8px; transition: all .2s; font-size: .92rem; line-height: 1.5; }
        .mode-card b { font-size: 1.1rem; color: #fff; }
        .mode-card span { color: #9fb3c8; }
        .mode-card:hover { border-color: #3498db; transform: translateY(-2px); }
        .mode-card-clinical:hover { border-color: #27ae60; }
        .mode-icon { font-size: 1.8rem; }
        .mode-cancel { margin-top: 18px; background: transparent; border: 1px solid #444; color: #9fb3c8;
            border-radius: 8px; padding: 8px 18px; cursor: pointer; }
        @media (max-width: 620px) { .mode-choices { grid-template-columns: 1fr; } }

        /* ---- OSCE station ---- */
        .osce-screen { display: none; width: 100%; max-width: 1080px; margin: 0 auto; padding: 18px 16px 60px; }
        .osce-head { display: flex; align-items: center; gap: 14px; margin-bottom: 14px; }
        .osce-head h2 { color: #3498db; font-size: 1.15rem; margin: 0; }
        .osce-chat { background: #17191b; border: 1px solid #2f3438; border-radius: 12px; padding: 14px;
            height: 300px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
        .osce-msg { max-width: 76%; padding: 10px 13px; border-radius: 12px; font-size: .93rem; line-height: 1.5; }
        .osce-patient { background: #22303a; color: #e8f2f8; align-self: flex-start; }
        .osce-you { background: #1f4560; color: #eaf4ff; align-self: flex-end; }
        .osce-system { background: #1f2a22; color: #d9f0e2; align-self: flex-start; font-family: ui-monospace, monospace; font-size: .86rem; }
        .osce-panel { margin-top: 16px; }
        .osce-stepper { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; }
        .osce-step { background: #24282c; border: 1px solid #3a4147; color: #cfd8dc; border-radius: 10px;
            padding: 12px 10px; cursor: pointer; font-size: .88rem; font-weight: 600; }
        .osce-step.active { background: #3498db; border-color: #3498db; color: #fff; }
        .osce-step.done { border-color: #27ae60; }
        .osce-hintrow { color: #9fb3c8; font-size: .9rem; margin: 14px 0 10px; }
        .osce-inputrow { display: flex; gap: 10px; margin-bottom: 12px; }
        .osce-inputrow input { flex: 1; background: #17191b; border: 1px solid #3a4147; color: #f0f2f5;
            border-radius: 10px; padding: 12px 14px; font-size: .95rem; }
        .osce-send { background: #3498db; border: none; color: #fff; border-radius: 10px; padding: 0 22px;
            font-weight: 700; cursor: pointer; }
        .osce-chips { display: flex; flex-wrap: wrap; gap: 8px; }
        .osce-chip { background: #24282c; border: 1px solid #3a4147; color: #cfd8dc; border-radius: 20px;
            padding: 9px 15px; font-size: .85rem; cursor: pointer; }
        .osce-chip:hover { border-color: #3498db; color: #fff; }
        .osce-chip.picked { background: #1f4560; border-color: #3498db; color: #fff; }
        .osce-chip-flag { border-color: #c0392b; color: #ffb3a7; }
        .osce-select { width: 100%; background: #17191b; border: 1px solid #3a4147; color: #f0f2f5;
            border-radius: 10px; padding: 12px 14px; font-size: .95rem; margin-bottom: 12px; }
        .osce-plan { width: 100%; min-height: 130px; background: #17191b; border: 1px solid #3a4147;
            color: #f0f2f5; border-radius: 10px; padding: 12px 14px; font-size: .95rem; line-height: 1.5;
            box-sizing: border-box; }
        .osce-finish { margin-top: 12px; background: #27ae60; border: none; color: #fff; border-radius: 10px;
            padding: 13px 26px; font-weight: 700; font-size: .98rem; cursor: pointer; }
        .osce-card { background: #1c1f22; border: 1px solid #3498db; border-radius: 14px; padding: 20px; }
        .osce-card h3 { margin: 0 0 16px; color: #fff; font-size: 1.2rem; }
        .osce-card h4 { margin: 20px 0 8px; color: #3498db; font-size: 1rem; }
        .score-row { display: grid; grid-template-columns: 190px 1fr 60px; gap: 12px; align-items: center;
            margin-bottom: 8px; font-size: .88rem; color: #cfd8dc; }
        .score-track { background: #2a2f33; border-radius: 6px; height: 8px; overflow: hidden; }
        .score-fill { background: #3498db; height: 100%; }
        .osce-notes { margin: 0; padding-left: 20px; color: #cfd8dc; font-size: .9rem; line-height: 1.6; }
        .osce-model { color: #9fb3c8; font-size: .9rem; line-height: 1.6; margin: 12px 0 0; }
        .osce-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; }
        .osce-llm { white-space: pre-wrap; background: #17191b; border: 1px solid #2f3438; border-radius: 12px;
            padding: 16px; margin-top: 16px; color: #d7e2ea; font-size: .9rem; line-height: 1.6; }
        .tutor-btn { background: #2d3f52; border: 1px solid #3498db; color: #dceaf7; border-radius: 8px;
            padding: 10px 18px; font-size: .88rem; cursor: pointer; margin-left: 10px; }
"""

MODE_PICKER = """    <!-- MODE PICKER -->
    <div id="mode-picker" class="mode-overlay" style="display:none;">
        <div class="mode-box">
            <h2 id="mode-title">Section</h2>
            <p id="mode-sub"></p>
            <div class="mode-choices">
                <button class="mode-card" onclick="chooseMode('pre')">
                    <span class="mode-icon">&#9889;</span>
                    <b>Pre-clinical PBL</b>
                    <span>Progressive case triggers, mechanism before diagnosis, Socratic prompts when you stall.</span>
                </button>
                <button class="mode-card mode-card-clinical" onclick="chooseMode('clinical')">
                    <span class="mode-icon">&#129658;</span>
                    <b>Clinical OSCE</b>
                    <span>Virtual patient, focused examination, investigations, differential, then a scored station.</span>
                </button>
            </div>
            <button class="mode-cancel" onclick="closeModePicker()">Cancel</button>
        </div>
    </div>

    <!-- OSCE STATION -->
    <div id="osce-screen" class="osce-screen">
        <div class="osce-head">
            <button class="back-btn" onclick="osceLeave()">&#8592; Back</button>
            <h2 id="osce-title"></h2>
        </div>
        <div id="osce-chat" class="osce-chat"></div>
        <div id="osce-panel" class="osce-panel"></div>
    </div>
"""

html = open(TPL, encoding="utf-8").read()

# CSS
html = html.replace("    </style>", CSS + "    </style>", 1)

# mode picker + OSCE screen before the video player overlay
anchor = "    <!-- VIDEO PLAYER MODAL -->"
assert anchor in html
html = html.replace(anchor, MODE_PICKER + "\n" + anchor, 1)

# tutor button in the pre-clinical case screen
old_next = '<button id="next-button" class="next-btn" onclick="nextCase()">Next Case</button>'
assert old_next in html
html = html.replace(old_next, old_next + '\n        <button id="tutor-button" class="tutor-btn" onclick="tutorHint()">Ask the tutor for a hint</button>', 1)

# drop the old openCategory (the dual-mode one lives in osce.js)
start = html.index("function openCategory(region, category) {")
end = html.index("function startLevel(region, category, lvl) {")
html = html[:start] + html[end:]

# splice osce.js before the bootstrap calls at the end of the script
boot = "renderQuizGrid();\nupdateHomeStatuses();"
assert boot in html
html = html.replace(boot, OSCE.strip() + "\n\n" + boot, 1)

open(TPL, "w", encoding="utf-8").write(html)
print("template patched:", len(html), "bytes")
