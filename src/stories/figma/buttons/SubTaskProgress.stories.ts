import type { Meta, StoryObj } from "@storybook/svelte";

import SubTaskProgress from "$lib/figma/buttons/SubTaskProgress.svelte";

import { task } from "$lib/storybook";

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
