import type { Meta, StoryObj } from "@storybook/svelte";

import ConfirmEmail from "$routes/(storefront)/(auth)/user/confirm-email/[email]/[token]/+page.svelte";

const meta: Meta<ConfirmEmail> = {
    component: ConfirmEmail,
};
export default meta;

type Story = StoryObj<ConfirmEmail>;

export const Default: Story = {};
