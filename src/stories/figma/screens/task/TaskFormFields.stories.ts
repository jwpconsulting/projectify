import type { Meta, StoryObj } from "@storybook/svelte";

import TaskFormFields from "$lib/figma/screens/task/TaskFormFields.svelte";

const meta: Meta<TaskFormFields> = {
    component: TaskFormFields,
    argTypes: {},
};
export default meta;

type Story = StoryObj<TaskFormFields>;

export const Default: Story = {};
