// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Dashboard from "$lib/figma/navigation/header/Dashboard.svelte";
import { mobileParameters, user1 } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Dashboard> = {
    component: Dashboard,
    argTypes: {},
    args: { user: user1 },
};
export default meta;

type Story = StoryObj<Dashboard>;

export const Desktop: Story = {};
export const Mobile: Story = {
    parameters: mobileParameters,
};
