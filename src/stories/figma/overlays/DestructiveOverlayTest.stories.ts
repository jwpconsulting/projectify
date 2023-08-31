import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters } from "$lib/storybook";

import DestructiveOverlayTest from "./DestructiveOverlayTest.svelte";

// TODO
// Ideally, we can test all kinds of destructive overlays here using
// argTypes
const meta: Meta<DestructiveOverlayTest> = {
    component: DestructiveOverlayTest,
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
