#!/bin/sh
# usage: shot.sh <url> <out.png> <width> <height>
S=/private/tmp/claude-501/-Users-nicolel-Library-Mobile-Documents-iCloud-md-obsidian-Documents/ee9fd929-dba4-4be3-bf81-eb8303fcf7e0/scratchpad
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
rm -f "$2"
"$CH" --headless=new --user-data-dir=$S/hl-profile --no-first-run --disable-gpu --hide-scrollbars --window-size=$3,$4 --force-device-scale-factor=2 --virtual-time-budget=10000 --screenshot="$2" "$1" >/dev/null 2>&1 &
P=$!; i=0; while [ $i -lt 45 ] && [ ! -s "$2" ]; do sleep 1; i=$((i+1)); done; sleep 1; kill $P 2>/dev/null; ls -la "$2"
