import type { Meta, StoryObj } from "@storybook/svelte";

import TaskScreenDesktop from "$lib/figma/screens/task/TaskScreenDesktop.svelte";

import { task } from "$lib/storybook";

const meta: Meta<TaskScreenDesktop> = {
    component: TaskScreenDesktop,
    parameters: {
        layout: "fullscreen",
    },
    args: {
        taskOrNewTask: {
            kind: "task",
            task,
        },
    },
};
export default meta;

type Story = StoryObj<TaskScreenDesktop>;

export const Default: Story = {};
