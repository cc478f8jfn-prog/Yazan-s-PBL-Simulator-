// ============ Dual-mode simulator ============
// A case runs either as Pre-clinical PBL or as a Clinical OSCE station. Nothing is
// duplicated in the data: the OSCE station is derived from the same record
// (mechanism, exam, diagnostic, explanation, options). A case can override any part
// by carrying its own `osce` object.

const OSCE_INTENTS = [
  { key: 'onset', label: 'Onset and duration', re: /(when|onset|start|how long|duration|began|since|first notice)/i },
  { key: 'character', label: 'Character', re: /(character|describe|what kind|type of|quality|sharp|dull|burning|crushing|like what)/i },
  { key: 'radiation', label: 'Radiation', re: /(radiat|spread|travel|move anywhere|go anywhere|elsewhere)/i },
  { key: 'associations', label: 'Associated symptoms', re: /(associat|anything else|other symptom|also|nausea|vomit|fever|weight|numb|weak|bladder|bowel|vision|breath|sweat)/i },
  { key: 'timing', label: 'Pattern', re: /(constant|intermittent|comes and goes|night|morning|pattern|worse at|progress)/i },
  { key: 'aggravating', label: 'Aggravating factors', re: /(aggravat|worse with|worse when|trigger|bring on|make it worse)/i },
  { key: 'relieving', label: 'Relieving factors', re: /(reliev|better with|better when|ease|help it|take anything)/i },
  { key: 'severity', label: 'Severity', re: /(sever|scale|out of ten|out of 10|how bad|mild|moderate)/i },
  { key: 'pmh', label: 'Past history', re: /(past|previous|medical history|condition|surger|operation|admitted|illness|diagnos)/i },
  { key: 'drugs', label: 'Drugs and allergies', re: /(medication|medicine|drug|tablet|taking|allerg|prescri)/i },
  { key: 'family', label: 'Family history', re: /(family|relativ|hereditar|runs in)/i },
  { key: 'social', label: 'Social history', re: /(smok|alcohol|drink|work|occupation|job|live|diet|travel|exercise)/i },
  { key: 'redflags', label: 'Red flag screen', re: /(red flag|weight loss|night sweat|fever|losing weight|incontinen|saddle|progressive|both leg|both side|urgent|serious)/i }
];

const RED_FLAG_TERMS = [
  ['weight loss', /weight loss|losing weight|cachexia/i],
  ['night sweats', /night sweat/i],
  ['fever', /fever|pyrexia/i],
  ['bladder or bowel dysfunction', /incontinen|retention of urine|bowel dysfunction|saddle/i],
  ['progressive weakness', /progressive (weakness|numbness)|worsening (weakness|deficit)/i],
  ['bilateral symptoms', /bilateral|both (hands|legs|arms|feet|sides)/i],
  ['significant trauma', /fall|accident|trauma|fracture|collision|impact/i],
  ['possible malignancy', /cancer|malignan|tumour|tumor|neoplasm|carcinoma|sarcoma/i],
  ['vascular compromise', /pulseless|pallor|ischemi|ischaemi|compartment|gangrene/i],
  ['systemic illness', /sepsis|shock|hypotension|tachycardia/i]
];

const EXAM_SYSTEMS = [
  { key: 'general', label: 'General inspection', re: /(pallor|jaundice|cyanosis|clubbing|lymph|weight|cachexia|distress|sweat)/i },
  { key: 'vitals', label: 'Vital signs', re: /(blood pressure|bp\b|pulse|tachycard|bradycard|hypotens|hypertens|fever|temperature|respiratory rate|saturat|shock)/i },
  { key: 'local', label: 'Local examination', re: /(swelling|lump|tender|tenderness|erythema|warm|deformity|effusion|restrict|range of motion|crepitus|mass|scar)/i },
  { key: 'neuro', label: 'Neurological examination', re: /(sensat|sensory|numb|reflex|power|weakness|paresis|tone|proprioce|nerve|dermatome|gait|coordination)/i },
  { key: 'vascular', label: 'Vascular examination', re: /(pulse|pulseless|capillary|venous|arterial|bruit|doppler|ulcer|oedema|edema)/i },
  { key: 'cardioresp', label: 'Cardiorespiratory examination', re: /(murmur|heart sound|breath sound|crepitation|crackles|wheeze|rub|jvp|pericard|lung|chest)/i },
  { key: 'abdominal', label: 'Abdominal examination', re: /(abdomen|abdominal|epigastric|hepatomegaly|splenomegaly|guarding|rigidity|bowel sound|distension)/i }
];

const IX_MENU = [
  { key: 'bloods', label: 'Blood tests', re: /(lab|blood|serum|haemat|hemat|anaemi|anemi|crp|esr|electrolyte|sodium|potassium|calcium|glucose|troponin|enzyme|ferritin|vitamin)/i },
  { key: 'xray', label: 'Plain radiograph', re: /(x-ray|radiograph|radiolog)/i },
  { key: 'ct', label: 'CT scan', re: /(ct\b|computed tomograph)/i },
  { key: 'mri', label: 'MRI', re: /(mri|magnetic resonance)/i },
  { key: 'us', label: 'Ultrasound', re: /(ultrasound|sonograph|echo)/i },
  { key: 'ecg', label: 'ECG', re: /(ecg|ekg|electrocardio)/i },
  { key: 'neurophys', label: 'Nerve conduction and EMG', re: /(emg|ncv|nerve conduction|electromyograph|electrodiagnostic)/i },
  { key: 'histo', label: 'Biopsy and histopathology', re: /(histolog|biopsy)/i },
  { key: 'micro', label: 'Microbiology', re: /(culture|gram stain|pcr|serolog|microbiolog)/i }
];

const MGMT_BY_CATEGORY = {
  'msk/nerves': ['Analgesia and activity modification', 'Nerve conduction study', 'Surgical decompression when deficits progress', 'Safety-net advice and review'],
  'msk/muscles': ['Analgesia and protected loading', 'Physiotherapy with graded strengthening', 'Exclude compartment syndrome', 'Orthopaedic referral if the tendon is ruptured'],
  'msk/bones': ['Analgesia and immobilisation', 'Imaging to confirm the fracture pattern', 'Orthopaedic referral for reduction or fixation', 'Neurovascular observation'],
  'msk/general': ['Analgesia and rest', 'Targeted imaging', 'Orthopaedic or rheumatology referral', 'Safety-net advice'],
  'physiology/blood': ['Correct the fluid or electrolyte deficit', 'Repeat electrolytes and haematocrit', 'Avoid rapid over-correction', 'Review drugs that disturb sodium or volume'],
  'physiology/cardio': ['ECG and haemodynamic assessment', 'Treat the underlying cardiac cause', 'Fluid and rate control as indicated', 'Escalate if there is shock or ischaemia'],
  'physiology/resp': ['Oxygen to target saturation', 'Blood gases to assess ventilation', 'Treat the precipitating cause', 'Escalate if work of breathing rises'],
  'physiology/renal': ['Assess volume status and urine output', 'Correct electrolyte and acid-base disturbance', 'Review nephrotoxic drugs', 'Nephrology referral if function deteriorates'],
  'physiology/endocrine': ['Confirm the hormonal axis', 'Correct the metabolic derangement', 'Endocrinology involvement', 'Patient education and follow-up'],
  'physiology/git': ['Assess hydration and nutrition', 'Treat the underlying gastrointestinal cause', 'Review drugs and diet triggers', 'Refer if there is bleeding or obstruction'],
  'physiology/repro': ['Confirm with a hormone or imaging test', 'Explain the findings and options', 'Obstetrics and gynaecology referral', 'Safety-net for pregnancy complications'],
  'physiology/immune': ['Look for underlying immunodeficiency', 'Treat infection promptly', 'Vaccination and prophylaxis review', 'Immunology referral'],
  'physiology/nerve_muscle': ['Confirm with nerve conduction or EMG', 'Physiotherapy and rehabilitation', 'Treat the underlying neuromuscular cause', 'Monitor respiratory function'],
  'physiology/cell': ['Correct the membrane or transport defect', 'Monitor electrolytes and osmolality', 'Review drugs affecting transport', 'Reassess after correction'],
  'embryology/level1': ['Explain the developmental basis', 'Arrange the appropriate screening test', 'Fetal medicine referral', 'Document counselling'],
  'embryology/level2': ['Counsel the parents on the anomaly', 'Paediatric surgical review', 'Plan delivery with neonatal support', 'Genetic counselling where relevant'],
  'embryology/level3': ['Confirm the defect with imaging', 'Multidisciplinary team discussion', 'Corrective surgery planning', 'Developmental follow-up'],
  'embryology/level4': ['Confirm the diagnosis', 'Involve the relevant specialty early', 'Parental counselling and consent', 'Structured follow-up'],
  'pathology/general': ['Treat the underlying pathological process', 'Targeted investigations', 'Multidisciplinary management', 'Follow-up with histology or imaging']
};

const MGMT_KEYWORDS = [
  [/surg|decompress|reduction|fixation|repair|excision|drainage|laparotom/i, 'Surgical referral'],
  [/antibiotic|antimicrob|penicillin|ceftriaxone/i, 'Antibiotic therapy'],
  [/anticoagul|heparin|warfarin/i, 'Anticoagulation assessment'],
  [/steroid|corticosteroid|immunosuppress/i, 'Steroid or immunosuppression decision'],
  [/insulin|glucose control/i, 'Glycaemic control'],
  [/thrombolys|stent|angioplast|revascularis/i, 'Urgent revascularisation'],
  [/transfus|blood products/i, 'Transfusion if indicated'],
  [/physiotherap|rehabilitat/i, 'Physiotherapy and rehabilitation']
];

const OSCE_SYSTEM_PROMPTS = {
  patient: 'You are a standardized patient in a medical school OSCE. Stay in role. Never volunteer a diagnosis, a test result or a plan. Answer only what is asked, in one or two short sentences, first person. Reveal a red flag only when the student asks a targeted question that would uncover it. If asked something outside your knowledge, say you do not know. Never break character during the station.',
  examiner: 'You are a senior OSCE examiner writing a structured scorecard. Judge only what the candidate actually did in the transcript. Score history coverage including SOCRATES, red flags identified, appropriateness of examination, appropriateness of investigations naming any unnecessary test, differential quality, final diagnostic accuracy and management safety. Be specific, quote the candidate where it matters, list misses as bullets, finish with three concrete improvements and a pass or fail against a 60 percent cut score.',
  tutor: 'You are a Socratic PBL tutor for pre-clinical students. Never give the answer. Ask one focused question at a time that moves the student from the clinical finding to the mechanism, then to the diagnosis. Keep every reply under 40 words.'
};

function llmSettings() {
  try { return JSON.parse(localStorage.getItem('medplat-llm') || '{}'); } catch (e) { return {}; }
}
function saveLlmSettings(o) { try { localStorage.setItem('medplat-llm', JSON.stringify(o)); } catch (e) {} }
function llmReady() { const s = llmSettings(); return !!(s.endpoint && s.key); }
function llmCall(systemPrompt, userPrompt) {
  const s = llmSettings();
  if (!s.endpoint || !s.key) return Promise.resolve(null);
  return fetch(s.endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + s.key },
    body: JSON.stringify({
      model: s.model || 'gpt-4o-mini',
      messages: [{ role: 'system', content: systemPrompt }, { role: 'user', content: userPrompt }],
      temperature: 0.4
    })
  }).then(r => r.json())
    .then(d => (d.choices && d.choices[0] && d.choices[0].message && d.choices[0].message.content) || null)
    .catch(() => null);
}

// ---------- derive the station ----------
function splitSentences(text) {
  return String(text || '').split(/(?<=[.!?])\s+/).map(s => s.trim()).filter(s => s.length > 3);
}

function deriveOsce(c) {
  const mech = c.mechanism || c.stem || '';
  const exam = c.exam || '';
  const diag = c.diagnostic || '';
  const expl = c.explanation || '';
  const all = [mech, exam, diag, expl].join(' ');
  const history = {};
  const examFindings = {};

  splitSentences(exam).forEach(sentence => {
    const low = sentence.toLowerCase();
    if (/(radiat|spread to|travels to)/.test(low)) history.radiation = history.radiation || sentence;
    else if (/(worse with|aggravat|triggered by)/.test(low)) history.aggravating = history.aggravating || sentence;
    else if (/(relieved by|better with|eases)/.test(low)) history.relieving = history.relieving || sentence;
    else if (/(for \d|since|weeks|months|days|hours|sudden|gradual)/.test(low)) history.onset = history.onset || sentence;
    else if (/(sharp|dull|burning|crushing|aching|throbbing|colicky)/.test(low)) history.character = history.character || sentence;
    else if (/(constant|intermittent|comes and goes|night|morning)/.test(low)) history.timing = history.timing || sentence;
    else if (/(nausea|vomit|fever|weight loss|numb|weakness|blurr|breath|sweat|paresthes)/.test(low)) {
      (history.associations = history.associations || []).push(sentence);
    } else {
      const sys = EXAM_SYSTEMS.find(s => s.re.test(low));
      if (sys) { (examFindings[sys.key] = examFindings[sys.key] || []).push(sentence); }
    }
  });
  splitSentences(diag).forEach(sentence => {
    const sys = EXAM_SYSTEMS.find(s => s.re.test(sentence));
    if (sys) { (examFindings[sys.key] = examFindings[sys.key] || []).push(sentence); }
  });

  if (!history.onset) {
    const age = (mech.match(/(\d{1,3})-year-old/) || [])[1];
    history.onset = age ? 'I am ' + age + ' years old, and this has been building up.' : 'It came on recently.';
  }
  if (!history.character) history.character = mech.replace(/^presents? with /i, '').replace(/\.$/, '');
  if (!history.timing) history.timing = 'It has been like this for a while now.';
  if (!history.severity) history.severity = 'It is bad enough that it is affecting what I can do.';

  const redFlags = [];
  RED_FLAG_TERMS.forEach(pair => { if (pair[1].test(all)) redFlags.push(pair[0]); });

  const investigations = [];
  splitSentences(diag).forEach(sentence => {
    const item = IX_MENU.find(ix => ix.re.test(sentence));
    if (item && !investigations.some(i => i.key === item.key)) {
      investigations.push({ key: item.key, label: item.label, result: sentence });
    }
  });
  if (!investigations.length) {
    const guess = IX_MENU.find(ix => ix.re.test(all));
    if (guess) investigations.push({ key: guess.key, label: guess.label, result: diag || 'The result is reported with the case.' });
  }

  const key = c.__region + '/' + c.__category;
  const mgmt = (MGMT_BY_CATEGORY[key] || ['Treat the underlying cause', 'Targeted investigation', 'Appropriate referral', 'Safety-net and follow-up']).slice();
  MGMT_KEYWORDS.forEach(pair => { if (pair[0].test(expl) && mgmt.indexOf(pair[1]) < 0) mgmt.push(pair[1]); });

  return {
    persona: {
      age: (mech.match(/(\d{1,3})-year-old/) || [])[1] || null,
      sex: /woman|female|girl|she\b/i.test(all) ? 'female' : (/man|male|boy|he\b/i.test(all) ? 'male' : 'patient')
    },
    chief: mech.replace(/^presents? with /i, '').replace(/\.$/, ''),
    history: history,
    redFlags: redFlags,
    exam: examFindings,
    investigations: investigations,
    ddx: (c.options || []).slice(),
    diagnosis: (c.options || [])[c.answer] || '',
    management: mgmt,
    explanation: expl
  };
}

// ---------- station state ----------
let osce = null;

function openCategory(region, category) {
  lastRegion = region;
  lastCategory = category;
  if (region === 'quiz') {
    quizTrack = (TRACKS.quiz.clinical.categories.indexOf(category) >= 0) ? 'clinical' : 'basic';
  }
  openModePicker(region, category);
}

function openModePicker(region, category) {
  const lvl = nextLevel(region, category);
  const picker = $('mode-picker');
  $('mode-title').textContent = (REGION_TITLES[region] || '') + ': ' + catTitle(region, category);
  $('mode-sub').textContent = lvl === null
    ? 'Every level in this section is finished. Both modes are still open.'
    : 'Level ' + lvl + ' of ' + totalLevels(region, category) + '. Pick how you want to run it.';
  picker.style.display = 'flex';
  picker.dataset.region = region;
  picker.dataset.category = category;
}

function closeModePicker() { $('mode-picker').style.display = 'none'; }

function chooseMode(mode) {
  const picker = $('mode-picker');
  const region = picker.dataset.region;
  const category = picker.dataset.category;
  closeModePicker();
  if (mode === 'clinical') {
    const lvl = nextLevel(region, category);
    startOSCE(region, category, lvl === null ? 1 : lvl);
  } else {
    const lvl = nextLevel(region, category);
    if (lvl === null) { showEnd(region, category); return; }
    startLevel(region, category, lvl);
  }
}

function startOSCE(region, category, lvl) {
  const all = levelCases(region, category, lvl);
  if (!all.length) { return; }
  const tpl = all[Math.floor(Math.random() * all.length)];
  tpl.__region = region;
  tpl.__category = category;
  osce = {
    region: region, category: category, level: lvl, tpl: tpl,
    st: deriveOsce(tpl),
    asked: {}, examDone: {}, ixOrdered: [], ddx: [], ddxNote: '',
    finalDx: '', plan: '', step: 'history', transcript: [], scored: null
  };
  if (currentView !== 'sim') NAV.push(currentView);
  currentView = 'sim';
  document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
  $('app-header').style.display = 'none';
  $('simulator-screen').style.display = 'none';
  $('osce-screen').style.display = 'block';
  $('osce-title').textContent = catTitle(region, category) + ' \u00B7 OSCE station';
  osce.transcript = [];
  osceSay('Hello doctor. I am ' + (osce.st.persona.age ? osce.st.persona.age + ' years old. ' : '') +
    'I came in because of ' + osce.st.chief + '.', 'patient');
  osceGo('history');
  window.scrollTo(0, 0);
}

function osceSay(text, who) {
  osce.transcript.push({ text: text, who: who });
  const chat = $('osce-chat');
  if (!chat) return;
  const d = document.createElement('div');
  d.className = 'osce-msg ' + (who === 'patient' ? 'osce-patient' : (who === 'you' ? 'osce-you' : 'osce-system'));
  d.textContent = text;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

function osceAsk() {
  const input = $('osce-q');
  if (!input) return;
  const q = input.value.trim();
  if (!q) return;
  input.value = '';
  osceSay(q, 'you');
  const intent = OSCE_INTENTS.find(i => i.re.test(q));
  if (!intent) {
    osceSay('I am not sure I follow, doctor. Could you ask that another way?', 'patient');
    renderOscePanel();
    return;
  }
  osce.asked[intent.key] = true;
  const s = osce.st;
  let reply;
  if (intent.key === 'associations') reply = (s.history.associations || []).join(' ') || 'Nothing else that I noticed.';
  else if (intent.key === 'redflags') reply = s.redFlags.length ? 'Now that you ask: ' + s.redFlags.join(', ') + '.' : 'Nothing like that, doctor.';
  else if (intent.key === 'pmh') reply = s.history.pmh || 'No long-standing illnesses that I know of.';
  else if (intent.key === 'drugs') reply = s.history.drugs || 'Only what the doctor prescribed. No allergies.';
  else if (intent.key === 'family') reply = s.history.family || 'Nobody in the family has had this.';
  else if (intent.key === 'social') reply = s.history.social || 'I do not smoke, and I drink very rarely.';
  else reply = s.history[intent.key] || 'I cannot really say, doctor.';
  osceSay(reply, 'patient');
  if (llmReady()) {
    const prompt = 'Station data: ' + JSON.stringify({ chief: s.chief, history: s.history, redFlags: s.redFlags }) +
      '\nCandidate asked: ' + q + '\nAnswer in role in at most two sentences.';
    llmCall(OSCE_SYSTEM_PROMPTS.patient, prompt).then(txt => { if (txt) osceSay(txt, 'patient'); });
  }
  renderOscePanel();
}

function osceQuick(key) {
  const intent = OSCE_INTENTS.find(i => i.key === key);
  if (!intent) return;
  const map = {
    onset: 'When did this start, and how long has it been going on?',
    character: 'Can you describe the feeling for me?',
    radiation: 'Does it spread anywhere else?',
    associations: 'Anything else going on, such as nausea, fever or numbness?',
    timing: 'Is it there all the time or does it come and go?',
    aggravating: 'What makes it worse?',
    relieving: 'Does anything make it better?',
    severity: 'How bad is it on a scale of one to ten?'
  };
  const q = map[key] || intent.label + '?';
  osceSay(q, 'you');
  osce.asked[key] = true;
  const s = osce.st;
  let reply;
  if (key === 'associations') reply = (s.history.associations || []).join(' ') || 'Nothing else that I noticed.';
  else reply = s.history[key] || 'I cannot really say, doctor.';
  osceSay(reply, 'patient');
  renderOscePanel();
}

function osceExamine(key) {
  const sys = EXAM_SYSTEMS.find(x => x.key === key);
  if (!sys) return;
  osce.examDone[key] = true;
  const found = osce.st.exam[key] || [];
  osceSay('Examination: ' + sys.label + '. ' + (found.length ? found.join(' ') : 'No abnormality detected.'), 'system');
  renderOscePanel();
}

function osceOrderIx(key) {
  const item = IX_MENU.find(x => x.key === key);
  if (!item) return;
  if (!osce.ixOrdered.some(i => i.key === key)) osce.ixOrdered.push({ key: key, label: item.label });
  const hit = osce.st.investigations.find(i => i.key === key);
  osceSay('Investigation: ' + item.label + '. ' + (hit ? hit.result : 'Normal or non-contributory.'), 'system');
  renderOscePanel();
}

function osceToggleDdx(option, btn) {
  const i = osce.ddx.indexOf(option);
  if (i >= 0) { osce.ddx.splice(i, 1); if (btn) btn.classList.remove('picked'); }
  else if (osce.ddx.length < 3) { osce.ddx.push(option); if (btn) btn.classList.add('picked'); }
  renderOscePanel();
}

function osceGo(step) {
  osce.step = step;
  renderOscePanel();
}

function osceScore() {
  const s = osce.st;
  const sc = { history: 0, redflags: 0, exam: 0, ix: 0, ddx: 0, dx: 0, mgmt: 0, notes: [] };
  const historyKeys = ['onset', 'character', 'radiation', 'timing', 'aggravating', 'relieving', 'severity', 'associations', 'pmh', 'drugs', 'family', 'social'];
  const available = historyKeys.filter(k => s.history[k]);
  const covered = available.filter(k => osce.asked[k]);
  sc.history = available.length ? Math.round(25 * covered.length / available.length) : 25;
  available.forEach(k => {
    if (!osce.asked[k]) {
      const label = (OSCE_INTENTS.find(i => i.key === k) || { label: k }).label;
      sc.notes.push('History missed: ' + label);
    }
  });

  if (s.redFlags.length) {
    sc.redflags = osce.asked.redflags ? 20 : 0;
    if (!osce.asked.redflags) sc.notes.push('Red flag screen skipped. Present in this patient: ' + s.redFlags.join(', '));
  } else sc.redflags = 20;

  const usefulExams = Object.keys(s.exam);
  const doneUseful = usefulExams.filter(k => osce.examDone[k]).length;
  const extra = Object.keys(osce.examDone).filter(k => usefulExams.indexOf(k) < 0).length;
  sc.exam = Math.max(0, Math.round(15 * (usefulExams.length ? doneUseful / usefulExams.length : 1)) - extra * 2);
  extra && sc.notes.push('Examinations requested with no findings in this patient: ' + extra);

  const usefulIx = s.investigations.map(i => i.key);
  const orderedUseful = osce.ixOrdered.filter(i => usefulIx.indexOf(i.key) >= 0).length;
  const unnecessary = osce.ixOrdered.filter(i => usefulIx.indexOf(i.key) < 0);
  sc.ix = Math.max(0, Math.round(15 * (usefulIx.length ? orderedUseful / usefulIx.length : 1)) - unnecessary.length * 2);
  unnecessary.forEach(i => sc.notes.push('Unnecessary investigation: ' + i.label));

  const rank = osce.ddx.indexOf(s.diagnosis);
  sc.ddx = rank === 0 ? 10 : (rank > 0 ? 6 : 0);
  if (rank < 0) sc.notes.push('Correct diagnosis was not in your differential.');

  sc.dx = osce.finalDx === s.diagnosis ? 10 : 0;
  if (!sc.dx) sc.notes.push('Final diagnosis missed. Expected answer: ' + s.diagnosis);

  const plan = (osce.plan || '') + ' ' + (osce.ddxNote || '');
  let hitCount = 0;
  s.management.forEach(m => {
    const words = m.toLowerCase().split(' ').filter(w => w.length > 4);
    const hit = words.some(w => plan.toLowerCase().indexOf(w) >= 0);
    if (hit) hitCount++; else sc.notes.push('Management not addressed: ' + m);
  });
  sc.mgmt = Math.round(10 * (s.management.length ? hitCount / s.management.length : 1));

  sc.total = Math.min(100, sc.history + sc.redflags + sc.exam + sc.ix + sc.ddx + sc.dx + sc.mgmt);
  sc.pass = sc.total >= 60;
  return sc;
}

function osceFinish() {
  if (!osce.finalDx) { alert('Choose a final diagnosis first.'); return; }
  const sc = osceScore();
  osce.scored = sc;
  const s = osce.st;
  const bar = (label, value, max) => '<div class="score-row"><span>' + label + '</span>' +
    '<div class="score-track"><div class="score-fill" style="width:' + Math.round(value / max * 100) + '%"></div></div>' +
    '<b>' + value + '/' + max + '</b></div>';
  let html = '<div class="osce-card"><h3>' + (sc.pass ? 'Pass' : 'Not yet a pass') + ': ' + sc.total + '/100</h3>' +
    bar('History coverage', sc.history, 25) + bar('Red flags', sc.redflags, 20) +
    bar('Examination', sc.exam, 15) + bar('Investigations', sc.ix, 15) +
    bar('Differential diagnosis', sc.ddx, 10) + bar('Final diagnosis', sc.dx, 10) +
    bar('Management safety', sc.mgmt, 10) +
    '<p class="osce-model"><b>Model answer:</b> ' + esc(s.diagnosis) + '. ' + esc(s.explanation) + '</p>' +
    '<p class="osce-model"><b>Safe management:</b> ' + esc(s.management.join('; ')) + '.</p>';
  html += '<h4>Examiner notes</h4><ul class="osce-notes">' +
    (sc.notes.length ? sc.notes.map(n => '<li>' + esc(n) + '</li>').join('') : '<li>Nothing missed. Clean station.</li>') +
    '</ul>';
  html += '<div class="osce-actions"><button class="btn-secondary" onclick="osceRetry()">Retry station</button>' +
    '<button class="btn-secondary" onclick="osceNewPatient()">New patient, same section</button>' +
    '<button class="btn-secondary" onclick="goHome()">Back to sections</button></div></div>';
  $('osce-panel').innerHTML = html;
  $('osce-chat').style.display = 'none';

  if (llmReady()) {
    const transcript = osce.transcript.map(m => m.who.toUpperCase() + ': ' + m.text).join('\n');
    const prompt = 'Case: ' + s.diagnosis + '. Transcript:\n' + transcript +
      '\nExaminations: ' + Object.keys(osce.examDone).join(', ') +
      '\nInvestigations ordered: ' + osce.ixOrdered.map(i => i.label).join(', ') +
      '\nDifferential submitted: ' + osce.ddx.join(' > ') +
      '\nFinal diagnosis: ' + osce.finalDx +
      '\nPlan: ' + osce.plan +
      '\nWrite the scorecard narrative.';
    llmCall(OSCE_SYSTEM_PROMPTS.examiner, prompt).then(txt => {
      if (txt) {
        const d = document.createElement('div');
        d.className = 'osce-llm';
        d.textContent = txt;
        $('osce-panel').appendChild(d);
      }
    });
  }
}

function osceRetry() { startOSCE(osce.region, osce.category, osce.level); }
function osceNewPatient() { startOSCE(osce.region, osce.category, osce.level); }

function renderOscePanel() {
  if (!osce) return;
  const s = osce.st;
  const step = osce.step;
  const steps = [['history', 'History'], ['exam', 'Examination'], ['ix', 'Investigations'], ['ddx', 'Differential'], ['plan', 'Diagnosis and plan']];
  let html = '<div class="osce-stepper">';
  steps.forEach((pair, i) => {
    const done = (pair[0] === 'history' && Object.keys(osce.asked).length) ||
      (pair[0] === 'exam' && Object.keys(osce.examDone).length) ||
      (pair[0] === 'ix' && osce.ixOrdered.length) ||
      (pair[0] === 'ddx' && osce.ddx.length) ||
      (pair[0] === 'plan' && osce.finalDx);
    html += '<button class="osce-step' + (step === pair[0] ? ' active' : '') + (done ? ' done' : '') +
      '" onclick="osceGo(\'' + pair[0] + '\')">' + (i + 1) + '. ' + pair[1] + '</button>';
  });
  html += '</div>';

  if (step === 'history') {
    html += '<div class="osce-hintrow">Ask by typing, or tap a prompt. The red flag screen is the step most students skip.</div>' +
      '<div class="osce-inputrow"><input id="osce-q" placeholder="Ask the patient a question" onkeydown="if(event.key===\'Enter\')osceAsk()">' +
      '<button class="osce-send" onclick="osceAsk()">Ask</button></div>' +
      '<div class="osce-chips">' + OSCE_INTENTS.slice(0, 9).map(i =>
        '<button class="osce-chip" onclick="osceQuick(\'' + i.key + '\')">' + i.label + '</button>').join('') +
      '<button class="osce-chip osce-chip-flag" onclick="osceQuick(\'redflags\')">Screen for red flags</button></div>';
  } else if (step === 'exam') {
    html += '<div class="osce-hintrow">Request only the examinations you would actually perform.</div><div class="osce-chips">' +
      EXAM_SYSTEMS.map(x => '<button class="osce-chip' + (osce.examDone[x.key] ? ' picked' : '') + '" onclick="osceExamine(\'' + x.key + '\')">' + x.label + '</button>').join('') + '</div>';
  } else if (step === 'ix') {
    html += '<div class="osce-hintrow">Every unnecessary test is named on the scorecard.</div><div class="osce-chips">' +
      IX_MENU.map(x => '<button class="osce-chip' + (osce.ixOrdered.some(i => i.key === x.key) ? ' picked' : '') + '" onclick="osceOrderIx(\'' + x.key + '\')">' + x.label + '</button>').join('') + '</div>';
  } else if (step === 'ddx') {
    html += '<div class="osce-hintrow">Pick up to three, most likely first.</div><div class="osce-chips">' +
      s.ddx.map(o => '<button class="osce-chip' + (osce.ddx.indexOf(o) >= 0 ? ' picked' : '') + '" onclick="osceToggleDdx(this.dataset.o,this)" data-o="' + esc(o) + '">' + esc(o) + '</button>').join('') +
      '</div><div class="osce-inputrow"><input placeholder="Reasoning (optional)" value="' + esc(osce.ddxNote) + '" oninput="osce.ddxNote=this.value"></div>';
  } else {
    html += '<div class="osce-hintrow">Commit to one diagnosis and a safe plan.</div>' +
      '<select class="osce-select" onchange="osce.finalDx=this.value">' +
      '<option value="">Choose your diagnosis</option>' +
      s.ddx.map(o => '<option' + (osce.finalDx === o ? ' selected' : '') + '>' + esc(o) + '</option>').join('') + '</select>' +
      '<textarea class="osce-plan" placeholder="Management plan: immediate steps, treatment, referral, safety net" oninput="osce.plan=this.value">' + esc(osce.plan) + '</textarea>' +
      '<button class="osce-finish" onclick="osceFinish()">Submit station</button>';
  }
  $('osce-panel').innerHTML = html;
}

function osceLeave() {
  osce = null;
  $('osce-screen').style.display = 'none';
  goHome();
}

// ---------- pre-clinical Socratic tutor ----------
function tutorHint() {
  if (!current || !current.active) return;
  const tpl = current.active;
  const exp = tpl.explanation || '';
  const first = exp.split(/(?<=[.!?])\s+/)[0] || '';
  const q1 = 'Before you answer, what in the patient file points to one structure or system rather than another?';
  const q2 = 'Which single finding here would be hardest to explain with a competing diagnosis?';
  const fb = $('feedback-box');
  fb.style.display = 'block';
  fb.className = 'feedback';
  fb.innerHTML = '<strong>Socratic prompt</strong><br><br>' + q1 + '<br><br>' + q2 +
    '<br><br><span style="color:#8c9ba5">Reveal the reasoning: ' + esc(first) + '</span>';
  if (llmReady()) {
    llmCall(OSCE_SYSTEM_PROMPTS.tutor, 'Case: ' + (tpl.mechanism || tpl.stem) + '. Findings: ' + (tpl.exam || '') +
      '. Ask one question.').then(txt => {
        if (txt) fb.innerHTML = '<strong>Socratic prompt</strong><br><br>' + esc(txt);
      });
  }
}
