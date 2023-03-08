import type { Meta, StoryObj } from "@storybook/svelte";

import TaskScreenMobile from "$lib/figma/screens/task/TaskScreenMobile.svelte";

import { task, mobileParameters } from "$lib/storybook";

const meta: Meta<TaskScreenMobile> = {
    component: TaskScreenMobile,
    parameters: {
        ...mobileParameters,
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<TaskScreenMobile>;

export const Task: Story = {
    args: {
        task,
    },
};

export const Updates: Story = {
    args: {
        task,
        state: "updates",
    },
};
