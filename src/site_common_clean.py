import re, os
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
