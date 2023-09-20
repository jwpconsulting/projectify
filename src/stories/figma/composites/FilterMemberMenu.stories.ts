import type { Meta, StoryObj } from "@storybook/svelte";

import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";

const meta: Meta<FilterMemberMenu> = {
    component: FilterMemberMenu,
};
export default meta;

type Story = StoryObj<FilterMemberMenu>;

export const Default: Story = {};
