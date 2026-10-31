# ז.ג דיגיטל — אתר הסוכנות

אתר HTML סטטי.

- `site/` — מה שמוגש לגולשים (זה מה שנפרס לשרת).
- `src/build.py` מייצר את `site/index.html` (`python3 build.py light`) ואת `site/dark.html` (`python3 build.py dark`).
- **מאמרים:** כל מאמר הוא קובץ `src/content/articles/<slug>.md` (הפורמט מתועד בראש `src/build_content.py`). `python3 build_content.py` בונה את דפי המאמרים, את `knowledge.html` (עם סינון לפי נושא), את `sitemap.xml` ואת רשימת המאמרים ב־`llms.txt`. `src/build_pages.py` בונה את הנגישות ו־404.
- סרטוני הפרקים יושבים ב־`site/videos/` (16:9 לאתר).
- **פרק חדש = קובץ md + וידאו + דחיפה + משיכה בשרת.**
- `src/lead-script.gs` — סקריפט גוגל שמקבל את הטופס (פרוס בחשבון גוגל של הסוכנות).
- `deploy/` — קובצי הגדרה לשרת; `.cpanel.yml` אומר ל־cPanel לאן להעתיק.

פריסה: cPanel → Git Version Control → Manage → Pull or Deploy → Update from Remote, ואז Deploy HEAD Commit.
