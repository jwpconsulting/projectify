// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Landing from "$lib/figma/navigation/header/Landing.svelte";
import { mobileParameters } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Landing> = {
    component: Landing,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<Landing>;

export const Desktop: Story = {};
export const Mobile: Story = {
    parameters: mobileParameters,
};
