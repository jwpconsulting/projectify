import type { Meta, StoryObj } from "@storybook/svelte";

import Title from "$lib/figma/cards/task-card/Title.svelte";

import { task } from "$lib/storybook";

const meta: Meta<Title> = {
    component: Title,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Title>;

export const Default: Story = {
    args: {
        task,
    },
};
