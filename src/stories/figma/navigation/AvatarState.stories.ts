import type { Meta, StoryObj } from "@storybook/svelte";

import AvatarState from "$lib/figma/navigation/AvatarState.svelte";
import type { AvatarStateSize } from "$lib/figma/types";
import { makeStorybookSelect, user1, user2 } from "$lib/storybook";
import type { User } from "$lib/types/user";

const users = makeStorybookSelect<User | null>({
    "With user 1": user1,
    "With user 2": user2,
    "No user": null,
});

const sizes = makeStorybookSelect<AvatarStateSize>({
    Small: "small",
    Medium: "medium",
    Large: "large",
    Hoverable: "hoverable",
});

const meta: Meta<AvatarState> = {
    component: AvatarState,
    argTypes: {
        user: users,
        size: sizes,
    },
    args: {
        user: "with-user-1",
        size: "small",
    },
};
export default meta;

type Story = StoryObj<AvatarState>;

export const Default: Story = {};

export const NoUser: Story = { args: { user: "no-user" } };
