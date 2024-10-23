// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
import { teamMember } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TaskUser> = {
    component: TaskUser,
    args: {
        teamMember,
        onInteract: console.log,
    },
};
export default meta;

type Story = StoryObj<TaskUser>;

export const Default: Story = {};

export const NoUser: Story = { args: { teamMember: undefined } };

export const NoAction: Story = { args: { onInteract: undefined } };
