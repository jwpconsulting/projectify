import type { Meta, StoryObj } from "@storybook/svelte";

import FloatingActionButton from "$lib/figma/buttons/FloatingActionButton.svelte";

const meta: Meta<FloatingActionButton> = {
    component: FloatingActionButton,
    argTypes: { disabled: { control: "boolean" } },
    args: {
        action: console.log,
        disabled: false,
    },
};
export default meta;

type Story = StoryObj<FloatingActionButton>;

export const Plus: Story = {
    args: {
        icon: "plus",
    },
};

export const Close: Story = {
    args: {
        icon: "close",
    },
};
