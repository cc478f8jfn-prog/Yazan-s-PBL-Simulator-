#!/usr/bin/env python3
"""Rebrand to YazMed, add light/dark theming, bilingual UI, flashcards and settings."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "tools", "template.html")
THEME = open(os.path.join(ROOT, "tools", "theme.css"), encoding="utf-8").read()
APP = open(os.path.join(ROOT, "tools", "app.js"), encoding="utf-8").read()

html = open(TPL, encoding="utf-8").read()

# ---------------------------------------------------------------- head
head_start = html.index("<head>")
head_end = html.index("</head>")
new_head = """<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YazMed | Medical Learning Platform</title>
    <meta name="description" content="YazMed is a medical learning platform: PBL cases, an OSCE simulator, terminology flashcards, a quiz bank and curated video lectures.">
    <meta name="theme-color" content="#0C161E">
    <link rel="icon" type="image/png" sizes="32x32" href="./favicon-32.png">
    <link rel="icon" type="image/png" sizes="512x512" href="./icon.png">
    <link rel="apple-touch-icon" href="./apple-touch-icon.png">
    <meta property="og:title" content="YazMed | Medical Learning Platform">
    <meta property="og:description" content="PBL cases, an OSCE simulator, terminology flashcards, a quiz bank and curated video lectures.">
    <meta property="og:image" content="./logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Noto+Naskh+Arabic:wght@400;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
    <script>
      (function () {
        try {
          var t = localStorage.getItem('medplat-theme');
          if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
          var s = localStorage.getItem('medplat-size');
          if (s === 's' || s === 'l') document.documentElement.setAttribute('data-size', s);
          var l = localStorage.getItem('medplat-lang');
          document.documentElement.lang = l === 'ar' ? 'ar' : 'en';
          document.documentElement.dir = l === 'ar' ? 'rtl' : 'ltr';
        } catch (e) {}
      })();
    </script>
""" + THEME
html = html[:head_start] + new_head + "    \n" + html[head_end:]

# ---------------------------------------------------------------- header
nav = """        <nav class="main-nav">
            <button class="nav-btn" data-view="landing" data-i18n="nav.home" onclick="showView('landing')">Home</button>
            <button class="nav-btn" data-view="videos" data-i18n="nav.videos" onclick="showView('videos')">Video Tutorials</button>
            <button class="nav-btn" data-view="pbl" data-i18n="nav.pbl" onclick="showView('pbl')">Basic PBL</button>
            <button class="nav-btn" data-view="osce" data-i18n="nav.osce" onclick="showView('osce')">OSCE Simulator</button>
            <button class="nav-btn" data-view="flash" data-i18n="nav.flash" onclick="showView('flash')">Terminology</button>
            <button class="nav-btn" data-view="quiz" data-i18n="nav.quiz" onclick="showView('quiz')">Quizzes</button>
            <button class="nav-btn" data-view="about" data-i18n="nav.about" onclick="showView('about')">About</button>
            <button class="nav-btn" data-view="contact" data-i18n="nav.contact" onclick="showView('contact')">Contact Me</button>
            <button class="nav-btn icon-only" data-view="settings" data-i18n="nav.settings" onclick="showView('settings')">Settings</button>
        </nav>"""
html = re.sub(r'<nav class="main-nav">.*?</nav>', nav, html, count=1, flags=re.S)
html = re.sub(r'<div class="logo"[^>]*>.*?</div>',
              '<button class="logo" onclick="showView(\'landing\')" aria-label="YazMed home">'
              '<img src="./logo-full.png" alt="YazMed" class="logo-img"></button>',
              html, count=1, flags=re.S)

# ---------------------------------------------------------------- landing hero
start = html.index('    <!-- LANDING VIEW -->')
end = html.index('    <!-- PBL SIMULATOR VIEW (by system) -->')
landing = """    <!-- LANDING VIEW -->
    <div id="view-landing" class="view" style="display:flex;">
        <div class="hero">
            <div>
                <div class="welcome-text" data-i18n="landing.welcome">welcome to</div>
                <h1 class="main-title">YazMed</h1>
                <p class="welcome-sub" data-i18n="landing.sub">Clinical PBL cases, an OSCE simulator, terminology flashcards, a quiz bank and video tutorials for the medical years, organised by system in one place.</p>
                <div class="big-buttons">
                    <button class="big-btn" onclick="showView('pbl')"><span class="big-label" data-i18n="landing.pbl">Basic PBL Simulator</span></button>
                    <button class="big-btn big-btn-primary" onclick="showView('osce')"><span class="big-label" data-i18n="landing.osce">OSCE Simulator</span></button>
                    <button class="big-btn" onclick="showView('flash')"><span class="big-label" data-i18n="landing.flash">Terminology Flashcards</span></button>
                    <button class="big-btn" onclick="showView('quiz')"><span class="big-label" data-i18n="landing.quiz">Quiz Bank</span></button>
                    <button class="big-btn" onclick="showView('videos')"><span class="big-label" data-i18n="landing.videos">Video Tutorials</span></button>
                </div>
            </div>
            <div class="hero-art">
                <img class="hero-emblem" src="./icon.png" alt="YazMed emblem">
                <svg class="hero-ecg" viewBox="0 0 600 46" preserveAspectRatio="none" aria-hidden="true">
                    <path d="M0 32 H120 l14 -18 l10 30 l12 -26 l10 14 H230 l16 -8 l12 8 H340 l14 -22 l12 34 l12 -30 l10 18 H600"></path>
                </svg>
            </div>
        </div>
    </div>

"""
html = html[:start] + landing + html[end:]

# ---------------------------------------------------------------- section headings + landing buttons i18n
html = html.replace('<div class="welcome-text">Basic PBL simulator</div>',
                    '<div class="welcome-text" data-i18n="pbl.welcome">Basic PBL simulator</div>')
html = html.replace('<h1 class="main-title">Choose a System</h1>',
                    '<h1 class="main-title" data-i18n="pbl.title">Choose a System</h1>')
html = html.replace('<p class="section-note">Progressive case triggers, mechanism before diagnosis, progress saved level by level, Socratic hints when you stall.</p>',
                    '<p class="section-note" data-i18n="pbl.note">Progressive case triggers, mechanism before diagnosis, progress saved level by level, Socratic hints when you stall.</p>')
html = html.replace('<div class="welcome-text">OSCE simulator</div>',
                    '<div class="welcome-text" data-i18n="osce.welcome">OSCE simulator</div>')
html = html.replace('<h1 class="main-title">Choose a Station</h1>',
                    '<h1 class="main-title" data-i18n="osce.title">Choose a Station</h1>')
html = html.replace('<p class="section-note">A virtual patient, focused examination, investigations, a differential and a plan. Every station ends with an examiner scorecard out of 100, pass mark 60.</p>',
                    '<p class="section-note" data-i18n="osce.note">A virtual patient, focused examination, investigations, a differential and a plan. Every station ends with an examiner scorecard out of 100, pass mark 60.</p>')
html = html.replace('<h2 class="section-title">Quiz Bank</h2>', '<h2 class="section-title" data-i18n="quiz.title">Quiz Bank</h2>')
html = html.replace('<p class="section-note">MCQs by system, split into levels that unlock as you finish. The clinical half covers the subjects you meet on the wards.</p>',
                    '<p class="section-note" data-i18n="quiz.note">MCQs by system, split into levels that unlock as you finish. The clinical half covers the subjects you meet on the wards.</p>')
html = html.replace('<button class="track-tab active" data-track="basic" onclick="setQuizTrack(\'basic\', this)">Basic Sciences</button>',
                    '<button class="track-tab active" data-track="basic" data-i18n="quiz.basic" onclick="setQuizTrack(\'basic\', this)">Basic Sciences</button>')
html = html.replace('<button class="track-tab" data-track="clinical" onclick="setQuizTrack(\'clinical\', this)">Clinical</button>',
                    '<button class="track-tab" data-track="clinical" data-i18n="quiz.clinical" onclick="setQuizTrack(\'clinical\', this)">Clinical</button>')
html = html.replace('<h2 class="section-title">Video Tutorials</h2>', '<h2 class="section-title" data-i18n="video.title">Video Tutorials</h2>')
html = html.replace('<button class="track-tab active" data-track="basic" onclick="setVideoTrack(\'basic\', this)">Basic Sciences</button>',
                    '<button class="track-tab active" data-track="basic" data-i18n="video.basic" onclick="setVideoTrack(\'basic\', this)">Basic Sciences</button>')
html = html.replace('<button class="track-tab" data-track="clinical" onclick="setVideoTrack(\'clinical\', this)">Clinical</button>',
                    '<button class="track-tab" data-track="clinical" data-i18n="video.clinical" onclick="setVideoTrack(\'clinical\', this)">Clinical</button>')

# ---------------------------------------------------------------- flashcards + settings views
extra_views = """    <!-- FLASHCARDS VIEW -->
    <div id="view-flash" class="view" style="display:none;">
        <button class="back-section" onclick="goBack()">&#8592; <span data-i18n="nav.home">Home</span></button>
        <h2 class="section-title" data-i18n="flash.title">Terminology Flashcards</h2>
        <p class="section-note" data-i18n="flash.note">Medical language in two tracks: basic word building and clinical usage.</p>
        <div class="track-tabs">
            <button class="track-tab active" data-track="basic" data-i18n="flash.basic" onclick="setFlashTrack('basic', this)">Basic terminology</button>
            <button class="track-tab" data-track="clinical" data-i18n="flash.clinical" onclick="setFlashTrack('clinical', this)">Clinical terminology</button>
        </div>
        <div id="flash-root"></div>
    </div>

    <!-- SETTINGS VIEW -->
    <div id="view-settings" class="view" style="display:none;">
        <button class="back-section" onclick="goBack()">&#8592; <span data-i18n="nav.home">Home</span></button>
        <h2 class="section-title" data-i18n="settings.title">Settings</h2>
        <p class="section-note" data-i18n="settings.note">Language, appearance and study tools. Everything is stored in this browser only.</p>
        <div class="settings-box" id="settings-body"></div>
    </div>

    <!-- QUIZ VIEW -->"""
html = html.replace("    <!-- QUIZ VIEW -->", extra_views, 1)

# ---------------------------------------------------------------- footer before the modals
footer = """    <footer class="site-footer">
        <div class="footer-brand">
            <img src="./logo-full.png" alt="YazMed">
            <span class="footer-tag"><span data-i18n="footer.tagline">Medical learning platform</span> · <span data-i18n="footer.rights">Built by a medical student, for medical students.</span></span>
        </div>
        <svg class="footer-ecg" viewBox="0 0 200 26" aria-hidden="true">
            <path d="M0 18 h40 l6 -9 l5 16 l6 -13 l5 8 h30 l8 -4 l6 4 h44 l6 -11 l6 17 l6 -14 l5 8 h27"></path>
        </svg>
        <div class="footer-links">
            <button data-i18n="nav.about" onclick="showView('about')">About</button>
            <button data-i18n="nav.contact" onclick="showView('contact')">Contact Me</button>
            <button data-i18n="nav.settings" onclick="showView('settings')">Settings</button>
        </div>
    </footer>

"""
html = html.replace("    <!-- VIDEO PLAYER MODAL -->", footer + "    <!-- VIDEO PLAYER MODAL -->", 1)

# wrap the views in <main>
html = html.replace("    <!-- LANDING VIEW -->", "    <main>\n    <!-- LANDING VIEW -->", 1)
html = html.replace("    <footer class=\"site-footer\">", "    </main>\n\n    <footer class=\"site-footer\">", 1)

# ---------------------------------------------------------------- data + engine
html = html.replace("const TRACKS = __TRACKS__;", "const TRACKS = __TRACKS__;\nconst FLASH = __FLASH__;")

# paint(): handle the new views
html = html.replace("  if (name === 'osce') renderOsceHome();",
                    "  if (name === 'osce') renderOsceHome();\n  if (name === 'flash') renderFlash();\n  if (name === 'settings') renderSettings();")

# region / category titles in Arabic when the UI is Arabic
html = html.replace("""function catTitle(region, category) {
  const byRegion = CATEGORY_TITLES[region];
  if (byRegion && byRegion[category]) return byRegion[category];
  return category;
}""",
"""function catTitle(region, category) {
  if (LANG === 'ar' && AR_CATS[region + '/' + category]) return AR_CATS[region + '/' + category];
  const byRegion = CATEGORY_TITLES[region];
  if (byRegion && byRegion[category]) return byRegion[category];
  return category;
}
function regionTitle(region) {
  if (LANG === 'ar' && AR_REGIONS[region]) return AR_REGIONS[region];
  return REGION_TITLES[region] || '';
}""")
html = html.replace("(REGION_TITLES[current.region] || '')", "regionTitle(current.region)")
html = html.replace("(REGION_TITLES[region] || '')", "regionTitle(region)")

# case screen strings
html = html.replace("""    ? 'Quiz: ' + catTitle(current.region, current.category)""",
                    """    ? t('quiz.title') + ': ' + catTitle(current.region, current.category)""")
html = html.replace("""  $('level-pill').textContent = 'Level ' + current.level + '/' + totalLevels(current.region, current.category)
    + ' \\u00B7 ' + LEVEL_LABELS[current.level - 1];""",
"""  $('level-pill').textContent = t('case.level') + ' ' + current.level + '/' + totalLevels(current.region, current.category)
    + ' \\u00B7 ' + LEVEL_LABELS[current.level - 1];""")
html = html.replace("""  $('level-count').textContent = doneCount + '/' + current.total + ' answered';""",
                    """  $('level-count').textContent = doneCount + '/' + current.total + ' ' + t('case.answered');""")
html = html.replace("""    obj.textContent = isQuestion
      ? 'Learning objective: apply the basic-science principle behind this question, not a memorised fact.'
      : 'Learning objective: explain the mechanism behind this presentation and justify your chosen diagnosis over the alternatives.';""",
"""    obj.textContent = isQuestion ? t('case.objectiveQ') : t('case.objective');""")
html = html.replace("""    $('case-text').innerHTML = '<strong>Question</strong>' + tpl.stem;""",
                    """    $('case-text').innerHTML = '<strong>' + t('case.question') + '</strong>' + tpl.stem;""")
html = html.replace("""    $('case-text').innerHTML = '<strong>Patient file</strong>' + buildVignette(tpl, isLimb);""",
                    """    $('case-text').innerHTML = '<strong>' + t('case.patientFile') + '</strong>' + buildVignette(tpl, isLimb);""")
html = html.replace("""  fb.innerHTML = '<strong>' + (correct ? 'Spot On.' : 'Incorrect Answer.') + '</strong><br><br>' + tpl.explanation;""",
                    """  fb.innerHTML = '<strong>' + (correct ? t('case.spotOn') : t('case.incorrect')) + '</strong><br><br>' + tpl.explanation;""")
html = html.replace("""  $('summary-title').textContent = 'Level ' + current.level + ' Complete \\u2014 ' + LEVEL_LABELS[current.level - 1];""",
                    """  $('summary-title').textContent = t('case.levelComplete') + ' \\u2014 ' + LEVEL_LABELS[current.level - 1];""")
html = html.replace("""    '<span class="stat-correct">Correct: ' + current.runCorrect + '</span> \\u00B7 ' +
    '<span class="stat-wrong">Wrong: ' + current.runWrong + '</span> \\u00B7 Accuracy: ' + acc + '%' +
    '<br><span style="color:#8c9ba5">Overall: ' + st.correct + ' correct \\u00B7 ' + st.wrong + ' wrong</span>';""",
"""    '<span class="stat-correct">' + t('case.correct') + ': ' + current.runCorrect + '</span> \\u00B7 ' +
    '<span class="stat-wrong">' + t('case.wrong') + ': ' + current.runWrong + '</span> \\u00B7 ' + t('case.accuracy') + ': ' + acc + '%' +
    '<br><span style="color:var(--dim)">' + t('case.overall') + ': ' + st.correct + ' / ' + st.wrong + '</span>';""")
html = html.replace("""  $('next-level-btn').textContent = 'Next Level (' + LEVEL_LABELS[nxt - 1] + ')';""",
                    """  $('next-level-btn').textContent = t('case.nextLevel') + ' (' + LEVEL_LABELS[nxt - 1] + ')';""")
html = html.replace("""  $('level-pill').textContent = 'Section Completed';""",
                    """  $('level-pill').textContent = t('case.sectionDone');""")
html = html.replace("""    '<br>Total answered: ' + (st.correct + st.wrong);""",
                    """    '<br>' + t('case.totalAnswered') + ': ' + (st.correct + st.wrong);""")

# tutor text
html = html.replace("""  fb.innerHTML = '<strong>Socratic prompt</strong><br><br>' + q1 + '<br><br>' + q2 +
    '<br><br><span style="color:#8c9ba5">Reveal the reasoning: ' + esc(first) + '</span>';""",
"""  fb.innerHTML = '<strong>' + t('case.socratic') + '</strong><br><br>' + q1 + '<br><br>' + q2 +
    '<br><br><span style="color:var(--dim)">' + t('case.reasoning') + ': ' + esc(first) + '</span>';""")
html = html.replace("""        if (txt) fb.innerHTML = '<strong>Socratic prompt</strong><br><br>' + esc(txt);""",
                    """        if (txt) fb.innerHTML = '<strong>' + t('case.socratic') + '</strong><br><br>' + esc(txt);""")

# OSCE strings
html = html.replace("""  $('osce-title').textContent = catTitle(region, category) + ' \\u00B7 OSCE station';""",
                    """  $('osce-title').textContent = catTitle(region, category) + ' \\u00B7 ' + t('osce.station');""")
html = html.replace("""    'I was asked to come and talk to you about what has been going on.', 'patient');
  osceSay('Presentation note: '""",
"""    t('osce.patientIntro'), 'patient');
  osceSay(t('osce.note') + ': '""")
html = html.replace("""    osceSay('I am not sure I follow, doctor. Could you ask that another way?', 'patient');""",
                    """    osceSay(t('osce.confused'), 'patient');""")
html = html.replace("""reply = s.redFlags.length ? 'Now that you ask: ' + s.redFlags.join(', ') + '.' : 'Nothing like that, doctor.';""",
                    """reply = s.redFlags.length ? t('osce.redflagAsk') + s.redFlags.join(', ') + '.' : t('osce.nothing');""")
html = html.replace("""    reply = (s.history.associations || []).join(' ') || 'Nothing else that I noticed.';""",
                    """    reply = (s.history.associations || []).join(' ') || t('osce.nothingElse');""")
html = html.replace("""  else if (key === 'associations') reply = (s.history.associations || []).join(' ') || 'Nothing else that I noticed.';""",
                    """  else if (key === 'associations') reply = (s.history.associations || []).join(' ') || t('osce.nothingElse');""")
html = html.replace("""  else reply = s.history[key] || 'I cannot really say, doctor.';""",
                    """  else reply = s.history[key] || t('osce.cannotSay');""")
html = html.replace("""  if (!reply) reply = 'I cannot really say, doctor.';""",
                    """  if (!reply) reply = t('osce.cannotSay');""")

# OSCE stepper labels + hints
html = html.replace("""  const steps = [['history', 'History'], ['exam', 'Examination'], ['ix', 'Investigations'], ['ddx', 'Differential'], ['plan', 'Diagnosis and plan']];""",
                    """  const steps = [['history', t('osce.history')], ['exam', t('osce.exam')], ['ix', t('osce.ix')], ['ddx', t('osce.ddx')], ['plan', t('osce.plan')]];""")
html = html.replace("""'<div class="osce-hintrow">Ask by typing, or tap a prompt. The red flag screen is the step most students skip.</div>' +
      '<div class="osce-inputrow"><input id="osce-q" placeholder="Ask the patient a question" onkeydown="if(event.key===\\'Enter\\')osceAsk()">' +
      '<button class="osce-send" onclick="osceAsk()">Ask</button></div>' +""",
"""'<div class="osce-hintrow">' + t('osce.hintHistory') + '</div>' +
      '<div class="osce-inputrow"><input id="osce-q" placeholder="' + t('osce.qPh') + '" onkeydown="if(event.key===\\'Enter\\')osceAsk()">' +
      '<button class="osce-send" onclick="osceAsk()">' + t('osce.ask') + '</button></div>' +""")
html = html.replace("""'<div class="osce-hintrow">Request only the examinations you would actually perform.</div><div class="osce-chips">'""",
                    """'<div class="osce-hintrow">' + t('osce.hintExam') + '</div><div class="osce-chips">'""")
html = html.replace("""'<div class="osce-hintrow">Every unnecessary test is named on the scorecard.</div><div class="osce-chips">'""",
                    """'<div class="osce-hintrow">' + t('osce.hintIx') + '</div><div class="osce-chips">'""")
html = html.replace("""'<div class="osce-hintrow">Pick up to three, most likely first.</div><div class="osce-chips">'""",
                    """'<div class="osce-hintrow">' + t('osce.hintDdx') + '</div><div class="osce-chips">'""")
html = html.replace("""'<div class="osce-hintrow">Commit to one diagnosis and a safe plan.</div>' +""",
                    """'<div class="osce-hintrow">' + t('osce.hintPlan') + '</div>' +""")
html = html.replace("""'<option value="">Choose your diagnosis</option>'""",
                    """'<option value="">' + t('osce.pickDx') + '</option>'""")
html = html.replace("""oninput="osce.plan=this.value">' + esc(osce.plan) + '</textarea>' +
      '<button class="osce-finish" onclick="osceFinish()">Submit station</button>';""",
"""oninput="osce.plan=this.value">' + esc(osce.plan) + '</textarea>' +
      '<button class="osce-finish" onclick="osceFinish()">' + t('osce.submit') + '</button>';""")
html = html.replace("""'<input placeholder="Reasoning (optional)" value="'""",
                    """'<input placeholder="' + t('osce.reasonPh') + '" value="'""")

# scorecard
html = html.replace("""  let html = '<div class="osce-card"><h3>' + (sc.pass ? 'Pass' : 'Not yet a pass') + ': ' + sc.total + '/100</h3>' +
    bar('History coverage', sc.history, 25) + bar('Red flags', sc.redflags, 20) +
    bar('Examination', sc.exam, 15) + bar('Investigations', sc.ix, 15) +
    bar('Differential diagnosis', sc.ddx, 10) + bar('Final diagnosis', sc.dx, 10) +
    bar('Management safety', sc.mgmt, 10) +
    '<p class="osce-model"><b>Model answer:</b> ' + esc(s.diagnosis) + '. ' + esc(s.explanation) + '</p>' +
    '<p class="osce-model"><b>Safe management:</b> ' + esc(s.management.join('; ')) + '.</p>';
  html += '<h4>Examiner notes</h4><ul class="osce-notes">' +
    (sc.notes.length ? sc.notes.map(n => '<li>' + esc(n) + '</li>').join('') : '<li>Nothing missed. Clean station.</li>') +
    '</ul>';""",
"""  let html = '<div class="osce-card"><h3>' + (sc.pass ? t('osce.pass') : t('osce.fail')) + ': ' + sc.total + '/100</h3>' +
    bar(t('osce.historyCoverage'), sc.history, 25) + bar(t('osce.redflags'), sc.redflags, 20) +
    bar(t('osce.examination'), sc.exam, 15) + bar(t('osce.investigations'), sc.ix, 15) +
    bar(t('osce.ddxScore'), sc.ddx, 10) + bar(t('osce.dxScore'), sc.dx, 10) +
    bar(t('osce.mgmtScore'), sc.mgmt, 10) +
    '<p class="osce-model"><b>' + t('osce.model') + ':</b> ' + esc(s.diagnosis) + '. ' + esc(s.explanation) + '</p>' +
    '<p class="osce-model"><b>' + t('osce.safe') + ':</b> ' + esc(s.management.join('; ')) + '.</p>';
  html += '<h4>' + t('osce.notes') + '</h4><ul class="osce-notes">' +
    (sc.notes.length ? sc.notes.map(n => '<li>' + esc(n) + '</li>').join('') : '<li>' + t('osce.clean') + '</li>') +
    '</ul>';""")
html = html.replace("""'<button class="btn-secondary" onclick="osceRetry()">Retry station</button>' +
    '<button class="btn-secondary" onclick="osceNewPatient()">New patient, same section</button>' +
    '<button class="btn-secondary" onclick="osceLeave()">Back to stations</button></div></div>';""",
"""'<button class="btn-secondary" onclick="osceRetry()">' + t('osce.retry') + '</button>' +
    '<button class="btn-secondary" onclick="osceNewPatient()">' + t('osce.newPatient') + '</button>' +
    '<button class="btn-secondary" onclick="osceLeave()">' + t('osce.backStations') + '</button></div></div>';""")

# video section labels
html = html.replace("""  html += langBlock('lang-ar', 'Arabic lectures', 'AR', ar);
  html += langBlock('lang-en', 'English lectures', 'EN', en);""",
"""  html += langBlock('lang-ar', t('video.ar'), 'AR', ar);
  html += langBlock('lang-en', t('video.en'), 'EN', en);""")
html = html.replace("""  html += '<div class="videos-menu"><button class="btn-secondary" onclick="videosBack()">&#8592; Back to topics</button></div>';""",
                    """  html += '<div class="videos-menu" style="margin-top:20px"><button class="btn-secondary" onclick="videosBack()">&#8592; ' + t('video.topics') + '</button></div>';""")

# splice the app shell before the bootstrap
html = html.replace("renderQuizGrid();\nrenderOsceHome();", APP.strip() + "\n\nrenderQuizGrid();\nrenderOsceHome();", 1)
html = html.replace("var homeBtn = document.querySelector('.nav-btn[data-view=\"landing\"]');",
                    "renderFlash();\napplyLang(localStorage.getItem('medplat-lang') || 'en');\napplyTheme(localStorage.getItem('medplat-theme') || 'system');\napplySize(localStorage.getItem('medplat-size') || 'm');\nvar homeBtn = document.querySelector('.nav-btn[data-view=\"landing\"]');")

open(TPL, "w", encoding="utf-8").write(html)
print("template rebuilt:", len(html), "bytes")
