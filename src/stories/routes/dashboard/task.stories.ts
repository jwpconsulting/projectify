import type { Meta, StoryObj } from "@storybook/svelte";

import { task } from "$lib/storybook";
import Task from "$routes/(platform)/dashboard/task/[taskUuid]/+page.svelte";

const meta: Meta<Task> = {
    component: Task,
    args: { data: { task } },
};
export default meta;

type Story = StoryObj<Task>;

export const Default: Story = {};
