// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import ConfirmPasswordReset from "$routes/(storefront)/user/(auth)/confirm-password-reset/[email]/[token]/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<ConfirmPasswordReset> = {
    component: ConfirmPasswordReset,
    args: {
        data: {
            // XXX why does pw reset need a redirect url?
            redirectTo: undefined,
            email: "hello@example.com",
            token: "yo",
        },
    },
};
export default meta;

type Story = StoryObj<ConfirmPasswordReset>;

export const Default: Story = {};
