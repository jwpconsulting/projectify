import type { Meta, StoryObj } from "@storybook/svelte";

import {
    mobileParameters,
    task,
    taskModule,
    workspaceBoardSection,
} from "$lib/storybook";

import UpdateTaskCard from "$lib/figma/screens/task/UpdateTaskCard.svelte";

const meta: Meta<UpdateTaskCard> = {
    component: UpdateTaskCard,
    args: {
        task,
        taskModule,
        workspaceBoardSection,
    },
};
export default meta;

type Story = StoryObj<UpdateTaskCard>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
