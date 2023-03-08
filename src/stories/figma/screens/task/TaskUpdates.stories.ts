import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdates from "$lib/figma/screens/task/TaskUpdates.svelte";

const meta: Meta<TaskUpdates> = {
    component: TaskUpdates,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TaskUpdates>;

export const Default: Story = {};
