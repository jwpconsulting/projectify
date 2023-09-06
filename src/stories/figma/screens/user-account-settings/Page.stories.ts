import type { Meta, StoryObj } from "@storybook/svelte";

import { user1 } from "$lib/storybook";

import Page from "$lib/figma/screens/user-account-settings/Page.svelte";

const meta: Meta<Page> = {
    component: Page,
    args: { user: user1 },
};
export default meta;

type Story = StoryObj<Page>;

export const Default: Story = {};
