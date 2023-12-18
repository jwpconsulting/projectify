import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
import { workspaceUser } from "$lib/storybook";

const meta: Meta<TaskUser> = {
    component: TaskUser,
    args: {
        workspaceUser,
        onInteract: console.log,
    },
};
export default meta;

type Story = StoryObj<TaskUser>;

export const Default: Story = {};

export const NoUser: Story = { args: { workspaceUser: undefined } };

export const NoAction: Story = { args: { onInteract: undefined } };
