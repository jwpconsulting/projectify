// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<HamburgerMenu> = {
    component: HamburgerMenu,
    argTypes: { isActive: { control: "boolean" } },
    args: { isActive: true, action: console.log },
};
export default meta;

type Story = StoryObj<HamburgerMenu>;

export const Default: Story = {};
