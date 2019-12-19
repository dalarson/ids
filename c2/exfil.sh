#!/usr/bin/env bash

for i in $(seq 1 25); do
    echo "$i" | tee /user_id
    curl -s -k https://10.0.0.3:5000/ >/dev/null
done
