import type { Meta, StoryObj } from "@storybook/svelte";

import { labels } from "$lib/storybook";

import Label from "$lib/figma/buttons/Label.svelte";

const meta: Meta<Label> = {
    component: Label,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Label>;

export const Default: Story = {
    args: {
        label: labels[0],
    },
};

export const Apply: Story = {
    args: {
        label: labels[labels.length - 1],
    },
};
