// ============================================================
//  Z.G Digital · לידים מהאתר
//  Google Apps Script: מקבל את הטופס מהאתר, רושם שורה בגיליון,
//  שולח מייל, ושולח הודעת וואטסאפ (אופציונלי, דרך CallMeBot).
//  פריסה: script.google.com → פרויקט חדש → להדביק → Deploy → New deployment
//          Type: Web app · Execute as: Me · Who has access: Anyone
//          את כתובת ה־Web app מדביקים באתר ב־LEAD_ENDPOINT.
// ============================================================

const SHEET_ID   = '1LwL2J1mTufBbgyrWij9ezHqs4G_QuYN8T4iBi8V9wEI'; // הגיליון "לידים מהאתר · זיגזג מדיה"
const SHEET_TAB  = 'לידים';
const MAIL_TO    = 'guy@zigzagmedia.co.il';
const MAIL_SUBJ  = 'ליד חדש מהאתר';

// וואטסאפ דרך CallMeBot (חינם): שולחים פעם אחת מהטלפון שלך את ההודעה
// "I allow callmebot to send me messages" למספר +34 644 71 83 05 (בוואטסאפ),
// מקבלים בחזרה apikey, ומדביקים כאן. להשאיר ריק = בלי וואטסאפ.
const WA_PHONE   = '972525649801';
const WA_APIKEY  = '';

function doGet() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true, service: 'zg-leads' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    const raw = (e && e.postData && e.postData.contents) || '';
    let d = {};
    try { d = JSON.parse(raw); } catch (_) { d = (e && e.parameter) || {}; }

    // מלכודת לבוטים: שדה "website" מוסתר באתר; אם מולא, מתעלמים בשקט
    if (d.website) return out({ ok: true });

    const name  = clean(d.name, 120);
    const phone = clean(d.phone, 40);
    const biz   = clean(d.biz, 1000);
    const page  = clean(d.page, 300) || 'https://zigzagmedia.co.il/';
    if (!name || !phone) return out({ ok: false, error: 'missing' });

    const now = new Date();
    const when = Utilities.formatDate(now, 'Asia/Jerusalem', 'dd/MM/yyyy HH:mm');
    const id = Utilities.formatDate(now, 'Asia/Jerusalem', 'yyyyMMdd-HHmmss');

    // 1) שורה בגיליון
    const sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_TAB);
    sh.appendRow([when, name, "'" + phone, biz, page, 'חדש', '', id]);

    // 2) מייל
    const sheetUrl = 'https://docs.google.com/spreadsheets/d/' + SHEET_ID;
    const body = [
      'ליד חדש מהאתר',
      '',
      'שם: ' + name,
      'טלפון: ' + phone,
      'העסק והמטרה: ' + (biz || '—'),
      'עמוד: ' + page,
      'זמן: ' + when,
      '',
      'וואטסאפ ללקוח: https://wa.me/' + toIntl(phone),
      'הגיליון: ' + sheetUrl
    ].join('\n');
    MailApp.sendEmail({ to: MAIL_TO, subject: MAIL_SUBJ + ': ' + name, body: body, name: 'אתר זיגזג מדיה' });

    // 3) וואטסאפ אליך (אם הוגדר מפתח)
    if (WA_APIKEY) {
      const msg = 'ליד חדש מהאתר\n' + name + ' · ' + phone + '\n' + (biz || '') + '\nhttps://wa.me/' + toIntl(phone);
      const url = 'https://api.callmebot.com/whatsapp.php?phone=' + WA_PHONE + '&apikey=' + WA_APIKEY + '&text=' + encodeURIComponent(msg);
      try { UrlFetchApp.fetch(url, { muteHttpExceptions: true }); } catch (_) {}
    }

    return out({ ok: true, id: id });
  } catch (err) {
    return out({ ok: false, error: String(err) });
  }
}

function clean(v, max) { return String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, max); }
function toIntl(p) { let d = String(p).replace(/\D/g, ''); if (d.startsWith('0')) d = '972' + d.slice(1); return d; }
function out(obj) { return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON); }
