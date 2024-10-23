// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Labels from "$lib/figma/cards/task-card/Labels.svelte";
import { task } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Labels> = {
    component: Labels,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Labels>;

export const Default: Story = {
    args: {
        task,
    },
};
