# Shared helpers for the sub-pages: head/nav/footer from index.html, rel(), page()
import re, os, json, html as H
os.chdir('/home/claude/site/calm')
CLEAN = os.environ.get('CLEAN_URLS') == '1'   # 1 = כתובות בלי .html (האתר החי); 0 = קבצים סטטיים (תצוגה מקדימה)
SITE_ROOT = 'https://zigzagmedia.co.il'

def clean_urls(s):
    """Turn every internal .html link into a root-absolute clean URL (knowledge.html → /knowledge, index.html#x → /#x)."""
    if not CLEAN: return s
    def fix(m):
        attr, url, frag = m.group(1), m.group(2), m.group(3) or ''
        pre = ''
        if url.startswith(SITE_ROOT + '/'): pre, url = SITE_ROOT, url[len(SITE_ROOT)+1:]
        while url.startswith('../') or url.startswith('./'): url = url[3:] if url.startswith('../') else url[2:]
        url = url.lstrip('/')
        url = '' if url == 'index.html' else url[:-5]
        return f'{attr}="{pre}/{url}{frag}"'
    s = re.sub(r'\b(href|content|data-thanks)="((?:https://zigzagmedia\.co\.il/)?[^"#:]*?\.html)(#[^"]*)?"', fix, s)
    s = re.sub(r'https://zigzagmedia\.co\.il/((?:[\w\-/]+?))\.html(?=["\s<)]|$)', lambda m: SITE_ROOT + '/' + ('' if m.group(1) == 'index' else m.group(1)), s)
    return s

base = open('index.html', encoding='utf-8').read()
head = re.search(r'<head>.*?</head>', base, re.S).group(0)
nav = re.search(r'<a class="skip".*?</nav>', base, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', base, re.S).group(0)

def rel(s, depth):
    pre = '../' * depth
    s = s.replace('href="#main"', 'href="#MAIN"').replace('href="#top"', f'href="{pre}index.html"')
    s = re.sub(r'href="#([a-z\-]+)"', lambda m: f'href="{pre}index.html#{m.group(1)}"', s)
    s = s.replace('href="#MAIN"', 'href="#main"')
    for f in ('agents.html', 'knowledge.html', 'accessibility.html', 'services.html', 'llms.txt', 'apple-touch-icon.png', 'favicon.svg', 'favicon-32.png', 'og.jpg'):
        s = s.replace(f'href="{f}"', f'href="{pre}{f}"')
    s = s.replace('src="art/', f'src="{pre}art/').replace('href="art/', f'href="{pre}art/').replace('content="og.jpg', f'content="{pre}og.jpg')
    s = s.replace('url(fonts/', f'url({pre}fonts/').replace('href="fonts/', f'href="{pre}fonts/').replace('href="services/', f'href="{pre}services/')
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

def page(path, title, desc, body, depth=0, extra_head='', canonical=None, og_image=None, og_type=None):
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{H.escape(title)}</title>', h, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{H.escape(desc, quote=True)}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{H.escape(title, quote=True)}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{H.escape(desc, quote=True)}">', h)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://zigzagmedia.co.il/{canonical or path}">', h)
    if og_image:
        h = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{og_image}">', h)
        h = re.sub(r'<meta property="og:image:width" content="\d+"><meta property="og:image:height" content="\d+">', '', h)
    if og_type: h = h.replace('<meta property="og:type" content="website">', f'<meta property="og:type" content="{og_type}">')
    h = h.replace('</head>', EXTRA_CSS + extra_head + '</head>')
    out = f'<!doctype html>\n<html lang="he" dir="rtl">\n{rel(h, depth)}\n<body>\n{rel(nav, depth)}\n<main id="main">\n{body}\n</main>\n{rel(footer, depth)}\n</body></html>'
    if path == '404.html':
        out = re.sub(r'(href|src|content)="(?!https?:|/|#|mailto:|tel:|data:)([^"]+)"', r'\1="/\2"', out)
        out = out.replace('url(fonts/', 'url(/fonts/')
    out = clean_urls(out)
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf-8').write(out)
    print('written', path, len(out))

