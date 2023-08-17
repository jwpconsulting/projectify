import type { Meta, StoryObj } from "@storybook/svelte";

import { createTaskModule } from "$lib/storybook";

import CreateTaskFormFields from "$lib/figma/screens/task/CreateTaskFormFields.svelte";

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
