# -*- coding: utf-8 -*-
# Content system: content/articles/*.md  ->  articles/<slug>.html + knowledge.html + sitemap.xml + the articles section of llms.txt
#
# Article file format (content/articles/<slug>.md):
#   ---
#   title: כותרת המאמר                      (חובה)
#   desc: משפט אחד: למי ומה יוצא מזה          (חובה, מופיע גם בגוגל ובכרטיס)
#   cat: קריאייטיב | נתונים ודוחות | אוטומציה | קמפיינים | תשתית ודאטה | אסטרטגיה | תקציבים גדולים   (חובה)
#   date: 2026-11-03                         (חובה, ISO)
#   read: 4                                  (דקות קריאה)
#   tool: קלוד + המחבר של מטא                (אופציונלי: הכלי/היכולת)
#   episode: 1                               (אופציונלי: מספר פרק בסדרה)
#   video: videos/meta-mcp-16x9.mp4          (אופציונלי: הסרטון הקצר, יחסית לשורש האתר)
#   poster: videos/meta-mcp-poster.jpg       (אופציונלי: תמונת פתיחה לסרטון)
#   cover: art/cat.jpg                       (אופציונלי: תמונה לכרטיס בדף הידע)
#   cta: רוצים שנבנה לכם את זה? | index.html#contact   (אופציונלי: טקסט | קישור)
#   draft: true                              (אופציונלי: לא נבנה ולא נכנס למפת האתר)
#   ---
#   גוף המאמר ב־Markdown. כותרות ## , רשימות, קישורים, **הדגשה**, > ציטוט, תמונות ![תיאור](../art/x.jpg)
#
# Build: python3 build_content.py   (after build.py light; before build_pages.py is fine too)
import re, os, json, html as H, datetime
import markdown
from site_common import page, rel, head

SITE = 'https://zigzagmedia.co.il'
CATS = ['קריאייטיב', 'נתונים ודוחות', 'אוטומציה', 'קמפיינים', 'תשתית ודאטה', 'אסטרטגיה', 'תקציבים גדולים']

def parse(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)$', raw, re.S)
    if not m: raise SystemExit(f'{path}: missing front matter')
    meta = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1); meta[k.strip()] = v.strip()
    for k in ('title', 'desc', 'cat', 'date'):
        if k not in meta: raise SystemExit(f'{path}: missing {k}')
    if meta['cat'] not in CATS: raise SystemExit(f'{path}: unknown cat "{meta["cat"]}" (allowed: {", ".join(CATS)})')
    meta['slug'] = os.path.splitext(os.path.basename(path))[0]
    meta['body_md'] = m.group(2).strip()
    meta['read'] = int(meta.get('read') or max(2, round(len(meta['body_md'].split()) / 180)))
    meta['draft'] = meta.get('draft', '').lower() in ('true', '1', 'yes', 'כן')
    return meta

def heb_date(iso):
    y, mo, d = iso.split('-')
    months = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר']
    return f'{months[int(mo)-1]} {y}'

ARTS = [parse(os.path.join('content/articles', f)) for f in sorted(os.listdir('content/articles')) if f.endswith('.md')]
ARTS = [a for a in ARTS if not a['draft']]
ARTS.sort(key=lambda a: (a['date'], a.get('episode', '0')), reverse=True)

CONTENT_CSS = '''<style>
.post .vid{margin:0 0 28px;border:3px solid var(--line);background:var(--ink);position:relative;box-shadow:10px 10px 0 var(--moon)}
.post .vid video{display:block;width:100%;height:auto;aspect-ratio:16/9;background:#000}
.post .sum{background:var(--bg2);border-inline-start:4px solid var(--moon);padding:16px 18px;margin:0 0 28px;font-size:17px;line-height:1.65}
.post .sum b{font-weight:900}
.post ul,.post ol{padding-inline-start:22px;margin:0 0 18px;font-size:18px;line-height:1.75}
.post li{margin:6px 0}
.post blockquote{margin:0 0 18px;padding:12px 18px;border-inline-start:4px solid var(--line);color:var(--dim);font-size:18px}
.post img{max-width:100%;height:auto;border:3px solid var(--line);margin:8px 0 18px}
.post code{font-family:ui-monospace,monospace;font-size:.92em;background:var(--bg2);padding:1px 6px}
.post pre{background:var(--ink);color:var(--bg);padding:16px 18px;overflow:auto;font-size:15px;line-height:1.6;margin:0 0 18px;direction:ltr;text-align:left}
.post pre code{background:none;padding:0;color:inherit}
.post a{color:var(--moon);font-weight:700}
.post table{width:100%;border-collapse:collapse;margin:0 0 22px;font-size:16px}
.post th,.post td{border:2px solid var(--line);padding:8px 12px;text-align:start;vertical-align:top}
.post th{background:var(--ink);color:var(--bg);font-weight:900}
.post .ph{background:var(--bg2);border:2px dashed var(--dim);color:var(--dim);padding:14px 16px;margin:0 0 18px;font-size:15px}
.post .fig{margin:8px 0 26px;text-align:center}
.post .fig img{margin:0;max-width:min(100%,640px)}
.post .fig.tall img{max-width:min(100%,420px)}
.post .fig figcaption{color:var(--dim);font-size:15px;line-height:1.5;margin-top:10px;text-align:start}
.post .tool{display:inline-block;margin-inline-start:10px;color:var(--dim);font-weight:400}
.post .ep{display:inline-block;background:var(--ink);color:var(--bg);font-weight:900;padding:2px 10px;margin-inline-end:8px;font-size:14px}
.hub .filters{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 6px}
.hub .filters button{min-height:44px;padding:8px 16px;border:3px solid var(--line);background:transparent;color:var(--fg);font:inherit;font-weight:700;cursor:pointer}
.hub .filters button[aria-pressed=true]{background:var(--ink);color:var(--bg)}
.hub .filters button:focus-visible{outline:3px solid var(--moon);outline-offset:2px}
.hub .list{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.hub .item{display:flex;flex-direction:column;gap:6px;padding:0;overflow:hidden}
.hub .item .cov{aspect-ratio:16/9;background:var(--ink);overflow:hidden;border-bottom:3px solid var(--line)}
.hub .item .cov img{width:100%;height:100%;object-fit:cover;display:block;filter:grayscale(1) contrast(1.05)}
.hub .item .txt{padding:18px 22px 22px}
.hub .item .meta{color:var(--dim);font-size:14px;margin-top:10px}
.hub .item[hidden]{display:none}
.hub .count{color:var(--dim);font-size:15px;margin:0 0 18px}
.hub h2.grp{font-size:clamp(26px,3.4vw,38px);margin:40px 0 6px}
.hub p.grp{color:var(--dim);margin:0 0 18px;max-width:65ch}
.hub .list.plain{grid-template-columns:1fr;gap:12px}
.hub .list.plain .item{flex-direction:row;align-items:baseline;gap:18px;padding:16px 22px}
.hub .list.plain .item .txt{padding:0;flex:1}
.hub .list.plain .item h2{font-size:22px;margin:4px 0 6px}
.hub .list.plain .item p{margin:0}
.hub .list.plain .item .meta{margin-top:6px}
</style>'''

def md(text):
    text = re.sub(r'^\[צילום מסך: (.*?)\]$', r'<p class="ph">[צילום מסך יתווסף כאן: \1]</p>', text, flags=re.M)
    return markdown.markdown(text, extensions=['extra', 'sane_lists', 'smarty'], output_format='html5')

for i, a in enumerate(ARTS):
    same = [b for b in ARTS if b is not a and b['cat'] == a['cat']][:2]
    others = (same + [b for b in ARTS if b is not a and b not in same])[:3]
    more = ''.join(f'<li><a href="{b["slug"]}.html">{H.escape(b["title"])}</a></li>' for b in others)
    video = ''
    if a.get('video'):
        poster = f' poster="../{a["poster"]}"' if a.get('poster') else ''
        video = f'<figure class="vid"><video controls playsinline preload="metadata"{poster} src="../{a["video"]}" aria-label="הסרטון הקצר: {H.escape(a["title"], quote=True)}"></video></figure>'
    ep = f'<span class="ep">פרק {a["episode"]}</span>' if a.get('episode') else ''
    tool = f'<span class="tool">· {H.escape(a["tool"])}</span>' if a.get('tool') else ''
    cta_t, cta_h = 'שלחו לנו את החשבון לבדיקה', '../index.html#contact'
    if a.get('cta') and '|' in a['cta']:
        cta_t, cta_h = [x.strip() for x in a['cta'].split('|', 1)]
        if not cta_h.startswith(('http', '../', '#')): cta_h = '../' + cta_h
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['desc'], "datePublished": a['date'], "inLanguage": "he",
          "author": {"@type": "Person", "name": "גיא שושני"}, "publisher": {"@type": "Organization", "name": "Z.G Digital (ז.ג דיגיטל)", "url": SITE},
          "mainEntityOfPage": f"{SITE}/articles/{a['slug']}.html", "articleSection": a['cat']}
    if a.get('video'):
        ld["video"] = {"@type": "VideoObject", "name": a['title'], "description": a['desc'], "uploadDate": a['date'], "contentUrl": f"{SITE}/{a['video']}", **({"thumbnailUrl": f"{SITE}/{a['poster']}"} if a.get('poster') else {})}
    body = f'''<article class="sec page post"><div class="wrap narrow">
  <p class="eyebrow">{ep}{H.escape(a['cat'])}{tool}</p>
  <h1>{H.escape(a['title'])}</h1>
  <p class="meta">גיא שושני · {heb_date(a['date'])} · {a['read']} דקות קריאה</p>
  {video}
  <p class="sum"><b>בקצרה:</b> {H.escape(a['desc'])}</p>
  {md(a['body_md'])}
  <div class="cta"><a class="btn" href="{cta_h}">{H.escape(cta_t)}</a><a class="link" href="../knowledge.html">לכל המאמרים →</a></div>
  <div class="more"><h2>עוד בנושא</h2><ul>{more}</ul></div>
</div></article>'''
    page(f'articles/{a["slug"]}.html', a['title'] + ' · Z.G Digital', a['desc'], body, depth=1,
         extra_head=CONTENT_CSS + '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')

# ---------------- knowledge hub ----------------
def card(a, cover=True):
    cov = ''
    if cover and a.get('cover'):
        cov = f'<div class="cov"><img src="{a["cover"]}" alt="" loading="lazy" width="960" height="540"></div>'
    ep = f'<span class="ep">פרק {a["episode"]}</span>' if a.get('episode') else ''
    return (f'<a class="item" href="articles/{a["slug"]}.html" data-cat="{H.escape(a["cat"], quote=True)}">{cov}<div class="txt">'
            f'<p class="eyebrow">{ep}{H.escape(a["cat"])}</p><h2>{H.escape(a["title"])}</h2><p>{H.escape(a["desc"])}</p>'
            f'<p class="meta">{heb_date(a["date"])} · {a["read"]} דקות קריאה{(" · " + H.escape(a["tool"])) if a.get("tool") else ""}</p></div></a>')
SERIES = sorted([a for a in ARTS if a.get('episode')], key=lambda a: int(a['episode']))
REST = [a for a in ARTS if not a.get('episode')]
cats_present = [c for c in CATS if any(a['cat'] == c for a in ARTS)]
filters = '<button type="button" aria-pressed="true" data-f="">הכול</button>' + ''.join(f'<button type="button" aria-pressed="false" data-f="{H.escape(c, quote=True)}">{H.escape(c)}</button>' for c in cats_present)
hub_js = '''<script>document.addEventListener('DOMContentLoaded',()=>{const bs=[...document.querySelectorAll('.hub .filters button')],items=[...document.querySelectorAll('.hub .item')],n=document.getElementById('count');
bs.forEach(b=>b.addEventListener('click',()=>{bs.forEach(x=>x.setAttribute('aria-pressed',x===b));const f=b.dataset.f;let k=0;items.forEach(it=>{const show=!f||it.dataset.cat===f;it.hidden=!show;if(show)k++;});n.textContent=k+' מאמרים';}));});</script>'''
page('knowledge.html', 'מידע שימושי · Z.G Digital', 'מידע שימושי מז.ג דיגיטל: כלים פרקטיים לעבודה בפרסום ממומן ובבינה מלאכותית, ואיך מחברים אותם לזרימת העבודה.',
     f'''<section class="sec page hub"><div class="wrap">
  <p class="eyebrow">ידע</p>
  <h1 class="post" style="font-size:clamp(36px,5vw,64px);margin:10px 0 8px">מידע שימושי</h1>
  <p class="lead" style="max-width:65ch">רשימת כלים פרקטיים לעבודה, ואיך מחברים אותם לזרימת העבודה שלנו.</p>
  <div class="filters" role="group" aria-label="סינון לפי נושא">{filters}</div>
  <p class="count" id="count">{len(ARTS)} מאמרים</p>
  <h2 class="grp">הסדרה: הצ'אט שעובד</h2>
  <p class="grp">בכל פרק כלי אחד: מה הוא עושה, איך מחברים אותו, ומה המגבלות.</p>
  <div class="list">{''.join(card(a) for a in SERIES)}</div>
  <h2 class="grp">עוד מאמרים</h2>
  <p class="grp">על פרסום ממומן, תשתית ואסטרטגיה.</p>
  <div class="list plain">{''.join(card(a, cover=False) for a in REST)}</div>
</div></section>''', extra_head=CONTENT_CSS + hub_js)

# ---------------- sitemap ----------------
today = datetime.date.today().isoformat()
urls = [('/', today), ('/knowledge.html', today)] + [(f'/articles/{a["slug"]}.html', a['date']) for a in ARTS] + [('/accessibility.html', '2026-10-21'), ('/agents.html', '2026-10-21')]
open('sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>\n' for u, d in urls) + '</urlset>\n')

# ---------------- llms.txt: the articles section ----------------
t = open('llms.txt', encoding='utf-8').read()
sec = '## מאמרים (מדור הידע)\n\n' + ''.join(f'- [{a["title"]}]({SITE}/articles/{a["slug"]}.html): {a["desc"]}\n' for a in ARTS) + '\n'
if '## מאמרים' in t:
    t = re.sub(r'## מאמרים.*?(?=\n## |\Z)', sec.rstrip('\n') + '\n', t, flags=re.S)
else:
    t = t.replace('## יצירת קשר', sec + '## יצירת קשר') if '## יצירת קשר' in t else t + '\n' + sec
open('llms.txt', 'w', encoding='utf-8').write(t)
print('articles:', len(ARTS), '| sitemap + llms.txt updated')
