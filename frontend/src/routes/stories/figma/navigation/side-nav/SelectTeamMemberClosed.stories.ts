// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK

import SelectTeamMemberClosed from "$lib/figma/navigation/side-nav/SelectTeamMemberClosed.svelte";
import { makeStorybookSelect, user1, user2 } from "$lib-stories/storybook";
import type { User } from "$lib/types/user";
import type { Meta, StoryObj } from "@storybook/svelte";

const users = makeStorybookSelect<User | null>({
    "With user 1": user1,
    "With user 2": user2,
    "No user": null,
});

const meta: Meta<SelectTeamMemberClosed> = {
    component: SelectTeamMemberClosed,
    argTypes: { user: users, active: { control: "boolean" } },
    args: {
        user: "with-user-1",
        active: true,
    },
};
export default meta;

type Story = StoryObj<SelectTeamMemberClosed>;

export const Default: Story = {};
export const NoUser: Story = { args: { user: "no-user" } };
