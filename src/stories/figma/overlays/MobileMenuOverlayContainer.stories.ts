import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect } from "$lib/storybook";

import MobileMenuOverlayContainer from "./MobileMenuOverlayContainer.svelte";

const mobileMenuType = makeStorybookSelect({
    Landing: { kind: "landing" },
    Dashboard: { kind: "dashboard" },
    Continue: { kind: "continue" },
});

const meta: Meta<MobileMenuOverlayContainer> = {
    component: MobileMenuOverlayContainer,
    argTypes: {
        mobileMenuType,
    },
    args: {
        mobileMenuType: "landing",
    },
};
export default meta;

type Story = StoryObj<MobileMenuOverlayContainer>;

export const Default: Story = {};
