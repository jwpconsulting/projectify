import type { Meta, StoryObj } from "@storybook/svelte";

import UserAccountSettings from "$lib/figma/screens/user-account-settings/UserAccountSettings.svelte";

const meta: Meta<UserAccountSettings> = {
    component: UserAccountSettings,
    argTypes: {},
};
export default meta;

type Story = StoryObj<UserAccountSettings>;

export const Default: Story = {};
