import type { Meta, StoryObj } from "@storybook/svelte";

import { createTaskModule } from "$lib/storybook";

import TaskCreateCard from "$lib/figma/screens/task/TaskCreateCard.svelte";

const meta: Meta<TaskCreateCard> = {
    component: TaskCreateCard,
    argTypes: {},
    args: {
        createTaskModule,
    },
};
export default meta;

type Story = StoryObj<TaskCreateCard>;

export const Default: Story = {};
