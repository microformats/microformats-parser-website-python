#!/bin/bash
SCRIPT=$(readlink -m "$0")

cd "$(dirname "$SCRIPT")"
source venv/bin/activate

if [ -n "$(pip list -o | grep -e mf2py -e mf2util)" ]; then
    echo "upgrading mf2py"
    pip install --upgrade mf2py mf2util
    restart mf2
fi
