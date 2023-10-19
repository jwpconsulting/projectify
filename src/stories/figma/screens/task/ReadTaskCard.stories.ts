import type { Meta, StoryObj } from "@storybook/svelte";

import ReadTaskCard from "$lib/figma/screens/task/ReadTaskCard.svelte";
import { task, workspaceBoardSection } from "$lib/storybook";

const meta: Meta<ReadTaskCard> = {
    component: ReadTaskCard,
    argTypes: {},
    args: { task, workspaceBoardSection },
};
export default meta;

type Story = StoryObj<ReadTaskCard>;

export const Default: Story = {};
