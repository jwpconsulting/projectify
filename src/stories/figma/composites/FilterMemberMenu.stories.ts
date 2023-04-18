import type { Meta, StoryObj } from "@storybook/svelte";

import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
import { workspaceUserSearchModule } from "$lib/storybook";

const meta: Meta<FilterMemberMenu> = {
    component: FilterMemberMenu,
    argTypes: {},
    args: { workspaceUserSearchModule },
};
export default meta;

type Story = StoryObj<FilterMemberMenu>;

export const Default: Story = {};
