import type { Meta, StoryObj } from "@storybook/svelte";

import SentEmailConfirmation from "$routes/(storefront)/(auth)/user/sent-email-confirmation-link/+page.svelte";

const meta: Meta<SentEmailConfirmation> = {
    component: SentEmailConfirmation,
};
export default meta;

type Story = StoryObj<SentEmailConfirmation>;

export const Default: Story = {};
