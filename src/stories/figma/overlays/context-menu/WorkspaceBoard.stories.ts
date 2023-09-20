import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceBoard } from "$lib/storybook";

import WorkspaceBoard from "$lib/figma/overlays/context-menu/WorkspaceBoard.svelte";

const meta: Meta<WorkspaceBoard> = {
    component: WorkspaceBoard,
    argTypes: {},
    args: { workspaceBoard },
};
export default meta;

type Story = StoryObj<WorkspaceBoard>;

export const Default: Story = {};
