import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceUser from "$lib/figma/overlays/context-menu/WorkspaceUser.svelte";
import { workspaceUserAssignment } from "$lib/storybook";

const meta: Meta<WorkspaceUser> = {
    component: WorkspaceUser,
    args: { workspaceUserAssignment },
};
export default meta;

type Story = StoryObj<WorkspaceUser>;

export const Default: Story = {};
