#!/bin/bash
# ז.ג דיגיטל: עדכון שוטף של האתר החי מהענף main בגיטהאב (בלי לגעת בארכיון או ב-.well-known).
set -e
cd "$HOME"
TS=$(date +%Y%m%d-%H%M)
TGZ="$HOME/repos/zigzag-site-main.tgz"
curl -fsSL "https://github.com/GuySho1/zigzag-site/archive/refs/heads/main.tar.gz" -o "$TGZ"
# גיבוי קטן של המצב הנוכחי (HTML בלבד, קל)
mkdir -p "$HOME/repos/backups"
tar -czf "$HOME/repos/backups/public_html_$TS.tgz" -C "$HOME/public_html" --exclude='*.mp4' --exclude='art' . 2>/dev/null || true
# פריסה על השורש
tar -xzf "$TGZ" -C "$HOME/public_html" --strip-components=2 "zigzag-site-main/site"
tar -xzOf "$TGZ" "zigzag-site-main/deploy/htaccess-live" > "$HOME/public_html/.htaccess"
echo "UPDATE $(date) backup=public_html_$TS.tgz" >> "$HOME/repos/deploy.log"
