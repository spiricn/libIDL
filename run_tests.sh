#!/bin/bash

export PYTHONPATH=`pwd`:$PYTHONPATH

main() {
	python -m unittest discover -s `pwd`/test -p "*.py"
}

main "$@"
