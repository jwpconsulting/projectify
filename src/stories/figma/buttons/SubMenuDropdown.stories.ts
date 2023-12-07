import { Search } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";

const meta: Meta<SubMenuDropdown> = {
    component: SubMenuDropdown,
    argTypes: {
        label: { control: "text" },
    },
    args: {
        label: "Hello world",
        icon: Search,
    },
};
export default meta;

type Story = StoryObj<SubMenuDropdown>;

export const Default: Story = {};
