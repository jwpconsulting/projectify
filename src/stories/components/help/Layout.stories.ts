import type { Meta, StoryObj } from "@storybook/svelte";

import Layout from "$lib/components/help/Layout.svelte";

const meta: Meta<Layout> = {
    component: Layout,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Layout>;

export const Default: Story = {};
