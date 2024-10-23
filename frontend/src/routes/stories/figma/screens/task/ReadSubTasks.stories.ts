// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import ReadSubTasks from "$lib/figma/screens/task/ReadSubTasks.svelte";
import { subTask } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<ReadSubTasks> = {
    component: ReadSubTasks,
};
export default meta;

type Story = StoryObj<ReadSubTasks>;

export const Default: Story = {
    args: {
        subTasks: [subTask, subTask],
    },
};

export const Empty: Story = {
    args: {
        subTasks: [],
    },
};
