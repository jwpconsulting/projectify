import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceBoard, workspaceBoardSection } from "$lib/storybook";

import WorkspaceBoardSection from "$lib/figma/overlays/context-menu/WorkspaceBoardSection.svelte";

const meta: Meta<WorkspaceBoardSection> = {
    component: WorkspaceBoardSection,
    argTypes: {},
    args: { workspaceBoard, workspaceBoardSection },
};
export default meta;

type Story = StoryObj<WorkspaceBoardSection>;

export const Default: Story = {};
