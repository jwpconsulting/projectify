import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
import { workspaceUser } from "$lib/storybook";

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
