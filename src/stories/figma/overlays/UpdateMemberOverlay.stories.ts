import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUserFilter } from "$lib/storybook";

import UpdateMemberOverlay from "$lib/figma/overlays/UpdateMemberOverlay.svelte";

const meta: Meta<UpdateMemberOverlay> = {
    component: UpdateMemberOverlay,
    argTypes: {},
    args: { workspaceUserFilter },
};
export default meta;

type Story = StoryObj<UpdateMemberOverlay>;

export const Default: Story = {};
