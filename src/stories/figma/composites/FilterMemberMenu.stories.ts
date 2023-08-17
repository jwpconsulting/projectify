import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUserSearchModule } from "$lib/storybook";

import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";

const meta: Meta<FilterMemberMenu> = {
    component: FilterMemberMenu,
    argTypes: {},
    args: { workspaceUserSearchModule },
};
export default meta;

type Story = StoryObj<FilterMemberMenu>;

export const Default: Story = {};
