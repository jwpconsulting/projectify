// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
import { makeStorybookSelect, user1, user2 } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";
import type { AvatarStateSize } from "$lib/figma/types";

const meta: Meta<AvatarVariant> = {
    component: AvatarVariant,
    argTypes: {
        size: makeStorybookSelect<AvatarStateSize>({
            Medium: "medium",
            Large: "large",
        }),
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
