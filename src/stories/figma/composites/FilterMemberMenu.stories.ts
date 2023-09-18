import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUserFilter } from "$lib/storybook";

import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";

const meta: Meta<FilterMemberMenu> = {
    component: FilterMemberMenu,
    argTypes: {},
    args: { workspaceUserFilter },
};
export default meta;

type Story = StoryObj<FilterMemberMenu>;

export const Default: Story = {};
