// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Layout from "$lib/figma/navigation/header/Layout.svelte";
import { mobileParameters } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Layout> = {
    component: Layout,
    argTypes: {},
    args: {
        logoVisibleDesktop: true,
        logoVisibleMobile: true,
    },
};
export default meta;

type Story = StoryObj<Layout>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
