// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Continue from "$lib/figma/navigation/header/Continue.svelte";
import { mobileParameters } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Continue> = {
    component: Continue,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<Continue>;

export const Desktop: Story = {};
export const Mobile: Story = {
    parameters: mobileParameters,
};
