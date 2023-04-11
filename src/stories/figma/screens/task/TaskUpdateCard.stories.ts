import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";

import { mobileParameters, task } from "$lib/storybook";

const meta: Meta<TaskUpdateCard> = {
    component: TaskUpdateCard,
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

type Story = StoryObj<TaskUpdateCard>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
