#!/bin/bash

set -x

rm ./dist/*
python3.7 setup.py sdist bdist_wheel
twine check dist/*
twine upload -r testpypi dist/*
