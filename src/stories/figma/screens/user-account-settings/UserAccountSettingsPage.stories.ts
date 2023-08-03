import type { Meta, StoryObj } from "@storybook/svelte";

import UserAccountSettingsPage from "$lib/figma/screens/user-account-settings/UserAccountSettingsPage.svelte";

import { user1 } from "$lib/storybook";

const meta: Meta<UserAccountSettingsPage> = {
    component: UserAccountSettingsPage,
    argTypes: {},
};
export default meta;

type Story = StoryObj<UserAccountSettingsPage>;

export const Default: Story = {
    args: {
        user: user1,
    },
};
