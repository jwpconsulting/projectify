import type { Meta, StoryObj } from "@storybook/svelte";

import { user1 } from "$lib/storybook";

import UserAccount from "$lib/figma/buttons/UserAccount.svelte";

const meta: Meta<UserAccount> = {
    component: UserAccount,
    args: {
        user: user1,
    },
};
export default meta;

type Story = StoryObj<UserAccount>;

export const Default: Story = {};
