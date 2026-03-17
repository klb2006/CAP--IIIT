#!/bin/bash
set -e

# Set up environment
export PYTHONUNBUFFERED=1

# Make sure to include all possible site-packages locations in PYTHONPATH
export PYTHONPATH="/usr/local/lib/python3.11/dist-packages:/usr/lib/python3/dist-packages:/opt/render/project/src/backend:$PYTHONPATH"

cd /opt/render/project/src/backend

# Execute the launcher
exec python3 run.py
