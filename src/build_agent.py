# -*- coding: utf-8 -*-
# דף הנחיתה "סוכן הפרסום" -> marketing-agent.html (עמוד עצמאי: העיצוב שלו, התפריט והמדידה של האתר)
# parts/agent_style.html + parts/agent_body.html ; התמונות: art/agent-1200.webp, art/agent-2000.webp, art/agent-og.jpg
import re, json, datetime, html as H
from site_common import base, head, nav, rel, clean_urls, SITE_ROOT

PATH = 'marketing-agent.html'
TITLE = 'סוכן פרסום בבינה מלאכותית לעסק שלכם · Z.G Digital'
DESC = 'סוכן בינה מלאכותית לניהול הפרסום הממומן של העסק, שנשען על 15 שנות הניסיון של גיא שושני וז.ג דיגיטל: שואל את השאלות שמקצוען פרסום ותיק היה שואל, ומקים את הקמפיין מקצה לקצה.'
DIFF = 'את היכולות עצמן (חיבור לחשבונות הפרסום, אוטומציות, יצירת מודעות) אפשר למצוא היום בהרבה מקומות. מה שמבדל את הסוכן הזה הוא הידע שנכנס אליו: 15 שנות ניסיון של גיא שושני בניהול פרסום ממומן, כולל שיטות עבודה, קייס סטאדיס, נתונים אמיתיים ותובנות מהשטח.'
WHAT = 'הקמה וליווי של סוכן בינה מלאכותית שמחובר לחשבונות הפרסום של העסק: כותבים לו מה הצורך, הוא שואל את השאלות שמקצוען פרסום ותיק היה שואל, ומייצר את הקמפיין מקצה לקצה.'
CAPS = [('ייעוץ מקצועי בלבד', 'הסוכן מחובר בצורה שמאפשרת קריאה בלבד, לטובת מתן חוות דעת מקצועית על הנעשה בפלטפורמות הפרסום השונות.'), ('שליטה וניהול', 'הסוכן יכול לשלוט בפועל במנהלי המודעות השונים: לעצור, להפעיל, לשנות תקציבים ולהקים מ־0 קמפיינים שונים.'), ('אוטומציות', 'הסוכן יתחבר לנכסים המשלימים כמו CRM, אתרי קומרס או קבצים לניהול לידים, ויוכל לבצע תיעוד, מעקב, דיווח וגזירת מסקנות עצמאית לטובת אופטימיזציה לתהליכי הפרסום.'), ('יכולות קריאייטיב', 'הסוכן יהיה מחובר ליכולות יצירת תמונות ווידאו ועריכה בקוד, ויוכל ליצור מודעות מקצה לקצה לפי דרישת הלקוח.')]

# head: המטא, האייקונים והפיקסלים של האתר, בלי גיליון הסגנונות של דף הבית
h = re.sub(r'<style>.*?</style>\s*', '', head, flags=re.S)
h = re.sub(r'<title>.*?</title>', f'<title>{H.escape(TITLE)}</title>', h, flags=re.S)
h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{H.escape(DESC, quote=True)}">', h)
h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{H.escape(TITLE, quote=True)}">', h)
h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{H.escape(DESC, quote=True)}">', h)
h = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{SITE_ROOT}/art/agent-og.jpg">', h)
h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE_ROOT}/{PATH}">', h)
h = h.replace('<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/heebo-hebrew-400-normal.woff2">', '<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/heebo-hebrew-700-normal.woff2">')

nav_css = base[base.index('/* nav */'):base.index('/* type */')]
style = open('parts/agent_style.html', encoding='utf-8').read().replace('__NAV_CSS__', nav_css)
ORG, GUY, URL = SITE_ROOT + '/#org', SITE_ROOT + '/#guy-shoshani', SITE_ROOT + '/' + PATH[:-5]   # כתובת נקייה תמיד
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "WebPage", "@id": URL, "url": URL, "name": TITLE, "description": DESC, "inLanguage": "he", "about": {"@id": URL + "#service"}, "isPartOf": {"@type": "WebSite", "url": SITE_ROOT, "name": "Z.G Digital"}},
  {"@type": "Service", "@id": URL + "#service", "name": "סוכן פרסום בבינה מלאכותית", "serviceType": "הקמה וליווי של סוכן בינה מלאכותית לניהול פרסום ממומן",
   "description": WHAT + ' ' + DIFF + ' המוח של הסוכן מכיל גם את החוקים והרגולציות של פלטפורמות הפרסום השונות.',
   "disambiguatingDescription": DIFF, "areaServed": "IL", "url": URL, "provider": {"@id": ORG},
   "hasOfferCatalog": {"@type": "OfferCatalog", "name": "יכולות לבחירת הלקוח", "itemListElement": [
       {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d}} for n, d in CAPS]}},
  {"@type": "ProfessionalService", "@id": ORG, "name": "Z.G Digital (ז.ג דיגיטל)", "alternateName": "זיגזג מדיה", "url": SITE_ROOT, "telephone": "+972525649801",
   "address": {"@type": "PostalAddress", "addressLocality": "תל אביב", "addressCountry": "IL"}, "founder": {"@id": GUY}},
  {"@type": "Person", "@id": GUY, "name": "גיא שושני", "jobTitle": "מייסד ז.ג דיגיטל, איש פרסום דיגיטלי", "worksFor": {"@id": ORG},
   "description": "15 שנות ניסיון בניהול פרסום ממומן. שיטות העבודה, הקייס סטאדיס, הנתונים והתובנות שלו מהשטח הם הידע שעליו בנוי סוכן הפרסום.",
   "knowsAbout": ["פרסום ממומן", "Performance marketing", "Meta Ads", "Google Ads", "YouTube Ads", "TikTok Ads", "ChatGPT Ads", "מדידה וייחוס", "סוכני בינה מלאכותית לפרסום"]}]}
h = h.replace('</head>', style + f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n</head>')

# התפריט של האתר: הקישורים מובילים לדף הבית, "דברו איתנו" מוביל לטופס של הדף הזה
n = rel(nav, 0)
n = n.replace('<a class="btn" href="index.html#contact">', '<a class="btn" href="#talk">')
n = n.replace(f'<a class="agent" href="{PATH}">', f'<a class="agent" href="{PATH}" aria-current="page">')

endpoint = re.search(r"const LEAD_ENDPOINT='([^']*)'", base).group(1)
body = open('parts/agent_body.html', encoding='utf-8').read().replace('__NAV__', n).replace('__LEAD_ENDPOINT__', endpoint)
out = f'<!doctype html>\n<html lang="he" dir="rtl">\n{h}\n<body>\n{body}\n</body></html>'
out = clean_urls(out)
open(PATH, 'w', encoding='utf-8').write(out)
print('written', PATH, len(out))

# sitemap + llms.txt
sm = open('sitemap.xml', encoding='utf-8').read()
loc = clean_urls(f'{SITE_ROOT}/{PATH}')
if loc not in sm:
    sm = sm.replace('</urlset>', f'  <url><loc>{loc}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>\n</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8').write(sm)
t = open('llms.txt', encoding='utf-8').read()
line = f'- [סוכן פרסום בבינה מלאכותית]({loc}): {WHAT} מה מבדל: {DIFF} המוח של הסוכן מכיל גם את החוקים והרגולציות של פלטפורמות הפרסום. ארבע יכולות לבחירת הלקוח: ייעוץ מקצועי בלבד (קריאה בלבד וחוות דעת), שליטה וניהול (הקמה, עצירה ושינוי של קמפיינים ותקציבים), אוטומציות (חיבור ל-CRM, לחנות ולקובצי לידים) ויכולות קריאייטיב (יצירת מודעות מקצה לקצה).\n'
if '- [סוכן פרסום בבינה מלאכותית](' in t:
    t = re.sub(r'- \[סוכן פרסום בבינה מלאכותית\]\([^\n]*\n', lambda m: line, t, count=1)
else:
    t = t.replace('\n## תחומי עסקים', line + '\n## תחומי עסקים', 1)
open('llms.txt', 'w', encoding='utf-8').write(t)
