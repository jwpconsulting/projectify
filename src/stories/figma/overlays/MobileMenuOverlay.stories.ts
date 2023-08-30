import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect } from "$lib/storybook";

import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";

const target = makeStorybookSelect({
    Landing: { kind: "landing" },
    Dashboard: { kind: "dashboard" },
    Continue: { kind: "continue" },
});

const meta: Meta<MobileMenuOverlay> = {
    component: MobileMenuOverlay,
    argTypes: {
        target,
    },
    args: {
        target: "landing",
    },
};
export default meta;

type Story = StoryObj<MobileMenuOverlay>;

export const Default: Story = {};
