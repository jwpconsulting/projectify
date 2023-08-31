import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters } from "$lib/storybook";

import { constructiveOverlays } from "./config";
import ConstructiveOverlayTest from "./ConstructiveOverlayTest.svelte";

const meta: Meta<ConstructiveOverlayTest> = {
    component: ConstructiveOverlayTest,
    argTypes: {
        target: constructiveOverlays,
    },
    args: {
        target: "update-workspace-board",
    },
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
