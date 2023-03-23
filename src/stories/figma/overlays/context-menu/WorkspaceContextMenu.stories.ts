import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceContextMenu from "$lib/figma/overlays/context-menu/WorkspaceContextMenu.svelte";

import { workspaceSearchModule } from "$lib/storybook";

const meta: Meta<WorkspaceContextMenu> = {
    component: WorkspaceContextMenu,
    argTypes: {},
    args: {
        workspaceSearchModule,
    },
};
export default meta;

type Story = StoryObj<WorkspaceContextMenu>;

export const Default: Story = {};
