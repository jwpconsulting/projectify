import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateUser from "$lib/figma/screens/task/TaskUpdateUser.svelte";
import { mobileParameters, user1 } from "$lib/storybook";

const meta: Meta<TaskUpdateUser> = {
    component: TaskUpdateUser,
};
export default meta;

type Story = StoryObj<TaskUpdateUser>;

export const Default: Story = {
    args: {
        user: user1,
    },
};
