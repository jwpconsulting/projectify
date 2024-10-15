// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import { user1 } from "$lib-stories/storybook";
import Profile from "$routes/(platform)/user/profile/+page.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Profile> = {
    component: Profile,
    args: { data: { user: user1, userAwaitable: Promise.resolve(user1) } },
};
export default meta;

type Story = StoryObj<Profile>;

export const Default: Story = {};
