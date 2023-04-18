import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
import { workspaceUser } from "$lib/storybook";

const meta: Meta<TaskUpdateUser> = {
    component: TaskUpdateUser,
    args: {
        workspaceUser,
        action: console.log,
    },
};
export default meta;

type Story = StoryObj<TaskUpdateUser>;

export const Default: Story = {};
