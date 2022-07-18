#!/bin/bash
# https://github.com/apollographql/apollo-client/issues/8218
FILE=node_modules/@apollo/client/package.json
if ! grep exports "$FILE" >/dev/null
then
    echo "bin/prebuild.sed"
    sed -i.bak -f bin/prebuild.sed "$FILE"
fi
