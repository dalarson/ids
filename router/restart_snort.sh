#!/usr/bin/env bash
set -euxo pipefail

pkill snort || true
sleep 1

snort -i br0 -D -A fast -c /etc/snort/snort.conf
