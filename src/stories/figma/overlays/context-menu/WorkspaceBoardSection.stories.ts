import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceBoardSection from "$lib/figma/overlays/context-menu/WorkspaceBoardSection.svelte";
import { workspaceBoard, workspaceBoardSection } from "$lib/storybook";

const meta: Meta<WorkspaceBoardSection> = {
    component: WorkspaceBoardSection,
    argTypes: {},
    args: { workspaceBoard, workspaceBoardSection },
};
export default meta;

type Story = StoryObj<WorkspaceBoardSection>;

export const Default: Story = {};
