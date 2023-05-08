import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateDescription from "$lib/figma/screens/task/TaskUpdateDescription.svelte";

const meta: Meta<TaskUpdateDescription> = {
    component: TaskUpdateDescription,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TaskUpdateDescription>;

export const Default: Story = {};
