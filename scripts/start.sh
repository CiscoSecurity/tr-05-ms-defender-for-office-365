#! /usr/bin/env sh
if test -z "${DEBUG}"; then
  echo "[start.sh] DEBUG MODE OFF" >>/var/log/messages
else
  {
    echo "[start.sh] DEBUG MODE ON"
    echo "[start.sh] ............."
    echo "[start.sh] Integration Module: $(jq -r .NAME /app/container_settings.json)"
    echo "[start.sh]            Version: $(jq -r .VERSION /app/container_settings.json)"
    echo "[start.sh] Starting supervisord ..."
    echo "[start.sh] ............."
  } >>/var/log/messages
fi
set -e
exec /usr/bin/supervisord -c /supervisord.ini
