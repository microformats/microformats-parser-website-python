#!/bin/bash
set -euo pipefail
cd "$(cd "$(dirname "$0")" && pwd)"

BUILDPACK_SCRIPT=$(curl -sf https://raw.githubusercontent.com/heroku/heroku-buildpack-python/main/lib/python_version.sh)
if [ -z "$BUILDPACK_SCRIPT" ]; then
    echo "Could not fetch Heroku buildpack Python version info"
    exit 1
fi

NEWEST_MINOR=$(echo "$BUILDPACK_SCRIPT" | grep '^NEWEST_SUPPORTED_PYTHON_3_MINOR_VERSION=' | grep -oE '[0-9]+')
LATEST_PYTHON=$(echo "$BUILDPACK_SCRIPT" | grep "^LATEST_PYTHON_3_${NEWEST_MINOR}=" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')

if [ -z "$LATEST_PYTHON" ]; then
    echo "Could not determine latest Heroku-supported Python version"
    exit 1
fi

CURRENT_PYTHON=$(cat .python-version 2>/dev/null)

if [ "$LATEST_PYTHON" != "$CURRENT_PYTHON" ]; then
    uv python install "$LATEST_PYTHON"
    sed -i "" "s/requires-python = \"==[0-9.]*\"/requires-python = \"==$LATEST_PYTHON\"/" pyproject.toml
    uv python pin "$LATEST_PYTHON"
    rm -f uv.lock
    uv lock
fi

uv sync --quiet

UPDATES=()
while read -r PKG _ LATEST _; do
    if grep -qi "\"${PKG}==" pyproject.toml; then
        UPDATES+=("${PKG}==${LATEST}")
    fi
done < <(uv pip list --outdated --format columns 2>/dev/null | tail -n +3)

if [ "${#UPDATES[@]}" -gt 0 ]; then
    uv add "${UPDATES[@]}"
fi
