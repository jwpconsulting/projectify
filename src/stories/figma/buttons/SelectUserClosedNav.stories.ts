// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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
