import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters, task } from "$lib/storybook";
import Update from "$routes/(platform)/dashboard/task/[taskUuid]/update/+page.svelte";

const meta: Meta<Update> = {
    component: Update,
    args: {
        data: { task },
    },
};
export default meta;

type Story = StoryObj<Update>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
