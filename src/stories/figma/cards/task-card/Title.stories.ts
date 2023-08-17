import type { Meta, StoryObj } from "@storybook/svelte";

import { task } from "$lib/storybook";

import Title from "$lib/figma/cards/task-card/Title.svelte";

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
