#!/bin/bash
#
# Clean development environment.

set -e

to_remove=(
    .installed.cfg .mr.developer.cfg bin buildout.cfg develop-eggs
    dist include lib64 lib parts pyvenv.cfg share
)

for item in "${to_remove[@]}"; do
    if [ -e "$item" ]; then
        rm -r "$item"
    fi
done
