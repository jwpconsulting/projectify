// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import SubTaskProgress from "$lib/figma/cards/task-card/SubTaskProgress.svelte";
import { task } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<SubTaskProgress> = {
    component: SubTaskProgress,
    argTypes: {},
};
export default meta;

type Story = StoryObj<SubTaskProgress>;

export const Default: Story = {
    args: {
        task,
    },
};
