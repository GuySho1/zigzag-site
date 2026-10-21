# ז.ג דיגיטל — אתר הסוכנות

אתר HTML סטטי. הקבצים בשורש הריפו הם מה שמוגש לגולשים.

- `build.py` מייצר את `index.html` (`python3 build.py light`) ואת `dark.html` (`python3 build.py dark`).
- `build_pages.py` מייצר את דפי הידע, המאמרים, הנגישות ו־404 מתוך `index.html`.
- `lead-script.gs` הוא הסקריפט של גוגל שמקבל את הטופס (פרוס בחשבון גוגל של הסוכנות).
- `deploy/` קבצי הגדרה לשרת.

פריסה: cPanel → Git Version Control → Pull or Deploy.
