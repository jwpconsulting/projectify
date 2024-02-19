#!/bin/bash
# Formerly used for
# https://github.com/apollographql/apollo-client/issues/8218
# Now used to patch types export in svelte-boring-avatar
FILE=node_modules/svelte-boring-avatars/package.json
if grep '"types": "./dist/ts/index.ts"' "$FILE" >/dev/null
then
    echo "Skip running bin/prebuild.sed on $FILE"
else
    echo "Running bin/prebuild.sed on $FILE"
    sed -i.bak -f bin/prebuild.sed "$FILE"
fi
