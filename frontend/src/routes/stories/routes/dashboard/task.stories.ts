// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import { task } from "$lib-stories/storybook";
import Task from "$routes/(platform)/dashboard/task/[taskUuid]/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Task> = {
    component: Task,
    args: { data: { task } },
};
export default meta;

type Story = StoryObj<Task>;

export const Default: Story = {};
