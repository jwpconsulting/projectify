// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import Profile from "$lib/figma/overlays/context-menu/Profile.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Profile> = {
    component: Profile,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Profile>;

export const Default: Story = {};
