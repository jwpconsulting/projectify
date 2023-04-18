import type { Meta, StoryObj } from "@storybook/svelte";

import UpdateLabelOverlay from "$lib/figma/overlays/UpdateLabelOverlay.svelte";

import { labelSearchModule } from "$lib/storybook";

const meta: Meta<UpdateLabelOverlay> = {
    component: UpdateLabelOverlay,
    argTypes: {},
    args: { labelSearchModule },
};
export default meta;

type Story = StoryObj<UpdateLabelOverlay>;

export const Default: Story = {};
