#!/usr/bin/env bash

cd "$(dirname "$0")"

PYTHONPATH=src python3 -m unittest discover -s tests
