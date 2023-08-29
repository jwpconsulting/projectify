import type { Meta, StoryObj } from "@storybook/svelte";

import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";

const meta: Meta<TaskTitle> = {
    component: TaskTitle,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TaskTitle>;

export const Default: Story = {};
