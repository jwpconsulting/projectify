import type { Meta, StoryObj } from "@storybook/svelte";

import { task } from "$lib/storybook";

import SubTaskProgress from "$lib/figma/buttons/SubTaskProgress.svelte";

const meta: Meta<SubTaskProgress> = {
    component: SubTaskProgress,
    argTypes: {},
};
export default meta;

type Story = StoryObj<SubTaskProgress>;

export const Default: Story = {
    args: {
        task,
    },
};
