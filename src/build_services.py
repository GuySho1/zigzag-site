# -*- coding: utf-8 -*-
# Service pages: content/services/*.md -> services/<slug>.html + services.html (index)
# Front matter: title, seo_title (optional), desc, kw (main search phrase), kw2 (optional), lead, articles (slugs, comma-separated), faq (lines "- שאלה | תשובה")
import re, os, json, html as H
import markdown
from site_common import page, rel, clean_urls
from build_content import CONTENT_CSS, ARTS, heb_date, SITE

if os.environ.get('SERVICES', '1') == '0':
    print('services: skipped (SERVICES=0)'); raise SystemExit(0)
ORDER = ['meta-ads', 'google-ads', 'performance', 'chatgpt-ads', 'creative', 'ai-for-business']

def parse(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)$', raw, re.S)
    if not m: raise SystemExit(f'{path}: missing front matter')
    meta, faq = {}, []
    for line in m.group(1).splitlines():
        if line.startswith('- ') and '|' in line:
            q, a = line[2:].split('|', 1); faq.append((q.strip(), a.strip()))
        elif ':' in line:
            k, v = line.split(':', 1); meta[k.strip()] = v.strip()
    for k in ('title', 'desc', 'kw', 'lead'):
        if k not in meta: raise SystemExit(f'{path}: missing {k}')
    meta['faq'] = faq
    meta['slug'] = os.path.splitext(os.path.basename(path))[0]
    meta['body_md'] = m.group(2).strip()
    meta['articles'] = [s.strip() for s in meta.get('articles', '').split(',') if s.strip()]
    return meta

SVCS = {parse(os.path.join('content/services', f))['slug']: parse(os.path.join('content/services', f))
        for f in os.listdir('content/services') if f.endswith('.md')}
SVCS = [SVCS[s] for s in ORDER if s in SVCS] + [v for k, v in SVCS.items() if k not in ORDER]
BY_SLUG = {a['slug']: a for a in ARTS}

SVC_CSS = '''<style>
.svcp .lead{font-size:clamp(19px,2.2vw,23px);line-height:1.6;color:var(--fg);margin:0 0 30px;max-width:62ch}
.svcp h2{font-size:clamp(23px,2.5vw,32px);margin:36px 0 10px}
.svcp p{font-size:18px;line-height:1.8;margin:0 0 16px}
.svcp strong{font-weight:900}
.faq{margin-top:40px;border-top:3px solid var(--line);padding-top:14px}
.faq h2{margin-top:10px}
.faq details{border-bottom:2px solid var(--line);padding:4px 0}
.faq summary{cursor:pointer;font-weight:700;font-size:19px;padding:14px 0;list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:'+';color:var(--moon);font-weight:900;font-size:26px;line-height:1;flex:none}
.faq details[open] summary::after{content:'–'}
.faq details p{margin:0 0 16px;color:var(--fg)}
.svcp .box{background:var(--bg2);border:3px solid var(--line);padding:22px 24px;margin:36px 0 0;position:relative}
.svcp .box::before{content:'';position:absolute;top:0;right:0;width:46px;height:5px;background:var(--moon)}
.svcp .box h2{margin:0 0 8px;font-size:24px}
.svcp .box p{margin:0 0 14px}
.svcp .cta{margin-top:10px}
.svcp .cta a.btn{min-height:50px;display:inline-flex;align-items:center;padding:0 24px;background:var(--moon);color:#fff;font-weight:700;text-decoration:none}
.svcp .cta a.link{font-weight:700;color:var(--moon)}
.svcp .others{margin-top:44px;border-top:3px solid var(--line);padding-top:22px}
.svcp .others h2{font-size:22px;margin:0 0 12px}
.svcp .others ul,.svcp .more ul{list-style:none;margin:0;padding:0;display:grid;gap:4px}
.svcp .others a,.svcp .more a{display:inline-flex;align-items:center;min-height:44px;font-weight:700;text-decoration:none;color:var(--moon)}
.svcp .more{margin-top:32px}
.svcp .more h2{font-size:22px;margin:0 0 10px}
.svcidx .list{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
</style>'''

def faq_html(faq):
    if not faq: return ''
    return '<section class="faq"><h2>שאלות שחוזרות</h2>' + ''.join(
        f'<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in faq) + '</section>'

for s in SVCS:
    body_html = markdown.markdown(s['body_md'], extensions=['extra'])
    related = [BY_SLUG[x] for x in s['articles'] if x in BY_SLUG]
    more = ('<section class="more"><h2>לקריאה נוספת</h2><ul>' + ''.join(
        f'<li><a href="../articles/{a["slug"]}.html">{H.escape(a["title"])}</a></li>' for a in related) + '</ul></section>') if related else ''
    others = [o for o in SVCS if o['slug'] != s['slug']]
    others_html = '<section class="others"><h2>עוד שירותים</h2><ul>' + ''.join(
        f'<li><a href="{o["slug"]}.html">{H.escape(o["title"])}</a></li>' for o in others) + '</ul></section>'
    ld_service = {"@context": "https://schema.org", "@type": "Service", "name": s['title'], "description": s['desc'], "serviceType": s['kw'],
                  "areaServed": "IL", "url": f"{SITE}/services/{s['slug']}.html",
                  "provider": {"@type": "ProfessionalService", "name": "Z.G Digital (ז.ג דיגיטל)", "url": SITE, "telephone": "+972525649801"}}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s['faq']]} if s['faq'] else None
    ld_crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "דף הבית", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "שירותים", "item": f"{SITE}/services.html"},
        {"@type": "ListItem", "position": 3, "name": s['title'], "item": f"{SITE}/services/{s['slug']}.html"}]}
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld_service, ld_faq, ld_crumbs) if x)
    body = f'''<section class="sec page"><div class="wrap narrow post svcp">
  <p class="eyebrow"><a href="../services.html" style="color:inherit;text-decoration:none">שירותים</a></p>
  <h1>{H.escape(s['title'])}</h1>
  <p class="lead">{H.escape(s['lead'])}</p>
  {body_html}
  {faq_html(s['faq'])}
  <div class="box"><h2>רוצים לדבר על החשבון שלכם?</h2><p>שיחה קצרה, בלי התחייבות, ובסופה תדעו מה אפשר לשפר, גם אם לא נעבוד יחד.</p>
    <div class="cta"><a class="btn" href="../index.html#contact">דברו איתנו</a><a class="link" href="https://wa.me/972525649801" target="_blank" rel="noopener">או בוואטסאפ ←</a></div></div>
  {more}
  {others_html}
</div></section>'''
    page(f'services/{s["slug"]}.html', (s.get('seo_title') or s['title']) + ' · Z.G Digital', s['desc'], body, depth=1,
         extra_head=CONTENT_CSS + SVC_CSS + lds)

# ---------------- services index ----------------
cards = ''.join(f'<a class="item" href="services/{s["slug"]}.html"><div class="txt"><h2>{H.escape(s["title"])}</h2><p>{H.escape(s["desc"])}</p></div></a>' for s in SVCS)
ld_list = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "name": s['title'], "url": f"{SITE}/services/{s['slug']}.html"} for i, s in enumerate(SVCS)]}
page('services.html', 'השירותים שלנו · Z.G Digital', 'פרסום ממומן במטא ובגוגל, פרפורמנס לתקציבים גדולים, פרסום בצ\'אט ג\'יפיטי, קריאייטיב לקמפיינים וסדנאות בינה מלאכותית לעסקים. סוכנות פרסום דיגיטלי מתל אביב.',
     f'''<section class="sec page"><div class="wrap hub svcidx">
  <p class="eyebrow">שירותים</p>
  <h1>מה אנחנו עושים</h1>
  <p class="lead" style="max-width:65ch">שישה דברים שאנחנו עושים כל יום, לכל אחד דף משלו: למי זה מתאים, איך זה עובד, מה כלול ומה לא.</p>
  <div class="list plain">{cards}</div>
</div></section>''', extra_head=CONTENT_CSS + SVC_CSS + f'<script type="application/ld+json">{json.dumps(ld_list, ensure_ascii=False)}</script>')
print('services:', len(SVCS))

# ---------------- llms.txt: services section ----------------
t = open('llms.txt', encoding='utf-8').read()
sec = '## דפי שירות\n\n' + ''.join(f'- [{s["title"]}]({SITE}/services/{s["slug"]}.html): {s["desc"]}\n' for s in SVCS) + '\n'
if '## דפי שירות' in t:
    t = re.sub(r'## דפי שירות.*?(?=\n## |\Z)', sec.rstrip('\n') + '\n', t, flags=re.S)
else:
    t = t.replace('## מאמרים', sec + '## מאמרים', 1)
open('llms.txt', 'w', encoding='utf-8').write(clean_urls(t))
