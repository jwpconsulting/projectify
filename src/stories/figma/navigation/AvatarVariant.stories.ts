import type { Meta, StoryObj } from "@storybook/svelte";

import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";

import { avatarVariantSizes } from "$lib/figma/types";
import { user1, user2 } from "$lib/storybook";

const meta: Meta<AvatarVariant> = {
    component: AvatarVariant,
    argTypes: {
        size: {
            options: avatarVariantSizes,
            control: {
                type: "radio",
            },
        },
    },
};
export default meta;

type Story = StoryObj<AvatarVariant>;

export const Default: Story = {
    args: {
        size: "medium",
        content: {
            kind: "single",
            user: null,
        },
    },
};

export const User1: Story = {
    args: {
        size: "medium",
        content: {
            kind: "single",
            user: user1,
        },
    },
};

export const User2: Story = {
    args: {
        size: "medium",
        content: {
            kind: "single",
            user: user2,
        },
    },
};

export const Multiple: Story = {
    args: {
        size: "medium",
        content: {
            kind: "multiple",
            users: [user1, user2],
        },
    },
};

export const Assign: Story = {
    args: {
        size: "medium",
        content: {
            kind: "assign",
            users: [user1, user2],
        },
    },
};
