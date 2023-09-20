import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUserAssignment } from "$lib/storybook";

import UpdateMemberOverlay from "$lib/figma/overlays/UpdateMemberOverlay.svelte";

const meta: Meta<UpdateMemberOverlay> = {
    component: UpdateMemberOverlay,
    args: { workspaceUserAssignment },
};
export default meta;

type Story = StoryObj<UpdateMemberOverlay>;

export const Default: Story = {};
