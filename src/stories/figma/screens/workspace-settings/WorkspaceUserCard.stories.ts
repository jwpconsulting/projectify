import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceUserCard from "$lib/figma/screens/workspace-settings/WorkspaceUserCard.svelte";
import { workspaceUser } from "$lib/storybook";

const meta: Meta<WorkspaceUserCard> = {
    component: WorkspaceUserCard,
    args: { workspaceUser },
};
export default meta;

type Story = StoryObj<WorkspaceUserCard>;

export const Default: Story = {};
