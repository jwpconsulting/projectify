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

import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
import { teamMember } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TaskUser> = {
    component: TaskUser,
    args: {
        teamMember,
        onInteract: console.log,
    },
};
export default meta;

type Story = StoryObj<TaskUser>;

export const Default: Story = {};

export const NoUser: Story = { args: { teamMember: undefined } };

export const NoAction: Story = { args: { onInteract: undefined } };
