import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import WorkspaceContextMenu from "$lib/figma/overlays/context-menu/WorkspaceContextMenu.svelte";

const meta: Meta<WorkspaceContextMenu> = {
    component: WorkspaceContextMenu,
    argTypes: {},
    args: { workspaces: [workspace] },
};
export default meta;

type Story = StoryObj<WorkspaceContextMenu>;

export const Default: Story = {};
