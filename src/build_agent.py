# -*- coding: utf-8 -*-
# דף הנחיתה "סוכן הפרסום" -> marketing-agent.html (עמוד עצמאי: העיצוב שלו, התפריט והמדידה של האתר)
# parts/agent_style.html + parts/agent_body.html ; התמונות: art/agent-1200.webp, art/agent-2000.webp, art/agent-og.jpg
import re, json, datetime, html as H
from site_common import base, head, nav, rel, clean_urls, SITE_ROOT

PATH = 'marketing-agent.html'
TITLE = 'סוכן פרסום בבינה מלאכותית לעסק שלכם · Z.G Digital'
DESC = 'סוכן בינה מלאכותית שמנהל את הפרסום הממומן שלכם: כותבים לו מה הצורך, הוא שואל את השאלות שמקצוען פרסום ותיק היה שואל, ומייצר את הקמפיין מקצה לקצה. מבוסס על 15 שנות הניסיון של ז.ג דיגיטל.'

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
ld = {"@context": "https://schema.org", "@type": "Service", "name": "סוכן פרסום בבינה מלאכותית", "serviceType": "הקמה וליווי של סוכן בינה מלאכותית לניהול פרסום ממומן",
      "description": DESC, "areaServed": "IL", "url": f"{SITE_ROOT}/{PATH}",
      "provider": {"@type": "ProfessionalService", "name": "Z.G Digital (ז.ג דיגיטל)", "url": SITE_ROOT, "telephone": "+972525649801"}}
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
line = f'- [סוכן פרסום בבינה מלאכותית]({loc}): הקמה וליווי של סוכן בינה מלאכותית שמחובר לחשבונות הפרסום של העסק. ארבע יכולות לבחירה: ייעוץ מקצועי בלבד (קריאה בלבד), שליטה וניהול (הקמה ושינוי של קמפיינים), אוטומציות (חיבור ל-CRM, לחנות ולקובצי לידים) ויכולות קריאייטיב (יצירת מודעות). מבוסס על 15 שנות הניסיון של ז.ג דיגיטל.\n'
if 'סוכן פרסום בבינה מלאכותית' not in t:
    t = t.replace('\n## תחומי עסקים', line + '\n## תחומי עסקים', 1)
    open('llms.txt', 'w', encoding='utf-8').write(t)
