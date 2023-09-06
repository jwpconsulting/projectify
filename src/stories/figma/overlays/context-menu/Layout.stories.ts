import type { Meta, StoryObj } from "@storybook/svelte";

import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";

const meta: Meta<Layout> = {
    component: Layout,
};
export default meta;

type Story = StoryObj<Layout>;

export const Default: Story = {};
