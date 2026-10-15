// Medicare Tunis: relecture des publications
// Lit et écrit l'onglet "Carrousels" du Google Sheet.
// Colonnes: A N°, B Idée, C Service, D à H Slides 1 à 5, I Instagram, J Facebook, K TikTok,
// L Photo, M à Q Images 1 à 5, R Statut, S Prête, T Publication IG/FB, U Publication TikTok,
// V ID Buffer, W Commentaire de la relectrice.

var SPREADSHEET_ID = '1u8JFdxYABPWXKk75KIXKauFp1uHbcfzCrUeq2rzjYzk';
var SHEET_NAME = 'Carrousels';
var NB_COLS = 23;

function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Relecture Medicare Tunis')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function sheet_() {
  return SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_NAME);
}

function imageUrl_(value) {
  var v = String(value || '').trim();
  if (!v) return '';
  var isDrive = v.indexOf('drive.google.com') >= 0 || v.indexOf('googleusercontent.com') >= 0;
  if (/^https?:\/\//.test(v) && !isDrive) return v;
  var m = v.match(/[-\w]{25,}/);
  return m ? 'https://lh3.googleusercontent.com/d/' + m[0] + '=w1080' : '';
}

function getPosts() {
  var sh = sheet_();
  var last = sh.getLastRow();
  if (last < 2) return [];
  var rows = sh.getRange(2, 1, last - 1, NB_COLS).getValues();
  var posts = [];
  rows.forEach(function (r, i) {
    var status = String(r[17] || '').trim();
    if (!r[1] || !status || status === 'Brouillon') return;
    var slides = [];
    for (var k = 0; k < 5; k++) {
      slides.push({ text: String(r[3 + k] || ''), image: imageUrl_(r[12 + k]) });
    }
    posts.push({
      row: i + 2,
      n: String(r[0]),
      idea: String(r[1]),
      service: String(r[2] || ''),
      slides: slides,
      captions: { instagram: String(r[8] || ''), facebook: String(r[9] || ''), tiktok: String(r[10] || '') },
      status: status,
      comment: String(r[22] || ''),
      scheduledIg: String(r[19] || ''),
      scheduledTt: String(r[20] || ''),
      example: /^EXEMPLE/i.test(String(r[1]))
    });
  });
  return posts;
}

// action: 'approve', 'changes' ou 'reset'
function decide(row, n, action, comment) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = sheet_();
    row = Number(row);
    if (row < 2 || row > sh.getLastRow()) throw new Error('Publication introuvable. Actualise la page.');
    var r = sh.getRange(row, 1, 1, NB_COLS).getValues()[0];
    if (String(r[0]) !== String(n)) throw new Error('La feuille a changé. Actualise la page.');
    if (String(r[17]) === 'Programmée') throw new Error('Cette publication est déjà programmée.');
    comment = String(comment || '').trim();
    if (action === 'approve') {
      sh.getRange(row, 18).setValue('Prête');
      sh.getRange(row, 19).setValue(true);
      if (comment) sh.getRange(row, 23).setValue(comment);
    } else if (action === 'changes') {
      if (!comment) throw new Error('Écris un commentaire pour dire ce qu\'il faut changer.');
      sh.getRange(row, 18).setValue('À modifier');
      sh.getRange(row, 19).setValue(false);
      sh.getRange(row, 23).setValue(comment);
    } else if (action === 'reset') {
      sh.getRange(row, 18).setValue('À relire');
      sh.getRange(row, 19).setValue(false);
    } else {
      throw new Error('Action inconnue.');
    }
    SpreadsheetApp.flush();
    return getPosts();
  } finally {
    lock.releaseLock();
  }
}

// ---------- Idées à valider (onglet "À valider") ----------
// Colonnes: A N°, B Idée, C Service, D Source, E Date, F Décision, G Commentaire, H Statut, I Potentiel social, J Rang.
var IDEAS_SHEET = 'À valider';

function ideasSheet_() {
  return SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(IDEAS_SHEET);
}

function getIdeas() {
  var sh = ideasSheet_();
  var last = sh.getLastRow();
  if (last < 2) return [];
  var rows = sh.getRange(2, 1, last - 1, 10).getValues();
  var out = [];
  rows.forEach(function (r, i) {
    var statut = String(r[7] || '').trim();
    if (!r[1] || statut !== 'En attente') return;
    out.push({
      row: i + 2,
      n: String(r[0]),
      idea: String(r[1]),
      service: String(r[2] || ''),
      source: String(r[3] || ''),
      potential: String(r[8] || ''),
      rank: Number(r[9]) || 0,
      decision: String(r[5] || '').trim()
    });
  });
  return out;
}

// action: 'approve', 'reject' ou 'reset'
function decideIdea(row, n, action) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = ideasSheet_();
    row = Number(row);
    if (row < 2 || row > sh.getLastRow()) throw new Error('Idée introuvable. Actualise la page.');
    var r = sh.getRange(row, 1, 1, 10).getValues()[0];
    if (String(r[0]) !== String(n)) throw new Error('La feuille a changé. Actualise la page.');
    if (String(r[7]) !== 'En attente') throw new Error('Un carrousel existe déjà pour cette idée.');
    if (action === 'approve') sh.getRange(row, 6).setValue('Approuvée');
    else if (action === 'reject') sh.getRange(row, 6).setValue('Rejetée');
    else if (action === 'reset') sh.getRange(row, 6).setValue('');
    else throw new Error('Action inconnue.');
    SpreadsheetApp.flush();
    return getIdeas();
  } finally {
    lock.releaseLock();
  }
}
