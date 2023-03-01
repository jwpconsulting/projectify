#!/bin/sh
set -e
path=$1
component=$2
cat <<EOF > "src/lib/$path/$component.svelte"
<script lang="ts">
</script>

Hello, World
EOF
cat <<EOF > "src/stories/$path/$component.stories.ts"
import type { Meta, StoryObj } from "@storybook/svelte";

import $component from "\$lib/$path/$component.svelte";

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
