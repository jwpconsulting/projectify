import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect, mobileParameters } from "$lib/storybook";

import MobileMenuOverlayTest from "./MobileMenuOverlayTest.svelte";

const mobileMenuType = makeStorybookSelect({
    Landing: { kind: "landing" },
    Dashboard: { kind: "dashboard" },
    Continue: { kind: "continue" },
});

const meta: Meta<MobileMenuOverlayTest> = {
    component: MobileMenuOverlayTest,
    argTypes: {
        mobileMenuType,
    },
    args: {
        mobileMenuType: "landing",
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<MobileMenuOverlayTest>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
