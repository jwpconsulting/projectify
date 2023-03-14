import type { Meta, StoryObj } from "@storybook/svelte";

import Chevrons from "$lib/figma/cards/task-card/Chevrons.svelte";

import { task } from "$lib/storybook";

const meta: Meta<Chevrons> = {
    component: Chevrons,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Chevrons>;

export const Default: Story = {
    args: {
        task,
    },
};
