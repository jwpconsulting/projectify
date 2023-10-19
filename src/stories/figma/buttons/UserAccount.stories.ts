import type { Meta, StoryObj } from "@storybook/svelte";

import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
import { user1 } from "$lib/storybook";

const meta: Meta<UserAccount> = {
    component: UserAccount,
    args: {
        user: user1,
    },
};
export default meta;

type Story = StoryObj<UserAccount>;

export const Default: Story = {};
