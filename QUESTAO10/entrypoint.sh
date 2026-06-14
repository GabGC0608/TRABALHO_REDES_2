#!/bin/sh
set -e

python -m http.server 8080 &
python ServerWebSocket.py
