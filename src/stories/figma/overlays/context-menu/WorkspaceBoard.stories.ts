import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceBoard from "$lib/figma/overlays/context-menu/WorkspaceBoard.svelte";
import { workspaceBoard } from "$lib/storybook";

const meta: Meta<WorkspaceBoard> = {
    component: WorkspaceBoard,
    argTypes: {},
    args: { workspaceBoard },
};
export default meta;

type Story = StoryObj<WorkspaceBoard>;

export const Default: Story = {};
