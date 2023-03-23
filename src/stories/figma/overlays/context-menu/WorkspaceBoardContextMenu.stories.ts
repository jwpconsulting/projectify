import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceBoardContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardContextMenu.svelte";

import { workspaceBoard } from "$lib/storybook";

const meta: Meta<WorkspaceBoardContextMenu> = {
    component: WorkspaceBoardContextMenu,
    argTypes: {},
    args: { workspaceBoard },
};
export default meta;

type Story = StoryObj<WorkspaceBoardContextMenu>;

export const Default: Story = {};
