import type { Meta, StoryObj } from "@storybook/svelte";

import UpdateLabelOverlay from "$lib/figma/overlays/UpdateLabelOverlay.svelte";

const meta: Meta<UpdateLabelOverlay> = {
    component: UpdateLabelOverlay,
    argTypes: {},
};
export default meta;

type Story = StoryObj<UpdateLabelOverlay>;

export const Default: Story = {};
