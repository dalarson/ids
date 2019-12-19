#!/usr/bin/env bash
set -euo pipefail

rm -f cookies

curl -s -c cookies -XPOST -F "user_id=$((RANDOM % 1000))" "http://$1:5000/signin" | w3m -dump -T text/html

echo
cat cookies
echo

curl -s -b cookies "http://$1:5000/home" | w3m -dump -T text/html

rm -f cookies
