#!/bin/sh
set -e
path=$1
component=$2
component_file="lib/$path/$component.svelte"
full_component_file="src/$component_file"
stories_file="src/stories/$path/$component.stories.ts"

if test ! -e "$component_file"
then
    cat <<EOF > "$component_file"
<script lang="ts">
</script>

Hello, World
EOF
fi

if test ! -e "$stories_file"
then
    mkdir -p "$(dirname $stories_file)"
    cat <<EOF > "$stories_file"
import type { Meta, StoryObj } from "@storybook/svelte";

import $component from "\$$full_component_file";

const meta: Meta<$component> = {
    component: $component,
    argTypes: {
    },
};
export default meta;

type Story = StoryObj<$component>;

export const Default: Story = {
};
EOF
fi
