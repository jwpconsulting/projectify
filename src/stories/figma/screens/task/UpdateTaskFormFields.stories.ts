import type { Meta, StoryObj } from "@storybook/svelte";

import { task } from "$lib/storybook";

import UpdateTaskFormFields from "$lib/figma/screens/task/UpdateTaskFormFields.svelte";


const meta: Meta<UpdateTaskFormFields> = {
    component: UpdateTaskFormFields,
    args: { task },
};
export default meta;

type Story = StoryObj<UpdateTaskFormFields>;

export const Default: Story = {};
