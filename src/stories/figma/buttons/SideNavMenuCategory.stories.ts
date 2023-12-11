import { Search } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";

const meta: Meta<SideNavMenuCategory> = {
    component: SideNavMenuCategory,
    argTypes: {
        filtered: { control: "boolean" },
        open: { control: "boolean" },
    },
    args: {
        label: "Hello world",
        icon: Search,
        filtered: true,
        open: false,
    },
};
export default meta;

type Story = StoryObj<SideNavMenuCategory>;

export const Default: Story = {};
