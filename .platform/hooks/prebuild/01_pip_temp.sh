#!/bin/bash
set -e

echo "=== Configuring pip installation storage ==="

mkdir -p /var/app/pip-temp
mkdir -p /var/app/pip-cache

chmod 777 /var/app/pip-temp
chmod 777 /var/app/pip-cache

export TMPDIR=/var/app/pip-temp
export TEMP=/var/app/pip-temp
export TMP=/var/app/pip-temp

PIP_BIN=$(find /var/app/venv -type f -path "*/bin/pip" | head -1)

if [ -z "$PIP_BIN" ]; then
    echo "ERROR: pip executable not found"
    exit 1
fi

echo "Found pip at: $PIP_BIN"

mv "$PIP_BIN" "${PIP_BIN}-real"

cat > "$PIP_BIN" <<'EOF'
#!/bin/bash

export TMPDIR=/var/app/pip-temp
export TEMP=/var/app/pip-temp
export TMP=/var/app/pip-temp
export PIP_CACHE_DIR=/var/app/pip-cache

exec "$(dirname "$0")/pip-real" --no-cache-dir "$@"
EOF

chmod +x "$PIP_BIN"

echo "=== Pip storage configuration completed ==="

df -h