import type { Meta, StoryObj } from "@storybook/svelte";

import Layout from "$lib/figma/navigation/header/Layout.svelte";
import { mobileParameters } from "$lib/storybook";

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
