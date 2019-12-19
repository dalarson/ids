#!/usr/bin/env bash
set -euxo pipefail

curl -s -b "secret_message=$*" -d user_id=100 -c - 10.0.0.3:5000/signin | grep secret_message | awk '{print $7}'
