#!/bin/bash

set -e

./scripts/clean.sh

python3 -m venv .

./bin/pip install wheel zc.buildout
./bin/buildout -c localhost.cfg

if ! which npm &> /dev/null; then
    sudo apt-get install npm
fi

npm --prefix . --no-save install \
    ./devsrc/treibstoff