// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import TeamMember from "$lib/figma/cards/task-card/TeamMember.svelte";
import { task } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TeamMember> = {
    component: TeamMember,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TeamMember>;

export const Assignee: Story = {
    args: {
        task,
    },
};

export const NoAssignee: Story = {
    args: {
        task: {
            ...task,
            assignee: undefined,
        },
    },
};
