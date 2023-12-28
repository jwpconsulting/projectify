import type { Meta, StoryObj } from "@storybook/svelte";

import RequestPasswordReset from "$routes/(storefront)/(auth)/user/request-password-reset/+page.svelte";

const meta: Meta<RequestPasswordReset> = {
    component: RequestPasswordReset,
};
export default meta;

type Story = StoryObj<RequestPasswordReset>;

export const Default: Story = {};
