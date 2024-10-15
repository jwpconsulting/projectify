// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import RequestPasswordReset from "$routes/(storefront)/user/(auth)/request-password-reset/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<RequestPasswordReset> = {
    component: RequestPasswordReset,
};
export default meta;

type Story = StoryObj<RequestPasswordReset>;

export const Default: Story = {};
