import type { Meta, StoryObj } from "@storybook/svelte";

import FilterWorkspaceUsers from "$lib/figma/navigation/side-nav/FilterWorkspaceUsers.svelte";

const meta: Meta<FilterWorkspaceUsers> = {
    component: FilterWorkspaceUsers,
};
export default meta;

type Story = StoryObj<FilterWorkspaceUsers>;

export const Default: Story = {};
