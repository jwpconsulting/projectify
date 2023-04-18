import type { Meta, StoryObj } from "@storybook/svelte";

import UpdateUser from "$lib/figma/buttons/UpdateUser.svelte";
import { user1 } from "$lib/storybook";

const meta: Meta<UpdateUser> = {
    component: UpdateUser,
    argTypes: {},
    args: {
        action: console.log,
    },
};
export default meta;

type Story = StoryObj<UpdateUser>;

export const Default: Story = {
    args: {
        user: user1,
    },
};

export const NoUser: Story = {
    args: {
        user: null,
    },
};
