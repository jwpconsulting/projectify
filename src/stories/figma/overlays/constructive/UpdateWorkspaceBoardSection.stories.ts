import type { Meta, StoryObj } from "@storybook/svelte";

import UpdateWorkspaceBoardSection from "$lib/figma/overlays/constructive/UpdateWorkspaceBoardSection.svelte";
import { workspaceBoardSection } from "$lib/storybook";

const meta: Meta<UpdateWorkspaceBoardSection> = {
    component: UpdateWorkspaceBoardSection,
    args: { workspaceBoardSection },
};
export default meta;

type Story = StoryObj<UpdateWorkspaceBoardSection>;

export const Default: Story = {};
