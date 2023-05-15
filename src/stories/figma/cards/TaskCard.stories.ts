import type { Meta, StoryObj } from "@storybook/svelte";

import TaskCard from "$lib/figma/cards/TaskCard.svelte";

import { moveTaskModule, mobileParameters, task } from "$lib/storybook";

const meta: Meta<TaskCard> = {
    component: TaskCard,
    argTypes: {},
    args: {
        task,
        moveTaskModule,
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
