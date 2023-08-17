import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceBoard } from "$lib/storybook";

import SelectWorkspaceBoard from "$lib/figma/buttons/SelectWorkspaceBoard.svelte";

const meta: Meta<SelectWorkspaceBoard> = {
    component: SelectWorkspaceBoard,
    argTypes: {},
    args: {
        workspaceBoard,
    },
};
export default meta;

type Story = StoryObj<SelectWorkspaceBoard>;

export const Default: Story = {};
