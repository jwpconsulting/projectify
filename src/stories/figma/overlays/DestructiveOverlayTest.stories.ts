import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters } from "$lib/storybook";

import { destructiveOverlays } from "./config";
import DestructiveOverlayTest from "./DestructiveOverlayTest.svelte";

// TODO
// Ideally, we can test all kinds of destructive overlays here using
// argTypes
const meta: Meta<DestructiveOverlayTest> = {
    component: DestructiveOverlayTest,
    argTypes: {
        target: destructiveOverlays,
    },
    args: {
        target: "delete-label",
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<DestructiveOverlayTest>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
