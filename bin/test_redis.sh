#!/bin/sh
set -e
pipenv run pytest \
    -x \
    --pdb \
    --ds=projectify.settings.test_redis \
    "workspace/test/test_consumers.py"
