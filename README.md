# ז.ג דיגיטל — אתר הסוכנות

אתר HTML סטטי.

- `site/` — מה שמוגש לגולשים (זה מה שנפרס לשרת).
- `src/build.py` מייצר את `site/index.html` (`python3 build.py light`) ואת `site/dark.html` (`python3 build.py dark`); `src/build_pages.py` מייצר את דפי הידע, המאמרים, הנגישות ו־404.
- `src/lead-script.gs` — סקריפט גוגל שמקבל את הטופס (פרוס בחשבון גוגל של הסוכנות).
- `deploy/` — קובצי הגדרה לשרת; `.cpanel.yml` אומר ל־cPanel לאן להעתיק.

פריסה: cPanel → Git Version Control → Manage → Pull or Deploy → Update from Remote, ואז Deploy HEAD Commit.
