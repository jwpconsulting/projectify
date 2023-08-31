import type { Meta, StoryObj } from "@storybook/svelte";

import { destructiveOverlays } from "./config";

import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";

const meta: Meta<DestructiveOverlay> = {
    component: DestructiveOverlay,
    argTypes: { target: destructiveOverlays },
    args: { target: "delete-board" },
};
export default meta;

type Story = StoryObj<DestructiveOverlay>;

export const Default: Story = {};
