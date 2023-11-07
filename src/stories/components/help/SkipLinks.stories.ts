import type { Meta, StoryObj } from "@storybook/svelte";

import SkipLinks from "$lib/components/help/SkipLinks.svelte";

const meta: Meta<SkipLinks> = {
    component: SkipLinks,
    argTypes: {},
};
export default meta;

type Story = StoryObj<SkipLinks>;

export const Default: Story = {};
