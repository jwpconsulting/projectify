import type { Meta, StoryObj } from "@storybook/svelte";

import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";

import { destructiveOverlays } from "./config";

const meta: Meta<DestructiveOverlay> = {
    component: DestructiveOverlay,
    argTypes: { target: destructiveOverlays },
    args: { target: "delete-board" },
};
export default meta;

type Story = StoryObj<DestructiveOverlay>;

export const Default: Story = {};
