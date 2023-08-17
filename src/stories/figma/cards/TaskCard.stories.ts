import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters, task } from "$lib/storybook";

import TaskCard from "$lib/figma/cards/TaskCard.svelte";

const meta: Meta<TaskCard> = {
    component: TaskCard,
    argTypes: {},
    args: {
        task,
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<TaskCard>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
