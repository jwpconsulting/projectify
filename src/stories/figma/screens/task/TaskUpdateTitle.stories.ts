import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateTitle from "$lib/figma/screens/task/TaskUpdateTitle.svelte";

const meta: Meta<TaskUpdateTitle> = {
    component: TaskUpdateTitle,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TaskUpdateTitle>;

export const Default: Story = {};
