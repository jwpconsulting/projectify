import type { Meta, StoryObj } from "@storybook/svelte";

import SubTask from "$lib/figma/buttons/SubTask.svelte";

import { subTask } from "$lib/storybook";

const meta: Meta<SubTask> = {
    component: SubTask,
    argTypes: {},
};
export default meta;

type Story = StoryObj<SubTask>;

export const Default: Story = {
    args: {
        subTask,
        state: "normal",
    },
};

export const Edit: Story = {
    args: {
        subTask,
        state: "edit",
    },
};
