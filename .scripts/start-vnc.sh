#!/usr/bin/env bash
set -euo pipefail

export DISPLAY="${DISPLAY:-:0}"
SCREEN_RES="${SCREEN_RES:-1280x800x24}"
RFB_PORT="${RFB_PORT:-5900}"
NOVNC_PORT="${NOVNC_PORT:-6080}"

log() { echo "[$(date +'%H:%M:%S')] $*"; }

# Clean up stale locks (common after abrupt container rebuilds)
if [[ -e "/tmp/.X0-lock" && "$DISPLAY" = ":0" ]]; then
  log "Removing stale /tmp/.X0-lock"
  rm -f /tmp/.X0-lock || true
fi

# 1) Start Xvfb
if ! pgrep -x Xvfb >/dev/null; then
  log "Starting Xvfb on $DISPLAY at ${SCREEN_RES}"
  Xvfb "$DISPLAY" -screen 0 "$SCREEN_RES" >/tmp/xvfb.log 2>&1 &
fi

# Wait for X socket to exist
for i in {1..50}; do
  [[ -S "/tmp/.X11-unix/X${DISPLAY#:}" ]] && break
  sleep 0.1
done
if [[ ! -S "/tmp/.X11-unix/X${DISPLAY#:}" ]]; then
  log "ERROR: X socket not found; Xvfb failed to start"; exit 1
fi

# 2) Start a lightweight WM
if ! pgrep -x fluxbox >/dev/null; then
  log "Starting fluxbox"
  fluxbox >/tmp/fluxbox.log 2>&1 &
fi

# 3) Start x11vnc attached to the ready display
if ! pgrep -x x11vnc >/dev/null; then
  log "Starting x11vnc on :$RFB_PORT"
  x11vnc -display "$DISPLAY" -forever -shared -nopw -rfbport "$RFB_PORT" \
    >/tmp/x11vnc.log 2>&1 &
fi

# Wait for 5900 to listen
for i in {1..100}; do
  if ss -ltn | grep -q ":${RFB_PORT} "; then break; fi
  sleep 0.1
done
if ! ss -ltn | grep -q ":${RFB_PORT} "; then
  log "ERROR: x11vnc did not open port ${RFB_PORT}"; exit 1
fi

# 4) Start noVNC / websockify (keep in foreground)
log "Starting noVNC on 0.0.0.0:${NOVNC_PORT} -> localhost:${RFB_PORT}"
exec websockify --web=/usr/share/novnc/ 0.0.0.0:"$NOVNC_PORT" localhost:"$RFB_PORT"
