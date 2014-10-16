#!/bin/bash

# Fail on first error
set -e

# Run tests first; if any of the tests fail do not install
./run_tests.sh

sudo python setup.py install
