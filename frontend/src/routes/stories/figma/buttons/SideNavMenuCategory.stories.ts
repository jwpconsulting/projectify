// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
import { Search } from "@steeze-ui/heroicons";
import type { Meta, StoryObj } from "@storybook/svelte";

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
