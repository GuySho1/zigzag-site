# Sub-pages of the calm site, built from the same head / nav / footer as index.html:
#   knowledge.html + articles/*.html   (the three articles from the old site)
#   accessibility.html                 (הצהרת נגישות)
#   404.html
import re, os, json, html as H
os.chdir('/home/claude/site/calm')
base = open('index.html', encoding='utf-8').read()
head = re.search(r'<head>.*?</head>', base, re.S).group(0)
nav = re.search(r'<a class="skip".*?</nav>', base, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', base, re.S).group(0)

def rel(s, depth):
    pre = '../' * depth
    s = s.replace('href="#main"', 'href="#MAIN"').replace('href="#top"', f'href="{pre}index.html"')
    s = re.sub(r'href="#([a-z\-]+)"', lambda m: f'href="{pre}index.html#{m.group(1)}"', s)
    s = s.replace('href="#MAIN"', 'href="#main"')
    for f in ('agents.html', 'knowledge.html', 'accessibility.html', 'llms.txt', 'apple-touch-icon.png', 'favicon.svg', 'favicon-32.png', 'og.jpg'):
        s = s.replace(f'href="{f}"', f'href="{pre}{f}"')
    s = s.replace('src="art/', f'src="{pre}art/').replace('href="art/', f'href="{pre}art/').replace('content="og.jpg', f'content="{pre}og.jpg')
    return s

EXTRA_CSS = '''<style>
.page{padding:112px 0 72px}
.narrow{max-width:72ch;margin-inline:auto}
.post h1{font-size:clamp(32px,4.6vw,58px);line-height:1.08;margin:10px 0 10px}
.post .meta{color:var(--dim);font-size:15px;margin:0 0 28px}
.post p{font-size:18px;line-height:1.8;margin:0 0 18px}
.post h2{font-size:clamp(24px,2.6vw,34px);margin:34px 0 10px}
.list{display:grid;gap:18px;margin-top:28px}
.item{display:block;background:var(--bg2);border:3px solid var(--line);padding:22px 24px;text-decoration:none;color:inherit;position:relative}
.item::before{content:'';position:absolute;top:0;right:0;width:46px;height:5px;background:var(--moon)}
.item h2{font-size:clamp(22px,2.4vw,30px);margin:6px 0 8px}
.item p{margin:0;color:var(--dim);font-size:16px}
.item .eyebrow{margin-bottom:4px;color:var(--bg)}
.more{margin-top:48px;border-top:3px solid var(--line);padding-top:24px}
.more h2{font-size:22px;margin-bottom:14px}
.more ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.more a{display:inline-flex;align-items:center;min-height:44px;font-weight:700;text-decoration:none;color:var(--moon)}
.cta{margin-top:40px;display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.acc h2{font-size:22px;margin:30px 0 8px}
.acc ul{padding-inline-start:22px}.acc li{margin:6px 0}
.lost{min-height:70svh;display:grid;align-items:center}
.lost .grid{align-items:center}
</style>
<script>document.addEventListener('DOMContentLoaded',()=>{const nav=document.querySelector('.nav');let last=scrollY;addEventListener('scroll',()=>{const y=scrollY;if(!matchMedia('(max-width:899px)').matches){nav.classList.remove('away');last=y;return;}if(y>last+8&&y>140)nav.classList.add('away');else if(y<last-8||y<80)nav.classList.remove('away');last=y;},{passive:true});});</script>
'''

def page(path, title, desc, body, depth=0, extra_head='', canonical=None):
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{H.escape(title)}</title>', h, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{H.escape(desc, quote=True)}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{H.escape(title, quote=True)}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{H.escape(desc, quote=True)}">', h)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://zigzagmedia.co.il/{canonical or path}">', h)
    h = h.replace('</head>', EXTRA_CSS + extra_head + '</head>')
    out = f'<!doctype html>\n<html lang="he" dir="rtl">\n{rel(h, depth)}\n<body>\n{rel(nav, depth)}\n<main id="main">\n{body}\n</main>\n{rel(footer, depth)}\n</body></html>'
    if path == '404.html':
        out = re.sub(r'(href|src|content)="(?!https?:|/|#|mailto:|tel:|data:)([^"]+)"', r'\1="/\2"', out)
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf-8').write(out)
    print('written', path, len(out))

# ---------------- the articles ----------------
ARTICLES = [
 dict(slug='infrastructure-before-everything', cat='תשתית ודאטה', date='פברואר 2026', iso='2026-02-01',
  title='תשתית לפני הכול: למה Business Manager מסודר שווה יותר מקמפיין מושקע',
  desc='לפני שמוציאים שקל על פרסום: פיקסל, אירועי המרה, Conversions API, גוגל אנליטיקס 4 ותג מנג\'ר. תשתית חזקה = נתונים אמיתיים = החלטות נכונות.',
  body=[
   'רוב העסקים מגיעים אלינו עם חשבון פרסום שנפתח לפני שנים ולא מחובר לכלום. פיקסל שמדלג על אירועים קריטיים. קהלים מותאמים אישית שנבנו בטעות על תנועה לא רלוונטית. דאטה שאי אפשר לסמוך עליה, ואז תוהים למה הקמפיינים לא מביאים תוצאות.',
   'לפני שמוציאים שקל אחד על פרסום, צריך לוודא ש־Meta Business Manager מוגדר נכון: הפיקסל מחובר לכל הדפים הנכונים, אירועי המרה מוגדרים לפי עדיפות (רכישה, ליד, התחלת תשלום), וה־Conversions API עובד במקביל לפיקסל כדי לכסות על הפערים של iOS. זה לא סקסי, אבל זה מה שמכפיל את ההחזר על ההשקעה בפרסום.',
   'אותו עיקרון חל על גוגל: חשבון Google Ads מחובר ל־Google Analytics 4, המרות מוגדרות כראשיות (לא משניות), ו־Tag Manager מוגדר כך שכל שינוי עתידי לא ידרוש מפתח. תשתית חזקה = נתונים אמיתיים = החלטות נכונות.']),
 dict(slug='strategy-not-template', cat='אסטרטגיה', date='פברואר 2026', iso='2026-02-01',
  title='פרסום שמאחוריו ראש, ולא שבלונה',
  desc='למה קמפיין שהועתק מהמתחרה נראה טוב על הנייר ולא מוכר כלום, ואיך מתאימים את המתודולוגיה לתקציב של 3,000 ש"ח ושל 80,000 ש"ח בחודש.',
  body=[
   'אחרי 15 שנה בתחום, אני יכול לזהות קמפיין שנבנה מתוך העתקה מהמתחרה ממרחק של קילומטר. הוא נראה טוב על הנייר: קריאייטיב נחמד, טקסט שיווקי מהוקצע, תקציב "הגיוני". אבל הוא לא מוכר כלום. הסיבה? אף אחד לא שאל קודם מה באמת גורם ללקוח הספציפי הזה לקנות, ועל מה הוא מוכן לשלם.',
   'השלב הקריטי ביותר הוא לפני שנפתח את מנהל הפרסום. להבין מי הלקוח האידיאלי של העסק, מה מציק לו, איפה הוא מבלה אונליין, ואיזה מסר עשוי לגרום לו לעצור בסקרול ולפעול. יש לגוגל כלים מצוינים לזה, אבל שום כלי לא יחליף שיחה אמיתית עם בעל העסק.',
   'התכנון האסטרטגי צריך להיות מותאם לתקציב: עסק עם 3,000 ש"ח בחודש לא יכול לעבוד על אותה מתודולוגיה של עסק עם 80,000 ש"ח. הראשון צריך להיות ממוקד: מסר חד, ערוץ אחד שעובד. השני יכול להרשות לעצמו מיקס מדיה ובדיקות מקבילות. שבלונה אחת לשניהם זו רשלנות.']),
 dict(slug='big-budgets-are-different', cat='תקציבים גדולים', date='פברואר 2026', iso='2026-02-01',
  title='גדול זה לא מסובך, זה אחרת',
  desc='מה משתנה כשמנהלים מאות אלפי שקלים בחודש על כמה פלטפורמות: קצב תקציב, תקרות הצעה, מודל ייחוס אחד ודוח מאוחד.',
  body=[
   'כשמנהלים תקציבי פרסום של מאות אלפי שקלים בחודש על פני כמה פלטפורמות, הכללים משתנים לחלוטין. מה שעובד על 5,000 ש"ח לא עובד על 500,000 ש"ח. לא כי הסכום גדול יותר, אלא כי הדינמיקה של הפלטפורמה, קהל היעד ותחרות המכרזים משתנים.',
   'הטעות הנפוצה ביותר של מנהלי פרסום שמתרחבים לתקציבים גדולים: הם מגדילים את ההוצאה בלי לשמור על קצב תקציב נכון. האלגוריתמים של מטא וגוגל יאכלו תקציב גדול מהר מאוד בלי לייצר החזר יחסי, אם לא מגדירים תקרות הצעה ויעדי נתח חשיפות נכון.',
   'ניהול פלטפורמות מרובות (מטא, גוגל, טיקטוק, טאבולה) בו־זמנית דורש גם מודל ייחוס ברור. בלי זה, כל פלטפורמה תיטול לעצמה קרדיט על אותה המרה, ותקבלו דוחות נוצצים שמסתירים כפילויות. הפתרון: ייחוס מבוסס נתונים עם חלון המרה אחיד בכל הפלטפורמות, ודוח מאוחד שמסתכל על הכול יחד.']),
]

for i, a in enumerate(ARTICLES):
    others = ''.join(f'<li><a href="{b["slug"]}.html">{H.escape(b["title"])}</a></li>' for j, b in enumerate(ARTICLES) if j != i)
    paras = ''.join(f'<p>{H.escape(p)}</p>' for p in a['body'])
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['desc'], "datePublished": a['iso'], "inLanguage": "he",
          "author": {"@type": "Person", "name": "גיא שושני"}, "publisher": {"@type": "Organization", "name": "Z.G Digital (זיגזג מדיה)", "url": "https://zigzagmedia.co.il"},
          "mainEntityOfPage": f"https://zigzagmedia.co.il/articles/{a['slug']}.html"}
    body = f'''<article class="sec page post"><div class="wrap narrow">
  <p class="eyebrow">{H.escape(a['cat'])}</p>
  <h1>{H.escape(a['title'])}</h1>
  <p class="meta">גיא שושני · {a['date']}</p>
  {paras}
  <div class="cta"><a class="btn" href="../index.html#contact">שלחו לנו את החשבון לבדיקה</a><a class="link" href="../knowledge.html">לכל המאמרים →</a></div>
  <div class="more"><h2>עוד מאמרים</h2><ul>{others}</ul></div>
</div></article>'''
    page(f'articles/{a["slug"]}.html', a['title'] + ' · Z.G Digital', a['desc'], body, depth=1,
         extra_head='<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')

items = ''.join(f'<a class="item" href="articles/{a["slug"]}.html"><p class="eyebrow">{H.escape(a["cat"])}</p><h2>{H.escape(a["title"])}</h2><p>{H.escape(a["desc"])}</p></a>' for a in ARTICLES)
page('knowledge.html', 'ידע · Z.G Digital', 'קצת ידע לדרך: תשתית ודאטה, אסטרטגיה, ותקציבים גדולים. מאמרים קצרים מתוך 15 שנה של פרסום ממומן.',
     f'''<section class="sec page"><div class="wrap narrow">
  <p class="eyebrow">ידע</p>
  <h1 class="post" style="font-size:clamp(36px,5vw,64px);margin:10px 0 8px">קצת ידע לדרך.</h1>
  <p class="lead">שלושה דברים שאנחנו אומרים לכל לקוח חדש, בלי קשר לגודל התקציב.</p>
  <div class="list">{items}</div>
</div></section>''')

# ---------------- accessibility statement ----------------
page('accessibility.html', 'הצהרת נגישות · Z.G Digital', 'הצהרת הנגישות של אתר Z.G Digital (זיגזג מדיה): רמת ההתאמה, מה נעשה, חריגים ידועים ודרכי פנייה.',
     '''<section class="sec page acc"><div class="wrap narrow post">
  <p class="eyebrow">נגישות</p>
  <h1>הצהרת נגישות</h1>
  <p class="meta">עודכן לאחרונה: אוקטובר 2026</p>
  <p>ז.ג דיגיטל בע"מ (Z.G Digital, זיגזג מדיה) רואה חשיבות רבה במתן שירות שוויוני לכלל הציבור, ובכלל זה לאנשים עם מוגבלות. אנחנו משקיעים מאמצים כדי שהאתר יהיה נגיש, נוח וקריא לכולם, בהתאם לתקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע"ג–2013, ולתקן הישראלי ת"י 5568 המבוסס על הנחיות WCAG 2.0 ברמה AA. האתר נבנה תוך כוונה לעמוד גם בהנחיות המעודכנות WCAG 2.2 ברמה AA.</p>
  <h2>מה נעשה באתר</h2>
  <ul>
    <li>ניווט מלא במקלדת, עם סימון פוקוס ברור בכל קישור, כפתור ושדה, וקישור "דלג לתוכן" בראש כל עמוד.</li>
    <li>ניגודיות צבעים של 4.5:1 לפחות לכל טקסט, ו־3:1 לגבולות ופקדים.</li>
    <li>מבנה כותרות היררכי, תיאור חלופי לכל תמונה בעלת משמעות, ושמות נגישים לכפתורים עם אייקון.</li>
    <li>טפסים עם תוויות גלויות, סימון שדות חובה, והודעות שגיאה בטקסט ליד השדה.</li>
    <li>תנועה: האתר מכבד את הגדרת "הפחתת תנועה" של מערכת ההפעלה, ובמחשב קיים כפתור "עצור תנועה" שעוצר כל תנועה אוטומטית.</li>
    <li>התאמה מלאה למסכי טלפון, הגדלת טקסט עד 200% והצגה תקינה ברוחב 320 פיקסלים, בלי גלילה אופקית.</li>
    <li>שטחי לחיצה של 44×44 פיקסלים לפחות, וקרוסלת השירותים בטלפון ניתנת להפעלה בכפתורים ובמקלדת.</li>
    <li>הטקסט נכתב בעברית פשוטה, ומספרים, כתובות ומיילים מסומנים בכיוון הנכון.</li>
  </ul>
  <h2>חריגים ידועים</h2>
  <ul>
    <li>רקע הפתיח כולל אנימציה עדינה שאינה ניתנת לעצירה בטלפון (היא נעצרת אוטומטית כשמופעלת "הפחתת תנועה" במכשיר).</li>
    <li>קבצי וידאו, אם יתווספו לאתר, יצורפו עם כתוביות.</li>
  </ul>
  <h2>נתקלתם בבעיה?</h2>
  <p>אם מצאתם רכיב שאינו נגיש או שיש לכם הצעה לשיפור, נשמח לשמוע ולתקן: רכז הנגישות של החברה הוא גיא שושני. אפשר לפנות בטלפון <a href="tel:+972525649801" dir="ltr">052-5649801</a>, בוואטסאפ, או במייל <a href="mailto:guy@zigzagmedia.co.il" dir="ltr">guy@zigzagmedia.co.il</a>. נשתדל להשיב תוך שני ימי עסקים.</p>
  <p>ההצהרה נכתבה בהתאם לנדרש בתקנות, ותעודכן עם כל שינוי מהותי באתר.</p>
</div></section>''')

# ---------------- 404 ----------------
ROOT404 = True
page('404.html', 'הדף הלך לאיבוד · Z.G Digital', 'הדף שחיפשתם לא נמצא. חזרו לדף הבית של Z.G Digital או דברו איתנו.',
     '''<section class="sec page lost"><div class="wrap grid">
  <div class="copy">
    <p class="eyebrow">404</p>
    <h1 style="font-size:clamp(40px,6vw,76px)">הדף הזה<br><span class="k">הלך לאיבוד.</span></h1>
    <p class="lead">גם לנו זה קורה לפעמים בתל אביב. הקישור ישן, או שהדף עבר דירה.</p>
    <div class="cta"><a class="btn" href="/">לדף הבית</a><a class="link" href="/#contact">דברו איתנו ←</a></div>
  </div>
  <figure class="frame" style="aspect-ratio:1/1;width:min(100%,460px);justify-self:center"><div class="pic"><picture><source type="image/webp" srcset="/art/w/cat-480.webp 480w, /art/w/cat-800.webp 800w, /art/w/cat-1047.webp 1047w" sizes="(max-width:899px) calc(100vw - 40px), 460px"><img src="/art/cat.jpg" alt="איור דיו של חתול על מעקה מול ירח סגול" width="1300" height="1300"></picture></div></figure>
</div></section>''')
