#!/bin/sh
# Packs firmware/servo_tool as an App Lab app zip for the guide's download link:
# site/public/downloads/servo_tool.zip (App Lab: + next to Apps > Import or install an App).
set -e
cd "$(dirname "$0")/../firmware"
out=../site/public/downloads/servo_tool.zip
mkdir -p ../site/public/downloads
rm -f "$out"
zip -qrX "$out" servo_tool -x 'servo_tool/data/*' '*.DS_Store'
echo "wrote $(cd ../site/public/downloads && pwd)/servo_tool.zip"
