// ============ YazMed app shell: language, theme, settings, flashcards ============

const I18N = {
  en: {
    'nav.home': 'Home', 'nav.videos': 'Video Tutorials', 'nav.pbl': 'Basic PBL',
    'nav.osce': 'OSCE Simulator', 'nav.quiz': 'Quizzes', 'nav.flash': 'Terminology',
    'nav.about': 'About', 'nav.contact': 'Contact Me', 'nav.settings': 'Settings',
    'landing.welcome': 'welcome to',
    'landing.title': 'YazMed',
    'landing.sub': 'Clinical PBL cases, an OSCE simulator, terminology flashcards, a quiz bank and video tutorials for the medical years, organised by system in one place.',
    'landing.videos': 'Video Tutorials', 'landing.pbl': 'Basic PBL Simulator',
    'landing.osce': 'OSCE Simulator', 'landing.quiz': 'Quiz Bank',
    'landing.flash': 'Terminology Flashcards',
    'pbl.welcome': 'Basic PBL simulator', 'pbl.title': 'Choose a System',
    'pbl.note': 'Progressive case triggers, mechanism before diagnosis, progress saved level by level, Socratic hints when you stall.',
    'osce.welcome': 'OSCE simulator', 'osce.title': 'Choose a Station',
    'osce.note': 'A virtual patient, focused examination, investigations, a differential and a plan. Every station ends with an examiner scorecard out of 100, pass mark 60.',
    'quiz.title': 'Quiz Bank',
    'quiz.note': 'MCQs by system, split into levels that unlock as you finish. The clinical half covers the subjects you meet on the wards.',
    'quiz.basic': 'Basic Sciences', 'quiz.clinical': 'Clinical',
    'video.title': 'Video Tutorials', 'video.basic': 'Basic Sciences', 'video.clinical': 'Clinical',
    'video.ar': 'Arabic lectures', 'video.en': 'English lectures', 'video.topics': 'Back to topics',
    'video.sections': 'sections', 'video.videos': 'videos',
    'flash.title': 'Terminology Flashcards',
    'flash.note': 'Medical language in two tracks: basic word building and clinical usage. Each track runs from first year to final year.',
    'flash.basic': 'Basic terminology', 'flash.clinical': 'Clinical terminology',
    'flash.level': 'Level', 'flash.cards': 'cards', 'flash.known': 'known',
    'flash.flip': 'Flip card', 'flash.next': 'Next', 'flash.prev': 'Previous',
    'flash.markKnown': 'Mark as known', 'flash.knownDone': 'Known', 'flash.shuffle': 'Shuffle',
    'flash.reset': 'Reset progress', 'flash.back': 'Back to levels',
    'flash.hintFront': 'Tap the card to reveal the definition',
    'flash.hintBack': 'Tap again to hide the definition',
    'flash.empty': 'No cards in this level yet.',
    'settings.title': 'Settings',
    'settings.note': 'Language, appearance and study tools. Everything is stored in this browser only.',
    'settings.language': 'Language', 'settings.langHint': 'Interface language. Case and question text stays in English.',
    'settings.theme': 'Appearance', 'settings.themeSystem': 'System', 'settings.themeLight': 'Light', 'settings.themeDark': 'Dark',
    'settings.themeHint': 'System follows your device setting. Light uses the warm paper background.',
    'settings.size': 'Text size', 'settings.sizeS': 'Small', 'settings.sizeM': 'Medium', 'settings.sizeL': 'Large',
    'settings.sizeHint': 'Applies to the whole site straight away.',
    'settings.ai': 'AI endpoint for the OSCE patient and examiner',
    'settings.aiHint': 'Optional. An OpenAI-compatible chat endpoint. Leave empty and the built-in responder runs everything offline.',
    'settings.endpoint': 'Endpoint', 'settings.key': 'API key', 'settings.model': 'Model',
    'settings.save': 'Save', 'settings.saved': 'Saved.',
    'settings.data': 'Your progress', 'settings.dataHint': 'Clears what this browser remembers about your study progress.',
    'settings.resetPbl': 'Reset PBL progress', 'settings.resetOsce': 'Reset OSCE stations',
    'settings.resetFlash': 'Reset flashcards', 'settings.resetAll': 'Reset everything',
    'settings.resetDone': 'Cleared.',
    'case.level': 'Level', 'case.answered': 'answered', 'case.correct': 'Correct', 'case.wrong': 'Wrong',
    'case.accuracy': 'Accuracy', 'case.overall': 'Overall', 'case.spotOn': 'Spot On.',
    'case.incorrect': 'Incorrect Answer.', 'case.next': 'Next Case', 'case.tutor': 'Ask the tutor for a hint',
    'case.objective': 'Learning objective: explain the mechanism behind this presentation and justify your chosen diagnosis over the alternatives.',
    'case.objectiveQ': 'Learning objective: apply the basic-science principle behind this question, not a memorised fact.',
    'case.patientFile': 'Patient file', 'case.question': 'Question',
    'case.levelComplete': 'Level Complete', 'case.sectionDone': 'Section Completed',
    'case.retryLevel': 'Retry Level', 'case.nextLevel': 'Next Level', 'case.backHome': 'Back to Home',
    'case.retrySection': 'Retry Section', 'case.totalAnswered': 'Total answered',
    'case.socratic': 'Socratic prompt', 'case.reasoning': 'Reveal the reasoning',
    'osce.station': 'OSCE station', 'osce.history': 'History', 'osce.exam': 'Examination',
    'osce.ix': 'Investigations', 'osce.ddx': 'Differential', 'osce.plan': 'Diagnosis and plan',
    'osce.ask': 'Ask', 'osce.submit': 'Submit station', 'osce.retry': 'Retry station',
    'osce.newPatient': 'New patient, same section', 'osce.backStations': 'Back to stations',
    'osce.aiSettings': 'AI settings', 'osce.pickDx': 'Choose your diagnosis',
    'osce.hintHistory': 'Ask by typing, or tap a prompt. The red flag screen is the step most students skip.',
    'osce.hintExam': 'Request only the examinations you would actually perform.',
    'osce.hintIx': 'Every unnecessary test is named on the scorecard.',
    'osce.hintDdx': 'Pick up to three, most likely first.',
    'osce.hintPlan': 'Commit to one diagnosis and a safe plan.',
    'osce.qPh': 'Ask the patient a question', 'osce.planPh': 'Management plan: immediate steps, treatment, referral, safety net',
    'osce.reasonPh': 'Reasoning (optional)', 'osce.model': 'Model answer', 'osce.safe': 'Safe management',
    'osce.notes': 'Examiner notes', 'osce.clean': 'Nothing missed. Clean station.',
    'osce.pass': 'Pass', 'osce.fail': 'Not yet a pass',
    'osce.historyCoverage': 'History coverage', 'osce.redflags': 'Red flags', 'osce.examination': 'Examination',
    'osce.investigations': 'Investigations', 'osce.ddxScore': 'Differential diagnosis',
    'osce.dxScore': 'Final diagnosis', 'osce.mgmtScore': 'Management safety',
    'osce.patientIntro': 'I was asked to come and talk to you about what has been going on.',
    'osce.note': 'Presentation note', 'osce.confused': 'I am not sure I follow, doctor. Could you ask that another way?',
    'osce.nothing': 'Nothing like that, doctor.', 'osce.nothingElse': 'Nothing else that I noticed.',
    'osce.cannotSay': 'I cannot really say, doctor.', 'osce.redflagAsk': 'Now that you ask: ',
    'footer.tagline': 'Medical learning platform',
    'footer.rights': 'Built by a medical student, for medical students.'
  },
  ar: {
    'nav.home': 'الرئيسية', 'nav.videos': 'مكتبة الفيديو', 'nav.pbl': 'حالات أساسية',
    'nav.osce': 'محاكي OSCE', 'nav.quiz': 'بنك الأسئلة', 'nav.flash': 'المصطلحات',
    'nav.about': 'عن المنصة', 'nav.contact': 'اتصل بي', 'nav.settings': 'الإعدادات',
    'landing.welcome': 'مرحباً بك في',
    'landing.title': 'YazMed',
    'landing.sub': 'حالات تعلم قائمة على المشكلات، ومحاكي امتحان سريري، وبطاقات مصطلحات، وبنك أسئلة، ومكتبة فيديو لسنوات الطب، مرتبة حسب الأجهزة في مكان واحد.',
    'landing.videos': 'مكتبة الفيديو', 'landing.pbl': 'محاكي الحالات الأساسية',
    'landing.osce': 'محاكي OSCE', 'landing.quiz': 'بنك الأسئلة',
    'landing.flash': 'بطاقات المصطلحات',
    'pbl.welcome': 'محاكي الحالات الأساسية', 'pbl.title': 'اختر جهازاً',
    'pbl.note': 'حالات متتابعة، الميكانيزم قبل التشخيص، تقدم محفوظ لكل مستوى، وتلميحات سقراطية عند التعثر.',
    'osce.welcome': 'محاكي OSCE', 'osce.title': 'اختر محطة',
    'osce.note': 'مريض افتراضي، فحص موجّه، فحوصات، تشخيص تفريقي وخطة. كل محطة تنتهي ببطاقة تقييم من مئة، والنجاح عند ستين.',
    'quiz.title': 'بنك الأسئلة',
    'quiz.note': 'أسئلة اختيار من متعدد حسب الجهاز، مقسمة إلى مستويات تُفتح بالتتابع. النصف السريري يغطي مواد العنقود السريري.',
    'quiz.basic': 'العلوم الأساسية', 'quiz.clinical': 'العلوم السريرية',
    'video.title': 'مكتبة الفيديو', 'video.basic': 'العلوم الأساسية', 'video.clinical': 'العلوم السريرية',
    'video.ar': 'محاضرات عربية', 'video.en': 'محاضرات إنجليزية', 'video.topics': 'رجوع إلى الموضوعات',
    'video.sections': 'أقسام', 'video.videos': 'فيديو',
    'flash.title': 'بطاقات المصطلحات',
    'flash.note': 'لغة الطب في مسارين: بناء المصطلح الأساسي والاستخدام السريري. كل مسار من السنة الأولى إلى السنة النهائية.',
    'flash.basic': 'المصطلحات الأساسية', 'flash.clinical': 'المصطلحات السريرية',
    'flash.level': 'المستوى', 'flash.cards': 'بطاقة', 'flash.known': 'محفوظة',
    'flash.flip': 'اقلب البطاقة', 'flash.next': 'التالي', 'flash.prev': 'السابق',
    'flash.markKnown': 'حفظتها', 'flash.knownDone': 'محفوظة', 'flash.shuffle': 'خلط',
    'flash.reset': 'تصفير التقدم', 'flash.back': 'رجوع إلى المستويات',
    'flash.hintFront': 'اضغط البطاقة لإظهار التعريف',
    'flash.hintBack': 'اضغط مرة أخرى لإخفاء التعريف',
    'flash.empty': 'لا توجد بطاقات في هذا المستوى بعد.',
    'settings.title': 'الإعدادات',
    'settings.note': 'اللغة والمظهر وأدوات الدراسة. كل شيء يُحفظ في هذا المتصفح فقط.',
    'settings.language': 'اللغة', 'settings.langHint': 'لغة الواجهة. نصوص الحالات والأسئلة تبقى بالإنجليزية.',
    'settings.theme': 'المظهر', 'settings.themeSystem': 'النظام', 'settings.themeLight': 'فاتح', 'settings.themeDark': 'داكن',
    'settings.themeHint': 'خيار النظام يتبع إعداد جهازك. الفاتح يستخدم خلفية ورقية دافئة.',
    'settings.size': 'حجم الخط', 'settings.sizeS': 'صغير', 'settings.sizeM': 'متوسط', 'settings.sizeL': 'كبير',
    'settings.sizeHint': 'يُطبق على الموقع كله فوراً.',
    'settings.ai': 'واجهة الذكاء الاصطناعي للمريض والممتحن',
    'settings.aiHint': 'اختياري. أي واجهة متوافقة مع OpenAI. إذا تُركت فارغة يعمل الرد المدمج دون إنترنت.',
    'settings.endpoint': 'الرابط', 'settings.key': 'المفتاح', 'settings.model': 'الموديل',
    'settings.save': 'حفظ', 'settings.saved': 'تم الحفظ.',
    'settings.data': 'تقدمك', 'settings.dataHint': 'يمسح ما يحفظه هذا المتصفح عن تقدمك الدراسي.',
    'settings.resetPbl': 'تصفير الحالات', 'settings.resetOsce': 'تصفير محطات OSCE',
    'settings.resetFlash': 'تصفير البطاقات', 'settings.resetAll': 'تصفير الكل',
    'settings.resetDone': 'تم المسح.',
    'case.level': 'المستوى', 'case.answered': 'تمت الإجابة', 'case.correct': 'صحيح', 'case.wrong': 'خطأ',
    'case.accuracy': 'الدقة', 'case.overall': 'الإجمالي', 'case.spotOn': 'إجابة صحيحة.',
    'case.incorrect': 'إجابة خاطئة.', 'case.next': 'الحالة التالية', 'case.tutor': 'اطلب تلميحاً من المدرّس',
    'case.objective': 'هدف التعلم: اشرح الميكانيزم وراء هذا العرض وبرّر تشخيصك مقابل البدائل.',
    'case.objectiveQ': 'هدف التعلم: طبّق المبدأ العلمي وراء هذا السؤال لا مجرد حفظ المعلومة.',
    'case.patientFile': 'ملف المريض', 'case.question': 'سؤال',
    'case.levelComplete': 'اكتمل المستوى', 'case.sectionDone': 'اكتمل القسم',
    'case.retryLevel': 'إعادة المستوى', 'case.nextLevel': 'المستوى التالي', 'case.backHome': 'رجوع للرئيسية',
    'case.retrySection': 'إعادة القسم', 'case.totalAnswered': 'إجمالي الإجابات',
    'case.socratic': 'سؤال سقراطي', 'case.reasoning': 'اكشف الاستدلال',
    'osce.station': 'محطة OSCE', 'osce.history': 'القصة المرضية', 'osce.exam': 'الفحص',
    'osce.ix': 'الفحوصات', 'osce.ddx': 'التشخيص التفريقي', 'osce.plan': 'التشخيص والخطة',
    'osce.ask': 'اسأل', 'osce.submit': 'إنهاء المحطة', 'osce.retry': 'إعادة المحطة',
    'osce.newPatient': 'مريض جديد، نفس القسم', 'osce.backStations': 'رجوع إلى المحطات',
    'osce.aiSettings': 'إعدادات الذكاء', 'osce.pickDx': 'اختر تشخيصك',
    'osce.hintHistory': 'اسأل بالكتابة أو اختر سؤالاً جاهزاً. فحص العلامات الخطرة هو الخطوة التي ينساها معظم الطلاب.',
    'osce.hintExam': 'اطلب فقط الفحوصات التي ستجريها فعلاً.',
    'osce.hintIx': 'كل فحص غير ضروري يُذكر في التقييم.',
    'osce.hintDdx': 'اختر حتى ثلاثة، الأرجح أولاً.',
    'osce.hintPlan': 'التزم بتشخيص واحد وخطة آمنة.',
    'osce.qPh': 'اسأل المريض سؤالاً', 'osce.planPh': 'خطة العلاج: الخطوات الفورية، العلاج، الإحالة، وشبكة الأمان',
    'osce.reasonPh': 'الاستدلال (اختياري)', 'osce.model': 'الإجابة النموذجية', 'osce.safe': 'التدبير الآمن',
    'osce.notes': 'ملاحظات الممتحن', 'osce.clean': 'لا شيء فاتك. محطة نظيفة.',
    'osce.pass': 'ناجح', 'osce.fail': 'لم تصل إلى النجاح بعد',
    'osce.historyCoverage': 'تغطية القصة', 'osce.redflags': 'العلامات الخطرة', 'osce.examination': 'الفحص',
    'osce.investigations': 'الفحوصات', 'osce.ddxScore': 'التشخيص التفريقي',
    'osce.dxScore': 'التشخيص النهائي', 'osce.mgmtScore': 'سلامة التدبير',
    'osce.patientIntro': 'طُلب مني أن آتي وأتحدث معك عمّا يجري.',
    'osce.note': 'ملاحظة العرض', 'osce.confused': 'لم أفهم تماماً يا دكتور، هل يمكنك صياغة السؤال بطريقة أخرى؟',
    'osce.nothing': 'لا شيء من هذا يا دكتور.', 'osce.nothingElse': 'لا شيء آخر لاحظته.',
    'osce.cannotSay': 'لا أستطيع الجزم يا دكتور.', 'osce.redflagAsk': 'بما أنك سألت: ',
    'footer.tagline': 'منصة التعلم الطبي',
    'footer.rights': 'بناها طالب طب لطلاب الطب.'
  }
};

const AR_REGIONS = {
  msk: 'الجهاز العضلي الهيكلي', embryology: 'التطور وعلم الأجنة',
  pathology: 'علم الأمراض العام', physiology: 'علم وظائف الأعضاء', quiz: 'بنك الأسئلة'
};
const AR_CATS = {
  'msk/nerves': 'إصابات الأعصاب', 'msk/muscles': 'إصابات العضلات', 'msk/bones': 'إصابات العظام', 'msk/general': 'إصابات عامة',
  'embryology/level1': 'المستوى الأول: الأساسيات والأسابيع', 'embryology/level2': 'المستوى الثاني: تكوّن الأعضاء',
  'embryology/level3': 'المستوى الثالث: العيوب البنيوية', 'embryology/level4': 'المستوى الرابع: الأمراض المتقدمة',
  'pathology/general': 'علم الأمراض العام',
  'physiology/cell': 'الخلية والغشاء', 'physiology/nerve_muscle': 'العصب والعضلة', 'physiology/blood': 'الدم وسوائل الجسم',
  'physiology/immune': 'المناعة', 'physiology/cardio': 'القلب والأوعية', 'physiology/resp': 'الجهاز التنفسي',
  'physiology/renal': 'الكلى والحمض القاعدي', 'physiology/git': 'الجهاز الهضمي', 'physiology/endocrine': 'الغدد الصماء',
  'physiology/repro': 'التكاثر',
  'quiz/msk': 'العضلي الهيكلي', 'quiz/neuro': 'الجهاز العصبي', 'quiz/cardio': 'القلب', 'quiz/resp': 'التنفسي',
  'quiz/renal': 'الكلى والمسالك', 'quiz/git': 'الهضمي والكبد', 'quiz/endocrine': 'الغدد الصماء', 'quiz/repro': 'التكاثر',
  'quiz/blood_immune': 'الدم والمناعة', 'quiz/development': 'التطور والأنسجة',
  'quiz/medicine': 'الباطنة', 'quiz/surgery': 'الجراحة', 'quiz/pediatrics': 'الأطفال',
  'quiz/obgyn': 'النساء والولادة', 'quiz/psychiatry': 'النفسية'
};

let LANG = 'en';
function t(key) {
  const dict = I18N[LANG] || I18N.en;
  return dict[key] || I18N.en[key] || key;
}

function applyLang(lang) {
  LANG = (lang === 'ar') ? 'ar' : 'en';
  document.documentElement.lang = LANG;
  document.documentElement.dir = LANG === 'ar' ? 'rtl' : 'ltr';
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.getAttribute('data-i18n'));
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    el.setAttribute('placeholder', t(el.getAttribute('data-i18n-ph')));
  });
  try { localStorage.setItem('medplat-lang', LANG); } catch (e) {}
  if (typeof refreshAll === 'function') refreshAll();
}

// ---------- theme and text size ----------
function applyTheme(theme) {
  const root = document.documentElement;
  if (theme === 'light' || theme === 'dark') root.setAttribute('data-theme', theme);
  else root.removeAttribute('data-theme');
  try { localStorage.setItem('medplat-theme', theme || 'system'); } catch (e) {}
  const sysLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
  const effective = (theme === 'light' || theme === 'dark') ? theme : (sysLight ? 'light' : 'dark');
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute('content', effective === 'light' ? '#F5F5DC' : '#0C161E');
}
function applySize(size) {
  if (size === 's' || size === 'l') document.documentElement.setAttribute('data-size', size);
  else document.documentElement.removeAttribute('data-size');
  try { localStorage.setItem('medplat-size', size || 'm'); } catch (e) {}
}

// ---------- settings view ----------
function renderSettings() {
  const box = $('settings-body');
  if (!box) return;
  const s = llmSettings();
  const theme = localStorage.getItem('medplat-theme') || 'system';
  const size = localStorage.getItem('medplat-size') || 'm';
  const seg = (id, options, active) => '<div class="seg" id="' + id + '">' + options.map(o =>
    '<button class="' + (o[0] === active ? 'active' : '') + '" onclick="' + o[2] + '">' + o[1] + '</button>').join('') + '</div>';
  box.innerHTML =
    '<div class="setting-row"><div class="setting-label">' + t('settings.language') + '</div>' +
      seg('seg-lang', [['en', 'English', "setLang('en')"], ['ar', 'العربية', "setLang('ar')"]], LANG) +
      '<p class="setting-hint">' + t('settings.langHint') + '</p></div>' +
    '<div class="setting-row"><div class="setting-label">' + t('settings.theme') + '</div>' +
      seg('seg-theme', [['system', t('settings.themeSystem'), "setTheme('system')"], ['light', t('settings.themeLight'), "setTheme('light')"], ['dark', t('settings.themeDark'), "setTheme('dark')"]], theme) +
      '<p class="setting-hint">' + t('settings.themeHint') + '</p></div>' +
    '<div class="setting-row"><div class="setting-label">' + t('settings.size') + '</div>' +
      seg('seg-size', [['s', t('settings.sizeS'), "setSize('s')"], ['m', t('settings.sizeM'), "setSize('m')"], ['l', t('settings.sizeL'), "setSize('l')"]], size) +
      '<p class="setting-hint">' + t('settings.sizeHint') + '</p></div>' +
    '<div class="setting-row"><div class="setting-label">' + t('settings.ai') + '</div>' +
      '<p class="setting-hint">' + t('settings.aiHint') + '</p>' +
      '<div class="full"><input type="text" id="ai-endpoint" placeholder="' + t('settings.endpoint') + '" value="' + esc(s.endpoint || '') + '"></div>' +
      '<div class="full"><input type="password" id="ai-key" placeholder="' + t('settings.key') + '" value="' + esc(s.key || '') + '"></div>' +
      '<div class="full"><input type="text" id="ai-model" placeholder="' + t('settings.model') + '" value="' + esc(s.model || 'gpt-4o-mini') + '"></div>' +
      '<div class="full"><button class="flash-btn primary" onclick="saveAi()">' + t('settings.save') + '</button> <span id="ai-status" class="setting-hint"></span></div></div>' +
    '<div class="setting-row"><div class="setting-label">' + t('settings.data') + '</div>' +
      '<p class="setting-hint">' + t('settings.dataHint') + '</p>' +
      '<div class="full"><button class="danger-btn" onclick="resetStore(SAVE_KEY)">' + t('settings.resetPbl') + '</button> ' +
      '<button class="danger-btn" onclick="resetStore(OSCE_KEY)">' + t('settings.resetOsce') + '</button> ' +
      '<button class="danger-btn" onclick="resetStore(FLASH_KEY)">' + t('settings.resetFlash') + '</button> ' +
      '<button class="danger-btn" onclick="resetStore(\'*\')">' + t('settings.resetAll') + '</button></div></div>';
}

function setLang(l) { applyLang(l); }
function setTheme(v) { applyTheme(v); renderSettings(); }
function setSize(v) { applySize(v); renderSettings(); }
function saveAi() {
  saveLlmSettings({
    endpoint: ($('ai-endpoint') || {}).value || '',
    key: ($('ai-key') || {}).value || '',
    model: ($('ai-model') || {}).value || 'gpt-4o-mini'
  });
  const st = $('ai-status');
  if (st) st.textContent = t('settings.saved');
}
function resetStore(key) {
  try {
    if (key === '*') {
      localStorage.removeItem(SAVE_KEY);
      localStorage.removeItem(OSCE_KEY);
      localStorage.removeItem(FLASH_KEY);
    } else {
      localStorage.removeItem(key);
    }
    SAVE = loadSave();
    flashState = { track: 'basic', level: null, idx: 0, flipped: false, known: {} };
    renderSettings();
    updateHomeStatuses();
    const st = $('ai-status');
    if (st) st.textContent = t('settings.resetDone');
  } catch (e) {}
}

// ---------- flashcards ----------
const FLASH_KEY = 'medplat-flash-v1';
let flashState = { track: 'basic', level: null, idx: 0, flipped: false, known: {} };

function flashStore() {
  try { return JSON.parse(localStorage.getItem(FLASH_KEY) || '{}'); } catch (e) { return {}; }
}
function flashSave(store) {
  try { localStorage.setItem(FLASH_KEY, JSON.stringify(store)); } catch (e) {}
}
function flashKnownSet() {
  const store = flashStore();
  const k = flashState.track + '/' + flashState.level;
  return new Set(store[k] || []);
}
function flashMarkKnown() {
  if (!flashState.level) return;
  const store = flashStore();
  const k = flashState.track + '/' + flashState.level;
  const set = new Set(store[k] || []);
  if (set.has(flashState.idx)) set.delete(flashState.idx); else set.add(flashState.idx);
  store[k] = Array.from(set);
  flashSave(store);
  renderFlash();
}
function setFlashTrack(track, btn) {
  flashState = { track: track, level: null, idx: 0, flipped: false, known: {} };
  document.querySelectorAll('#view-flash .track-tab').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderFlash();
}
function openFlashLevel(level) {
  flashState.level = level;
  flashState.idx = 0;
  flashState.flipped = false;
  renderFlash();
}
function flashBack() {
  flashState.level = null;
  renderFlash();
}
function flashFlip() { flashState.flipped = !flashState.flipped; renderFlash(); }
function flashNext(delta) {
  const set = FLASH[flashState.track][flashState.level];
  if (!set) return;
  const n = set.cards.length;
  flashState.idx = (flashState.idx + delta + n) % n;
  flashState.flipped = false;
  renderFlash();
}
function flashShuffle() {
  const set = FLASH[flashState.track][flashState.level];
  if (!set) return;
  for (let i = set.cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = set.cards[i]; set.cards[i] = set.cards[j]; set.cards[j] = tmp;
  }
  flashState.idx = 0;
  flashState.flipped = false;
  renderFlash();
}
function flashResetLevel() {
  const store = flashStore();
  delete store[flashState.track + '/' + flashState.level];
  flashSave(store);
  renderFlash();
}

function renderFlash() {
  const root = $('flash-root');
  if (!root) return;
  const track = FLASH[flashState.track];
  if (!track) { root.innerHTML = '<p class="vid-note">' + t('flash.empty') + '</p>'; return; }
  if (!flashState.level) {
    const store = flashStore();
    let html = '<div class="flash-grid">';
    Object.keys(track).forEach(level => {
      const set = track[level];
      const known = (store[flashState.track + '/' + level] || []).length;
      html += '<button class="flash-level" onclick="openFlashLevel(\'' + level + '\')">' +
        t('flash.level') + ' ' + level.replace('level', '') + ' · ' + esc(set.name) +
        '<span class="flash-count">' + set.cards.length + ' ' + t('flash.cards') + ' · ' + known + ' ' + t('flash.known') + '</span></button>';
    });
    root.innerHTML = html + '</div>';
    return;
  }
  const set = track[flashState.level];
  if (!set || !set.cards.length) { root.innerHTML = '<p class="vid-note">' + t('flash.empty') + '</p>'; return; }
  const cards = set.cards;
  const card = cards[flashState.idx] || cards[0];
  const known = flashKnownSet();
  const isKnown = known.has(flashState.idx);
  const pct = Math.round((known.size / cards.length) * 100);
  root.innerHTML =
    '<div class="flash-card-wrap">' +
      '<div class="flash-progress"><div class="flash-meta"><span>' + esc(set.name) + '</span>' +
        '<span>' + (flashState.idx + 1) + ' / ' + cards.length + ' · ' + known.size + ' ' + t('flash.known') + '</span></div>' +
        '<div class="progress-track"><div class="progress-fill" style="width:' + pct + '%"></div></div></div>' +
      '<div class="flash-card" onclick="flashFlip()">' +
        '<div class="flash-term">' + esc(card.term) + '</div>' +
        (LANG === 'ar' && card.ar ? '<div class="flash-ar">' + esc(card.ar) + '</div>' : '') +
        (flashState.flipped
          ? '<div class="flash-def">' + esc(card.definition) + '</div>'
          : '<div class="flash-hint">' + t('flash.hintFront') + '</div>') +
      '</div>' +
      '<div class="flash-toolbar">' +
        '<button class="flash-btn" onclick="flashNext(-1)">' + t('flash.prev') + '</button>' +
        '<button class="flash-btn primary" onclick="flashFlip()">' + t('flash.flip') + '</button>' +
        '<button class="flash-btn ' + (isKnown ? 'known' : '') + '" onclick="flashMarkKnown()">' +
          (isKnown ? t('flash.knownDone') : t('flash.markKnown')) + '</button>' +
        '<button class="flash-btn" onclick="flashNext(1)">' + t('flash.next') + '</button>' +
        '<button class="flash-btn" onclick="flashShuffle()">' + t('flash.shuffle') + '</button>' +
        '<button class="flash-btn" onclick="flashResetLevel()">' + t('flash.reset') + '</button>' +
        '<button class="flash-btn" onclick="flashBack()">' + t('flash.back') + '</button>' +
      '</div>' +
    '</div>';
}

// ---------- misc ----------
function refreshAll() {
  if (typeof updateHomeStatuses === 'function') updateHomeStatuses();
  if (typeof renderQuizGrid === 'function' && currentView === 'quiz') renderQuizGrid();
  if (typeof renderOsceHome === 'function' && currentView === 'osce') renderOsceHome();
  if (typeof renderVideos === 'function' && currentView === 'videos') renderVideos();
  if (typeof renderFlash === 'function' && currentView === 'flash') renderFlash();
  if (typeof renderSettings === 'function' && currentView === 'settings') renderSettings();
  if (typeof renderHeader === 'function' && currentView === 'sim' && current) renderHeader();
}
