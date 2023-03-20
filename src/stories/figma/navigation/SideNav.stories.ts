import type { Meta, StoryObj } from "@storybook/svelte";

import SideNav from "$lib/figma/navigation/SideNav.svelte";

const meta: Meta<SideNav> = {
    component: SideNav,
    argTypes: {},
};
export default meta;

type Story = StoryObj<SideNav>;

export const Default: Story = {};
