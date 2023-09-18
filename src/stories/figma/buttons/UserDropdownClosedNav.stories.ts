import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUserFilter } from "$lib/storybook";

import UserDropdownClosedNav from "$lib/figma/buttons/UserDropdownClosedNav.svelte";

const meta: Meta<UserDropdownClosedNav> = {
    component: UserDropdownClosedNav,
    argTypes: {},
    args: {
        workspaceUserFilter,
    },
};
export default meta;

type Story = StoryObj<UserDropdownClosedNav>;

export const Default: Story = {};
