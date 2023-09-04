import type { Meta, StoryObj } from "@storybook/svelte";

import { task, workspaceBoardSection } from "$lib/storybook";

import ReadTaskCard from "$lib/figma/screens/task/ReadTaskCard.svelte";

const meta: Meta<ReadTaskCard> = {
    component: ReadTaskCard,
    argTypes: {},
    args: { task, workspaceBoardSection },
};
export default meta;

type Story = StoryObj<ReadTaskCard>;

export const Default: Story = {};
