import type { Meta, StoryObj } from "@storybook/svelte";

import Labels from "$lib/figma/cards/task-card/Labels.svelte";
import { task } from "$lib/storybook";

const meta: Meta<Labels> = {
    component: Labels,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Labels>;

export const Default: Story = {
    args: {
        task,
    },
};
