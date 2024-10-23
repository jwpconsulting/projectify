// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Task from "$lib/figma/overlays/context-menu/Task.svelte";
import { task } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Task> = {
    component: Task,
    argTypes: {},
    args: { task },
};
export default meta;

type Story = StoryObj<Task>;

export const Default: Story = {};
