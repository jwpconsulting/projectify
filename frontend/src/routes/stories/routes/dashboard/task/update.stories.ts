// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import { mobileParameters, task } from "$lib-stories/storybook";
import Update from "$routes/(platform)/dashboard/task/[taskUuid]/update/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Update> = {
    component: Update,
    args: {
        data: { task },
    },
};
export default meta;

type Story = StoryObj<Update>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
