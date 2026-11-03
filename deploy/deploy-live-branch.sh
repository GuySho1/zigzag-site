#!/bin/bash
# ז.ג דיגיטל: פריסה אוטומטית של הענף live מגיטהאב. רץ מ-cron כל 10 דקות ופורס רק אם הענף השתנה.
# "עלה לאוויר" = דחיפה לענף live. יומן: repos/deploy.log. SHA אחרון שנפרס: repos/live.sha
set -e
cd "$HOME"
REPO="GuySho1/zigzag-site"; BR="live"
SHA=$(git ls-remote --heads "https://github.com/$REPO.git" "$BR" 2>/dev/null | cut -f1)
if [ -z "$SHA" ]; then
  SHA=$(curl -fsSL -H 'Accept: application/vnd.github.sha' "https://api.github.com/repos/$REPO/commits/$BR" 2>/dev/null || true)
fi
[ -z "$SHA" ] && exit 0
LAST=$(cat "$HOME/repos/live.sha" 2>/dev/null || true)
[ "$SHA" = "$LAST" ] && exit 0

TS=$(date +%Y%m%d-%H%M)
TGZ="$HOME/repos/zigzag-site-live.tgz"
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BR.tar.gz" -o "$TGZ"
mkdir -p "$HOME/repos/backups"
tar -czf "$HOME/repos/backups/public_html_$TS.tgz" -C "$HOME/public_html" --exclude='*.mp4' --exclude='art' . 2>/dev/null || true
tar -xzf "$TGZ" -C "$HOME/public_html" --strip-components=2 "zigzag-site-$BR/site"
tar -xzOf "$TGZ" "zigzag-site-$BR/deploy/htaccess-live" > "$HOME/public_html/.htaccess"
echo "$SHA" > "$HOME/repos/live.sha"
echo "LIVE $(date) sha=${SHA:0:10} backup=public_html_$TS.tgz" >> "$HOME/repos/deploy.log"
# שומרים רק 20 גיבויים אחרונים
ls -1t "$HOME/repos/backups"/public_html_*.tgz 2>/dev/null | tail -n +21 | xargs -r rm -f
