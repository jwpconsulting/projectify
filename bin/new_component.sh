#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
# Create a new Svelte component
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
set -e
path=$1
component=$2
component_file="lib/$path/$component.svelte"
full_component_file="src/$component_file"
stories_file="src/stories/$path/$component.stories.ts"

mkdir -p $(dirname "$full_component_file")

if test ! -e "$full_component_file"
then
    cat <<EOF > "$full_component_file"
<script lang="ts">
</script>

Hello, World
EOF
fi

mkdir -p $(dirname "$stories_file")

if test ! -e "$stories_file"
then
    mkdir -p "$(dirname $stories_file)"
    cat <<EOF > "$stories_file"
import type { Meta, StoryObj } from "@storybook/svelte";

import $component from "\$$component_file";

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
