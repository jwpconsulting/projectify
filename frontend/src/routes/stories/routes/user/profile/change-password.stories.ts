// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
/**
 * Stories for user change password form
 */

import ChangePassword from "$routes/(platform)/user/profile/change-password/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<ChangePassword> = {
    component: ChangePassword,
    args: {},
};
export default meta;

type Story = StoryObj<ChangePassword>;

export const Default: Story = {};
