import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters } from "$lib/storybook";

import Layout from "$lib/figma/navigation/header/Layout.svelte";

const meta: Meta<Layout> = {
    component: Layout,
    argTypes: {},
    args: {
        logoVisibleDesktop: true,
        logoVisibleMobile: true,
    },
};
export default meta;

type Story = StoryObj<Layout>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
