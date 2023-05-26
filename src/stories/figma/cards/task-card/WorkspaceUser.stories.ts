import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceUser from "$lib/figma/cards/task-card/WorkspaceUser.svelte";

import { task } from "$lib/storybook";

const meta: Meta<WorkspaceUser> = {
    component: WorkspaceUser,
    argTypes: {},
};
export default meta;

type Story = StoryObj<WorkspaceUser>;

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
