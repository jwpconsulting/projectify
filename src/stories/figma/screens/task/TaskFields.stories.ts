import type { Meta, StoryObj } from "@storybook/svelte";

import TaskFields from "$lib/figma/screens/task/TaskFields.svelte";

const meta: Meta<TaskFields> = {
    component: TaskFields,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TaskFields>;

export const Default: Story = {};
