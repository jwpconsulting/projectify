import type { Meta, StoryObj } from "@storybook/svelte";

import Task from "$lib/components/dashboard/task/Task.svelte";

const meta: Meta<Task> = {
    component: Task,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Task>;

export const Default: Story = {};
