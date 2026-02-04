#!/bin/sh
set -e

USER_ID=${LOCAL_USER_ID:-1000}
usermod -u $USER_ID  nonroot
chown -R nonroot ./
chown -R nonroot /home/nonroot

exec /usr/local/bin/pysu nonroot "$@"