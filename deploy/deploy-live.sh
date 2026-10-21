#!/bin/bash
# ז.ג דיגיטל: עלייה לאוויר. מזיז את הוורדפרס לארכיון ומעלה את האתר החדש לשורש.
set -e
cd "$HOME"
TS=$(date +%Y%m%d-%H%M)
TGZ="$HOME/repos/zigzag-site-main.tgz"
curl -fsSL "https://github.com/GuySho1/zigzag-site/archive/refs/heads/main.tar.gz" -o "$TGZ"
# 1) ארכיון הוורדפרס מחוץ לשורש האתר
mkdir -p "$HOME/_archive_wp_$TS"
shopt -s dotglob
for f in "$HOME"/public_html/*; do
  b=$(basename "$f")
  case "$b" in new|.well-known|cgi-bin) ;; *) mv "$f" "$HOME/_archive_wp_$TS/";; esac
done
shopt -u dotglob
# 2) האתר החדש לשורש
tar -xzf "$TGZ" -C "$HOME/public_html" --strip-components=2 "zigzag-site-main/site"
tar -xzOf "$TGZ" "zigzag-site-main/deploy/htaccess-live" > "$HOME/public_html/.htaccess"
rm -rf "$HOME/public_html/new"
echo "LIVE $(date) archive=_archive_wp_$TS" >> "$HOME/repos/deploy.log"
