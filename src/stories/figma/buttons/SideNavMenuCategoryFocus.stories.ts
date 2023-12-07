import { Search } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";

const meta: Meta<SideNavMenuCategoryFocus> = {
    component: SideNavMenuCategoryFocus,
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

type Story = StoryObj<SideNavMenuCategoryFocus>;

export const Default: Story = {};
