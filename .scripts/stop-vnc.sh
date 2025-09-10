#!/usr/bin/env bash
set -euo pipefail
pkill -f websockify || true
pkill -x x11vnc   || true
pkill -x fluxbox  || true
pkill -x Xvfb     || true
echo "Stopped Xvfb/fluxbox/x11vnc/websockify."
