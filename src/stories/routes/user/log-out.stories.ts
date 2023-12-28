import type { Meta, StoryObj } from "@storybook/svelte";

import LogOut from "$routes/(storefront)/(auth)/user/log-out/+page.svelte";

const meta: Meta<LogOut> = {
    component: LogOut,
};
export default meta;

type Story = StoryObj<LogOut>;

export const Default: Story = {};
