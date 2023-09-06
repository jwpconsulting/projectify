import type { Meta, StoryObj } from "@storybook/svelte";

import UserAccountSettings from "$lib/figma/screens/user-account-settings/UserAccountSettings.svelte";

import { user1 } from "$lib/storybook";

const meta: Meta<UserAccountSettings> = {
    component: UserAccountSettings,
    args: { user: user1 },
};
export default meta;

type Story = StoryObj<UserAccountSettings>;

export const Default: Story = {};
