import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceBoardSectionContextMenu from "$lib/figma/overlays/context-menu/WorkspaceBoardSectionContextMenu.svelte";

import {
    workspaceBoardSection,
    workspaceBoardSectionModule,
} from "$lib/storybook";

const meta: Meta<WorkspaceBoardSectionContextMenu> = {
    component: WorkspaceBoardSectionContextMenu,
    argTypes: {},
    args: { workspaceBoardSection, workspaceBoardSectionModule },
};
export default meta;

type Story = StoryObj<WorkspaceBoardSectionContextMenu>;

export const Default: Story = {};
