#!/bin/bash

set -e

./scripts/clean.sh

python3 -m venv .

./bin/pip install wheel zc.buildout
./bin/buildout -c localhost.cfg
