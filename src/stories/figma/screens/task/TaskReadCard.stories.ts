import type { Meta, StoryObj } from "@storybook/svelte";

import { task } from "$lib/storybook";

import TaskReadCard from "$lib/figma/screens/task/TaskReadCard.svelte";

const meta: Meta<TaskReadCard> = {
    component: TaskReadCard,
    argTypes: {},
    args: { task },
};
export default meta;

type Story = StoryObj<TaskReadCard>;

export const Default: Story = {};
