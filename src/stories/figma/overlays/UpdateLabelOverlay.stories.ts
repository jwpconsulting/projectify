import type { Meta, StoryObj } from "@storybook/svelte";

import { labelAssignment } from "$lib/storybook";

import UpdateLabelOverlay from "$lib/figma/overlays/UpdateLabelOverlay.svelte";

const meta: Meta<UpdateLabelOverlay> = {
    component: UpdateLabelOverlay,
    args: { labelAssignment },
};
export default meta;

type Story = StoryObj<UpdateLabelOverlay>;

export const Default: Story = {};
