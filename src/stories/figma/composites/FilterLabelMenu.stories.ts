import type { Meta, StoryObj } from "@storybook/svelte";

import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";

const meta: Meta<FilterLabelMenu> = {
    component: FilterLabelMenu,
    args: {
        mode: { kind: "filter" },
    },
};
export default meta;

type Story = StoryObj<FilterLabelMenu>;

export const Default: Story = {};
