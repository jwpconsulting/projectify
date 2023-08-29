import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUser } from "$lib/storybook";

import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";

const meta: Meta<TaskUser> = {
    component: TaskUser,
    args: {
        workspaceUser,
        action: console.log,
    },
};
export default meta;

type Story = StoryObj<TaskUser>;

export const Default: Story = {};
