#!/bin/bash
ruff format framex
python ./tests/all.py

poetry version patch
poetry build
poetry publish