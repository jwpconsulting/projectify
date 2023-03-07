import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateCard from "$lib/figma/screens/task/TaskUpdateCard.svelte";

import { task, mobileParameters } from "$lib/storybook";

const meta: Meta<TaskUpdateCard> = {
    component: TaskUpdateCard,
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<TaskUpdateCard>;

export const Default: Story = {
    args: {
        task,
    },
};

export const Mobile: Story = {
    args: {
        task,
    },
    parameters: {
        ...mobileParameters,
    },
};
