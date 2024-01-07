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

import TaskDueDate from "$lib/figma/screens/task/TaskDueDate.svelte";

const meta: Meta<TaskDueDate> = {
    component: TaskDueDate,
    args: { readonly: false },
    argTypes: {
        readonly: { control: "boolean" },
        date: {
            control: {
                type: "radio",
            },
            options: [null, "2024-01-01", "2024-01-01T23:23"],
        },
    },
};
export default meta;

type Story = StoryObj<TaskDueDate>;

export const Default: Story = {
    args: { date: null },
};

export const DateSelected: Story = {
    args: { date: "2024-01-01" },
};

export const DueSoon: Story = {
    args: { date: "2024-01-01", dueSoon: true },
};
