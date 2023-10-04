import type { Meta, StoryObj } from "@storybook/svelte";

import { subTask } from "$lib/storybook";

import SubTask from "$lib/figma/buttons/SubTask.svelte";

const meta: Meta<SubTask> = {
    component: SubTask,
};
export default meta;

type Story = StoryObj<SubTask>;

export const Default: Story = {
    args: {
        subTask,
    },
};
