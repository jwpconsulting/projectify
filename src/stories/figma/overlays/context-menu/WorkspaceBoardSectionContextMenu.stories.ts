import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceBoardSection } from "$lib/storybook";

import WorkspaceBoardSectionContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardSectionContextMenu.svelte";

const meta: Meta<WorkspaceBoardSectionContextMenu> = {
    component: WorkspaceBoardSectionContextMenu,
    argTypes: {},
    args: { workspaceBoardSection },
};
export default meta;

type Story = StoryObj<WorkspaceBoardSectionContextMenu>;

export const Default: Story = {};
