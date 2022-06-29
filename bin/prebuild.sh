#!/bin/bash
# https://github.com/apollographql/apollo-client/issues/8218
sed -i.bak -f bin/prebuild.sed node_modules/@apollo/client/package.json
