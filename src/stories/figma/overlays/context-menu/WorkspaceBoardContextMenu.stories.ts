import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceBoard } from "$lib/storybook";

import WorkspaceBoardContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardContextMenu.svelte";

const meta: Meta<WorkspaceBoardContextMenu> = {
    component: WorkspaceBoardContextMenu,
    argTypes: {},
    args: { workspaceBoard },
};
export default meta;

type Story = StoryObj<WorkspaceBoardContextMenu>;

export const Default: Story = {};
