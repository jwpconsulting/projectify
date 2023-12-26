import type { Meta, StoryObj } from "@storybook/svelte";

import { user1 } from "$lib/storybook";
import Profile from "$routes/(platform)/user/profile/+page.svelte";

const meta: Meta<Profile> = {
    component: Profile,
    args: { data: { user: user1 } },
};
export default meta;

type Story = StoryObj<Profile>;

export const Default: Story = {};
