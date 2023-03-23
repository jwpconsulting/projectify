import type { Meta, StoryObj } from "@storybook/svelte";

import SideNav from "$lib/figma/navigation/SideNav.svelte";

import { mobileParameters } from "$lib/storybook";

const meta: Meta<SideNav> = {
    component: SideNav,
    argTypes: {},
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<SideNav>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
