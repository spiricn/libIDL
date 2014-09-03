#!/bin/bash

export PYTHONPATH=`pwd`:$PYTHONPATH

pushd ./test

python Basic.py

popd

