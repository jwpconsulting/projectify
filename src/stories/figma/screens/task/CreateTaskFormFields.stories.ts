import type { Meta, StoryObj } from "@storybook/svelte";

import CreateTaskFormFields from "$lib/figma/screens/task/CreateTaskFormFields.svelte";

import { createTaskModule } from "$lib/storybook";

const meta: Meta<CreateTaskFormFields> = {
    component: CreateTaskFormFields,
    argTypes: {},
    args: {
        createTaskModule,
    },
};
export default meta;

type Story = StoryObj<CreateTaskFormFields>;

export const Default: Story = {};
