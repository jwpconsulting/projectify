#!/bin/sh
set -e
poetry run pytest \
    -x \
    --pdb \
    --ds=projectify.settings.test \
    --dc=TestRedis \
    "workspace/test/test_consumers.py"
