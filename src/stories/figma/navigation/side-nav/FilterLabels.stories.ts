import type { Meta, StoryObj } from "@storybook/svelte";

import FilterLabels from "$lib/figma/navigation/side-nav/FilterLabels.svelte";

const meta: Meta<FilterLabels> = {
    component: FilterLabels,
};
export default meta;

type Story = StoryObj<FilterLabels>;

export const Default: Story = {};
