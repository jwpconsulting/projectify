import type { Meta, StoryObj } from "@storybook/svelte";

import ReadSubTasks from "$lib/figma/screens/task/ReadSubTasks.svelte";
import { subTask } from "$lib/storybook";

const meta: Meta<ReadSubTasks> = {
    component: ReadSubTasks,
};
export default meta;

type Story = StoryObj<ReadSubTasks>;

export const Default: Story = {
    args: {
        subTasks: [subTask, subTask],
    },
};

export const Empty: Story = {
    args: {
        subTasks: [],
    },
};
