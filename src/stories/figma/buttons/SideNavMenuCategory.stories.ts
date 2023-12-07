import { Search } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";

const meta: Meta<SideNavMenuCategory> = {
    component: SideNavMenuCategory,
    args: {
        label: "asd",
        icon: Search,
        filtered: false,
        open: false,
        contained: false,
    },
    argTypes: {
        label: { control: "text" },
        filtered: { control: "boolean" },
        open: { control: "boolean" },
        contained: { control: "boolean" },
    },
};
export default meta;

type Story = StoryObj<SideNavMenuCategory>;

export const Default: Story = {};
export const Contained: Story = {
    args: { contained: true },
};
