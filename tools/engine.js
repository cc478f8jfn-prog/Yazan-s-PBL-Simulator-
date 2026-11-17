// ============ Yazan's Medplat engine ============
const SUBJECT_LABELS = {
  anatomy: 'Gross Anatomy', embryology: 'Embryology', histology: 'Histology',
  physiology: 'Physiology', biochemistry: 'Biochemistry', pathology: 'Pathology',
  pharmacology: 'Pharmacology', microbiology: 'Microbiology', immunology: 'Immunology',
  medicine: 'Internal Medicine', surgery: 'Surgery', pediatrics: 'Pediatrics',
  obgyn: 'Obstetrics & Gynaecology', psychiatry: 'Psychiatry'
};

function $(id) { return document.getElementById(id); }
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function loadSave() {
  try { const raw = localStorage.getItem(SAVE_KEY); return raw ? JSON.parse(raw) : {}; }
  catch (e) { return {}; }
}
function persist() { try { localStorage.setItem(SAVE_KEY, JSON.stringify(SAVE)); } catch (e) {} }
function catKey(region, category) { return region + '/' + category; }
function totalLevels(region, category) { return Object.keys(casesData[region][category]).length; }
function levelCases(region, category, lvl) { return casesData[region][category][String(lvl)] || []; }
function stateOf(region, category) {
  const k = catKey(region, category);
  if (!SAVE[k]) SAVE[k] = { level: 1, completed: {}, done: {}, correct: 0, wrong: 0 };
  return SAVE[k];
}
function nextLevel(region, category) {
  const st = stateOf(region, category);
  for (let lvl = 1; lvl <= totalLevels(region, category); lvl++) {
    if (!st.completed[lvl] && levelCases(region, category, lvl).length) return lvl;
  }
  return null;
}

// ---------- navigation with a real back stack ----------
const NAV = [];
let currentView = 'landing';

function viewTarget(name) { return name === 'pbl' ? 'home-screen' : 'view-' + name; }

function paint(name) {
  document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
  const el = document.getElementById(viewTarget(name));
  if (el) el.style.display = 'flex';
  $('app-header').style.display = 'flex';
  $('simulator-screen').style.display = 'none';
  currentView = name;
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector('.nav-btn[data-view="' + name + '"]');
  if (btn) btn.classList.add('active');
  if (name === 'quiz') { renderQuizGrid(); updateHomeStatuses(); }
  if (name === 'pbl') updateHomeStatuses();
  if (name === 'videos') renderVideos();
  window.scrollTo(0, 0);
}

function showView(name) {
  if (name !== currentView) NAV.push(currentView);
  paint(name);
}

function goBack() {
  if (currentView === 'videos') {
    if (vidsState.section) { vidsState.section = null; renderVideos(); return; }
    if (vidsState.subject) { vidsState.subject = null; renderVideos(); return; }
  }
  if (currentView === 'sim') { goHome(); return; }
  paint(NAV.length ? NAV.pop() : 'landing');
}

function goHome() {
  current = null;
  $('simulator-screen').style.display = 'none';
  NAV.length = 0;
  paint(lastRegion === 'quiz' ? 'quiz' : 'pbl');
}
function goLanding() { goHome(); paint('landing'); }

// ---------- quiz grid per track ----------
let quizTrack = 'basic';
function setQuizTrack(track, btn) {
  quizTrack = track;
  document.querySelectorAll('#view-quiz .track-tab').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderQuizGrid();
}
function renderQuizGrid() {
  const grid = $('quiz-grid');
  if (!grid) return;
  const cfg = (TRACKS.quiz && TRACKS.quiz[quizTrack]) || { categories: [] };
  grid.innerHTML = cfg.categories.map(cat => {
    const titles = (CATEGORY_TITLES.quiz || {});
    const label = titles[cat] || cat;
    const meta = CAT_META['quiz/' + cat] || '';
    return '<button class="start-box" onclick="openCategory(\'quiz\',\'' + cat + '\')" data-region="quiz" data-category="' + cat + '">' +
      esc(label) + '<span class="cat-meta">' + meta + '</span></button>';
  }).join('');
}

// ---------- play a level ----------
function openCategory(region, category) {
  lastRegion = region;
  lastCategory = category;
  if (region === 'quiz') quizTrack = (TRACKS.quiz.clinical.categories.indexOf(category) >= 0) ? 'clinical' : 'basic';
  const lvl = nextLevel(region, category);
  if (lvl === null) { showEnd(region, category); return; }
  startLevel(region, category, lvl);
}
function startLevel(region, category, lvl) {
  const st = stateOf(region, category);
  const all = levelCases(region, category, lvl);
  const pool = all.filter(c => !st.done[c.id]);
  current = { region, category, level: lvl, total: all.length, pool,
              runCorrect: 0, runWrong: 0, active: null, optionBtns: [] };
  if (currentView !== 'sim') NAV.push(currentView);
  currentView = 'sim';
  document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
  $('app-header').style.display = 'none';
  $('simulator-screen').style.display = 'block';
  $('summary-view').style.display = 'none';
  $('end-view').style.display = 'none';
  $('diagnostic-text').style.display = 'none';
  $('options-container').style.display = 'grid';
  $('feedback-box').style.display = 'none';
  $('next-button').style.display = 'none';
  renderHeader();
  if (pool.length === 0) { finishLevel(); return; }
  showCase();
}
function catTitle(region, category) {
  const byRegion = CATEGORY_TITLES[region];
  if (byRegion && byRegion[category]) return byRegion[category];
  return category;
}
function renderHeader() {
  const isQuiz = current.region === 'quiz';
  $('sim-title').textContent = isQuiz
    ? 'Quiz: ' + catTitle(current.region, current.category)
    : '\u26A1 ' + (REGION_TITLES[current.region] || '') + ': ' + catTitle(current.region, current.category);
  $('level-pill').textContent = 'Level ' + current.level + '/' + totalLevels(current.region, current.category)
    + ' \u00B7 ' + LEVEL_LABELS[current.level - 1];
  const doneCount = current.total - current.pool.length;
  $('level-count').textContent = doneCount + '/' + current.total + ' answered';
  $('progress-fill').style.width = (current.total ? Math.round(doneCount / current.total * 100) : 0) + '%';
}

// A bare verb phrase needs a subject in front of it; a phrase that already names
// someone (or starts with a noun) must be left alone.
const VERB_START = /^(is|are|was|were|has|had|have|presents|presented|presenting|develops|developed|complains|reports|reported|sustained|suffered|experienced|felt|fell|falls|lands|landed|caught|jammed|pulled|pushed|reached|grabbed|twisted|noticed|started|began|returned|attends|underwent|undergoes|required|received|took|takes|wore|stopped|swallowed|inhaled|drank|ate|comes|arrived|sits|tripped|slipped|collapsed|woke|walks|becomes|describes)\b/i;
const NOUN_START = /^(patient|man|woman|boy|girl|child|infant|baby|elderly|student|athlete|runner|cyclist|swimmer|dancer|mechanic|shopper|worker|driver|farmer|carpenter|teacher|nurse)\b/i;
const LIMB_WORD = /(arm|hand|wrist|elbow|shoulder|leg|knee|ankle|foot|heel|hip|thigh|calf|shin|forearm|finger|thumb|toe|limb)/i;

function buildVignette(tpl, isLimb) {
  let sentence = (tpl.mechanism || '').trim();
  if (/^is an? /i.test(sentence)) sentence = sentence.replace(/^is /i, '');
  let prefix = '';
  if (NOUN_START.test(sentence) && !/^a |^an |^the /i.test(sentence)) {
    prefix = 'A ';
  } else if (VERB_START.test(sentence)) {
    if (isLimb) {
      const age = 18 + Math.floor(Math.random() * 52);
      const g = genders[Math.floor(Math.random() * genders.length)];
      const occ = occupations[Math.floor(Math.random() * occupations.length)];
      prefix = 'A ' + age + '-year-old ' + g.id + ' ' + occ + ' ';
    } else {
      prefix = 'A patient ';
    }
  }
  sentence = prefix + sentence;
  if (!prefix) sentence = sentence.charAt(0).toUpperCase() + sentence.slice(1);
  sentence = sentence.replace(/\.+\s*$/, '');
  if (/\?$/.test(sentence)) return sentence;
  if (isLimb && LIMB_WORD.test(sentence) && !/bilateral|both |\b(right|left)\b/i.test(sentence)) {
    sentence += ' on the ' + sides[Math.floor(Math.random() * sides.length)] + ' side';
  }
  return sentence + '. On examination, ' + (tpl.exam || '');
}

function showCase() {
  const idx = Math.floor(Math.random() * current.pool.length);
  const tpl = current.pool.splice(idx, 1)[0];
  current.active = tpl;
  current.optionBtns = [];
  const isQuestion = !!tpl.stem;
  if (isQuestion) {
    $('case-text').innerHTML = '<strong>Question:</strong><br><br>' + tpl.stem;
    $('diagnostic-text').style.display = 'none';
  } else {
    const isLimb = current.region === 'msk';
    $('case-text').innerHTML = '<strong>Patient File:</strong><br><br>' + buildVignette(tpl, isLimb);
    $('diagnostic-text').innerHTML = tpl.diagnostic || '';
    $('diagnostic-text').style.display = 'block';
  }
  $('feedback-box').style.display = 'none';
  $('next-button').style.display = 'none';
  const oc = $('options-container');
  oc.innerHTML = '';
  const order = tpl.options.map((t, i) => ({ t, i })).sort(() => Math.random() - 0.5);
  order.forEach(({ t, i }) => {
    const b = document.createElement('button');
    b.className = 'option-btn';
    b.innerText = t;
    b.onclick = () => checkAnswer(i, b);
    oc.appendChild(b);
    current.optionBtns.push({ btn: b, orig: i });
  });
  renderHeader();
}
function checkAnswer(selIdx, btn) {
  const tpl = current.active;
  if (!tpl) return;
  const correct = selIdx === tpl.answer;
  document.querySelectorAll('.option-btn').forEach(b => b.disabled = true);
  current.optionBtns.forEach(({ btn: b, orig }) => {
    if (orig === tpl.answer) { b.style.background = '#27ae60'; b.style.borderColor = '#2ecc71'; }
  });
  if (!correct) { btn.style.background = '#c0392b'; btn.style.borderColor = '#e74c3c'; }
  const fb = $('feedback-box');
  fb.className = correct ? 'feedback correct-feedback' : 'feedback incorrect-feedback';
  fb.innerHTML = '<strong>' + (correct ? 'Spot On.' : 'Incorrect Answer.') + '</strong><br><br>' + tpl.explanation;
  fb.style.display = 'block';
  const st = stateOf(current.region, current.category);
  st.done[tpl.id] = correct ? 'c' : 'w';
  if (correct) { st.correct++; current.runCorrect++; } else { st.wrong++; current.runWrong++; }
  persist();
  $('next-button').style.display = 'block';
}
function nextCase() {
  if (current.pool.length === 0) { finishLevel(); return; }
  showCase();
}
function finishLevel() {
  const st = stateOf(current.region, current.category);
  st.completed[current.level] = true;
  persist();
  const nxt = nextLevel(current.region, current.category);
  if (nxt === null) { showEnd(current.region, current.category); return; }
  $('diagnostic-text').style.display = 'none';
  $('options-container').style.display = 'none';
  $('feedback-box').style.display = 'none';
  $('next-button').style.display = 'none';
  $('summary-view').style.display = 'block';
  const totalRun = current.runCorrect + current.runWrong;
  const acc = totalRun ? Math.round(current.runCorrect / totalRun * 100) : 0;
  $('summary-title').textContent = 'Level ' + current.level + ' Complete \u2014 ' + LEVEL_LABELS[current.level - 1];
  $('summary-stats').innerHTML =
    '<span class="stat-correct">Correct: ' + current.runCorrect + '</span> \u00B7 ' +
    '<span class="stat-wrong">Wrong: ' + current.runWrong + '</span> \u00B7 Accuracy: ' + acc + '%' +
    '<br><span style="color:#8c9ba5">Overall: ' + st.correct + ' correct \u00B7 ' + st.wrong + ' wrong</span>';
  $('next-level-btn').textContent = 'Next Level (' + LEVEL_LABELS[nxt - 1] + ')';
}
function goNextLevel() {
  const nxt = nextLevel(current.region, current.category);
  if (nxt) startLevel(current.region, current.category, nxt);
}
function retryLevel() {
  const st = stateOf(current.region, current.category);
  levelCases(current.region, current.category, current.level).forEach(c => { delete st.done[c.id]; });
  delete st.completed[current.level];
  persist();
  startLevel(current.region, current.category, current.level);
}
function showEnd(region, category) {
  const st = stateOf(region, category);
  if (currentView !== 'sim') NAV.push(currentView);
  current = { region, category, level: 1 };
  currentView = 'sim';
  document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
  $('app-header').style.display = 'none';
  $('simulator-screen').style.display = 'block';
  $('summary-view').style.display = 'none';
  $('end-view').style.display = 'block';
  $('diagnostic-text').style.display = 'none';
  $('options-container').style.display = 'none';
  $('feedback-box').style.display = 'none';
  $('next-button').style.display = 'none';
  $('sim-title').textContent = region === 'quiz'
    ? 'Quiz: ' + catTitle(region, category)
    : '\u26A1 ' + (REGION_TITLES[region] || '') + ': ' + catTitle(region, category);
  $('level-pill').textContent = 'Section Completed';
  $('level-count').textContent = '';
  $('progress-fill').style.width = '100%';
  $('end-stats').innerHTML =
    '<span class="stat-correct">Correct: ' + st.correct + '</span> \u00B7 ' +
    '<span class="stat-wrong">Wrong: ' + st.wrong + '</span>' +
    '<br>Total answered: ' + (st.correct + st.wrong);
  current = null;
}
function resetSection() {
  delete SAVE[catKey(lastRegion, lastCategory)];
  persist();
  startLevel(lastRegion, lastCategory, 1);
}

// ============ Video library ============
const VIDEO_INDEX = {};
Object.keys(VIDEO_DATA).forEach(subj => {
  Object.keys(VIDEO_DATA[subj]).forEach(sec => {
    const s = VIDEO_DATA[subj][sec];
    (s.ar || []).concat(s.en || []).forEach(v => {
      VIDEO_INDEX[v[0]] = { title: v[1], channel: v[2], lang: v[3], sec: s.name, subject: subj };
    });
  });
});

function openVideoPlayer(vid, title) {
  document.getElementById('video-player-title').textContent = title;
  document.getElementById('video-player-frame').innerHTML =
    '<iframe src="https://www.youtube.com/embed/' + vid + '?rel=0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>';
  document.getElementById('video-player-watch').href = 'https://www.youtube.com/watch?v=' + vid;
  document.getElementById('video-player-overlay').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}
function closeVideoPlayer() {
  document.getElementById('video-player-overlay').style.display = 'none';
  document.getElementById('video-player-frame').innerHTML = '';
  document.body.style.overflow = '';
}
function playVideo(id) {
  const v = VIDEO_INDEX[id];
  if (v) openVideoPlayer(id, v.title);
}
document.addEventListener('DOMContentLoaded', function () {
  var ov = document.getElementById('video-player-overlay');
  if (ov) ov.addEventListener('click', function (e) { if (e.target === this) closeVideoPlayer(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeVideoPlayer(); });
});

let vidsState = { track: 'basic', subject: null, section: null };

function setVideoTrack(track, btn) {
  vidsState = { track: track, subject: null, section: null };
  document.querySelectorAll('#view-videos .track-tab').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderVideos();
}

function subjectLabel(key) { return SUBJECT_LABELS[key] || key; }

function videoCard(v) {
  const id = v[0], title = esc(v[1]), ch = esc(v[2]), lang = v[3], exp = v[4];
  const chip = lang === 'ar' ? '<span class="chip chip-ar">AR</span>' : '<span class="chip chip-en">EN</span>';
  const expBadge = exp ? ' <span class="chip chip-exp">EXPLANATION</span>' : '';
  return '<a class="video-card" href="javascript:void(0)" onclick="playVideo(\'' + id + '\')">' +
    '<span class="video-thumb-wrap"><img class="video-thumb" loading="lazy" src="https://i.ytimg.com/vi/' + id +
    '/hqdefault.jpg" alt="" onerror="this.src=\'https://i.ytimg.com/vi/' + id + '/mqdefault.jpg\'">' +
    '<span class="vid-play-badge">&#9654;</span></span>' +
    '<div class="video-title">' + title + '</div>' +
    '<span class="vch">' + ch + ' ' + chip + expBadge + '</span></a>';
}

function langBlock(cls, label, tag, videos) {
  if (!videos.length) return '';
  return '<div class="lang-block"><div class="lang-title ' + cls + '">' + label +
    ' <span class="lang-tag">' + tag + '</span></div><div class="video-grid">' +
    videos.map(videoCard).join('') + '</div></div>';
}

function renderVideos() {
  const r = $('videos-root');
  if (!r) return;
  const cfg = (TRACKS.videos && TRACKS.videos[vidsState.track]) || { subjects: [] };

  if (!vidsState.subject) {
    if (!cfg.subjects.length) { r.innerHTML = '<p class="vid-note">Nothing here yet.</p>'; return; }
    r.innerHTML = '<div class="videos-menu">' + cfg.subjects.map(s => {
      const secs = VIDEO_DATA[s] || {};
      const n = Object.keys(secs).reduce((a, k) => a + (secs[k].ar || []).length + (secs[k].en || []).length, 0);
      return '<button class="vid-sub-btn" onclick="videosShow(\'' + s + '\')">' + esc(subjectLabel(s)) +
        '<span class="vid-count">' + Object.keys(secs).length + ' sections &middot; ' + n + ' videos</span></button>';
    }).join('') + '</div>';
    return;
  }

  const subj = VIDEO_DATA[vidsState.subject] || {};
  if (!vidsState.section) {
    let html = '<p class="vid-crumb">' + esc(subjectLabel(vidsState.subject)) + '</p><div class="cat-grid">';
    Object.keys(subj).forEach(k => {
      const s = subj[k];
      const n = (s.ar || []).length + (s.en || []).length;
      html += '<button class="start-box" onclick="videosSection(\'' + k + '\')">' + esc(s.name) +
        '<span class="cat-meta">' + n + ' videos &middot; ' + (s.ar || []).length + ' Arabic / ' +
        (s.en || []).length + ' English</span></button>';
    });
    html += '</div>';
    r.innerHTML = html;
    return;
  }

  const sec = subj[vidsState.section];
  if (!sec) { r.innerHTML = '<p class="vid-note">No videos in this section yet.</p>'; return; }
  const ar = sec.ar || [], en = sec.en || [];
  let html = '<p class="vid-crumb">' + esc(subjectLabel(vidsState.subject)) + ' &rsaquo; <b>' + esc(sec.name) + '</b></p>';
  html += langBlock('lang-ar', 'Arabic lectures', 'AR', ar);
  html += langBlock('lang-en', 'English lectures', 'EN', en);
  if (!ar.length && !en.length) html += '<p class="vid-note">No videos in this section yet.</p>';
  if (!en.length) html += '<p class="vid-empty">No English lectures for this section yet.</p>';
  if (!ar.length) html += '<p class="vid-empty">No Arabic lectures for this section yet.</p>';
  r.innerHTML = html;
}

function videosRoot() { vidsState = { track: vidsState.track || 'basic', subject: null, section: null }; renderVideos(); }
function videosShow(subject) { vidsState.subject = subject; vidsState.section = null; renderVideos(); }
function videosSection(sec) { vidsState.section = sec; renderVideos(); }
function videosBack() {
  if (vidsState.section) vidsState.section = null;
  else vidsState.subject = null;
  renderVideos();
}

// ---------- home screen statuses and category metadata ----------
function updateHomeStatuses() {
  document.querySelectorAll('.start-box[data-region]').forEach(btn => {
    const region = btn.getAttribute('data-region');
    const category = btn.getAttribute('data-category');
    if (!region || !category || !casesData[region] || !casesData[region][category]) return;
    const meta = CAT_META[catKey(region, category)];
    const metaSpan = btn.querySelector('.cat-meta');
    if (metaSpan && meta) metaSpan.textContent = meta.replace('&middot;', '\u00B7');
    const st = stateOf(region, category);
    const total = totalLevels(region, category);
    const lvl = nextLevel(region, category);
    let status;
    if (lvl === null) status = '\u2713 Section done \u00B7 retry available';
    else {
      const all = levelCases(region, category, lvl);
      const doneCount = all.filter(c => st.done[c.id]).length;
      status = 'Level ' + lvl + '/' + total + ' \u00B7 ' + doneCount + '/' + all.length + ' answered';
    }
    let span = btn.querySelector('.cat-status');
    if (!span) { span = document.createElement('span'); span.className = 'cat-status'; btn.appendChild(span); }
    span.textContent = status;
  });
}

renderQuizGrid();
updateHomeStatuses();
