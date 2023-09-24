import type { Meta, StoryObj } from "@storybook/svelte";

import { breadCrumbWorkspaceBoardSection } from "$lib/storybook";

import CreateTaskCard from "$lib/figma/screens/task/CreateTaskCard.svelte";

const meta: Meta<CreateTaskCard> = {
    component: CreateTaskCard,
    argTypes: {},
    args: {
        workspaceBoardSection: breadCrumbWorkspaceBoardSection,
    },
};
export default meta;

type Story = StoryObj<CreateTaskCard>;

export const Default: Story = {};
