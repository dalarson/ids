#!/usr/bin/env bash
set -euxo pipefail

tshark -l -i ws-eth0 -f "tcp port 5000" -Y "ssl.handshake.type == 1" -o http.ssl.port:5000 -T fields -e ssl.handshake.random_bytes 2>/dev/null | python3 exfil.py
