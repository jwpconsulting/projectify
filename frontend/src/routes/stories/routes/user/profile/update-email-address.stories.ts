// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
/**
 * Stories for user update email form
 */
import UpdateEmail from "$routes/(platform)/user/profile/update-email-address/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<UpdateEmail> = {
    component: UpdateEmail,
};
export default meta;

type Story = StoryObj<UpdateEmail>;

export const Default: Story = {};
