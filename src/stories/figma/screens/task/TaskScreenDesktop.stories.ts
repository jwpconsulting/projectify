import type { Meta, StoryObj } from "@storybook/svelte";

import TaskScreenDesktop from "$lib/figma/screens/task/TaskScreenDesktop.svelte";

import { task } from "$lib/storybook";

const meta: Meta<TaskScreenDesktop> = {
    component: TaskScreenDesktop,
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<TaskScreenDesktop>;

export const Default: Story = {
    args: {
        task,
    },
};
