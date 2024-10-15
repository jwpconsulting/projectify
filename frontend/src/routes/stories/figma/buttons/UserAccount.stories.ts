// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
import { user1 } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<UserAccount> = {
    component: UserAccount,
    args: {
        user: user1,
    },
};
export default meta;

type Story = StoryObj<UserAccount>;

export const Default: Story = {};
