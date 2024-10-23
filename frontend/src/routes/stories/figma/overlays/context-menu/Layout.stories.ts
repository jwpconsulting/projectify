// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Layout> = {
    component: Layout,
};
export default meta;

type Story = StoryObj<Layout>;

export const Default: Story = {};
