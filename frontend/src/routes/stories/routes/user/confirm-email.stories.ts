// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import ConfirmEmail from "$routes/(storefront)/user/(auth)/confirm-email/[email]/[token]/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<ConfirmEmail> = {
    component: ConfirmEmail,
};
export default meta;

type Story = StoryObj<ConfirmEmail>;

export const Default: Story = {};
