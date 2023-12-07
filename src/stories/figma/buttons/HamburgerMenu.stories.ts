import type { Meta, StoryObj } from "@storybook/svelte";

import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";

const meta: Meta<HamburgerMenu> = {
    component: HamburgerMenu,
    argTypes: { isActive: { control: "boolean" } },
    args: { isActive: true, action: console.log },
};
export default meta;

type Story = StoryObj<HamburgerMenu>;

export const Default: Story = {};
