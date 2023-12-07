import type { Meta, StoryObj } from "@storybook/svelte";

import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
import { makeStorybookSelect, user1, user2 } from "$lib/storybook";
import type { User } from "$lib/types/user";

const users = makeStorybookSelect<User | null>({
    "With user 1": user1,
    "With user 2": user2,
    "No user": null,
});

const meta: Meta<SelectUserClosedNav> = {
    component: SelectUserClosedNav,
    argTypes: { user: users, active: { control: "boolean" } },
    args: {
        user: "with-user-1",
        active: true,
    },
};
export default meta;

type Story = StoryObj<SelectUserClosedNav>;

export const Default: Story = {};
export const NoUser: Story = { args: { user: "no-user" } };
