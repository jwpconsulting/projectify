import type { Meta, StoryObj } from "@storybook/svelte";

import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";

const meta: Meta<TaskDescription> = {
    component: TaskDescription,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TaskDescription>;

export const Default: Story = {};
