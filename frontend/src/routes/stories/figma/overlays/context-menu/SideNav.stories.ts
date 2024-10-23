// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK

import SideNav from "$lib/figma/overlays/context-menu/SideNav.svelte";
import { workspace } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<SideNav> = {
    component: SideNav,
    argTypes: {},
    args: { workspace },
};
export default meta;

type Story = StoryObj<SideNav>;

export const Default: Story = {};
