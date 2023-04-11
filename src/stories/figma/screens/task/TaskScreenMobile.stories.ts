import type { Meta, StoryObj } from "@storybook/svelte";

import TaskScreenMobile from "$lib/figma/screens/task/TaskScreenMobile.svelte";

import { mobileParameters, task } from "$lib/storybook";

const meta: Meta<TaskScreenMobile> = {
    component: TaskScreenMobile,
    parameters: {
        ...mobileParameters,
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

type Story = StoryObj<TaskScreenMobile>;

export const Task: Story = {};

export const Updates: Story = {
    args: {
        state: "updates",
    },
};
