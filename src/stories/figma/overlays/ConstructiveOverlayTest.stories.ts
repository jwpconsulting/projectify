import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters } from "$lib/storybook";

import ConstructiveOverlayTest from "./ConstructiveOverlayTest.svelte";

const meta: Meta<ConstructiveOverlayTest> = {
    component: ConstructiveOverlayTest,
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<ConstructiveOverlayTest>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
