#!/bin/sh
set -eu

REMOTE_USER="${CONTACT_BRIDGE_REMOTE_USER:-admin}"
REMOTE_HOST="${CONTACT_BRIDGE_REMOTE_HOST:-47.236.185.172}"
REMOTE_PORT="${CONTACT_BRIDGE_REMOTE_PORT:-15678}"
LOCAL_TARGET="${CONTACT_BRIDGE_LOCAL_TARGET:-m8a-n8n:5678}"
KEY_SOURCE="${CONTACT_BRIDGE_SSH_KEY:-/run/secrets/woodmachinerynetwork_deploy}"
KEY_RUNTIME="/tmp/woodmachinerynetwork_deploy"

if [ ! -f "$KEY_SOURCE" ]; then
  echo "missing ssh key: $KEY_SOURCE" >&2
  exit 1
fi

cp "$KEY_SOURCE" "$KEY_RUNTIME"
chmod 600 "$KEY_RUNTIME"

echo "Starting M8A contact bridge tunnel: ${REMOTE_HOST}:${REMOTE_PORT} -> ${LOCAL_TARGET}"
exec ssh \
  -i "$KEY_RUNTIME" \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes \
  -o StrictHostKeyChecking=accept-new \
  -N -R "${REMOTE_PORT}:${LOCAL_TARGET}" "${REMOTE_USER}@${REMOTE_HOST}"
