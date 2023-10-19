import type { Meta, StoryObj } from "@storybook/svelte";

import FilterWorkspaceUser from "$lib/figma/composites/FilterWorkspaceUser.svelte";

const meta: Meta<FilterWorkspaceUser> = {
    component: FilterWorkspaceUser,
};
export default meta;

type Story = StoryObj<FilterWorkspaceUser>;

export const Default: Story = {};
