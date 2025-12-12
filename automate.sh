#!/bin/bash

# Activate the virtual environment
pipenv shell

# Execute the test suite
pytest -q
rc=$?

if [ $rc -eq 0 ]; then
  echo "Tests passed"
  exit 0
else
  echo "Tests failed (exit code $rc)"
  exit 1
fi
