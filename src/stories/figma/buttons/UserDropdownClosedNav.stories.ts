import type { Meta, StoryObj } from "@storybook/svelte";

import UserDropdownClosedNav from "$lib/figma/buttons/UserDropdownClosedNav.svelte";

const meta: Meta<UserDropdownClosedNav> = {
    component: UserDropdownClosedNav,
};
export default meta;

type Story = StoryObj<UserDropdownClosedNav>;

export const Default: Story = {};
