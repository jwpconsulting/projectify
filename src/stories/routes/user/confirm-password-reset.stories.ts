import type { Meta, StoryObj } from "@storybook/svelte";

import ConfirmPasswordReset from "$routes/(storefront)/(auth)/user/confirm-password-reset/[email]/[token]/+page.svelte";

const meta: Meta<ConfirmPasswordReset> = {
    component: ConfirmPasswordReset,
    args: {
        data: {
            email: "hello@example.com",
            token: "yo",
        },
    },
};
export default meta;

type Story = StoryObj<ConfirmPasswordReset>;

export const Default: Story = {};
