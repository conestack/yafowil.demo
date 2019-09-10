#!/bin/sh

rm -r ./lib ./include ./local ./bin ./share
virtualenv -p python3 --clear .
./bin/pip install --upgrade pip setuptools zc.buildout
./bin/buildout -c localhost.cfg
