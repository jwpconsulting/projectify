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

import FilterUser from "$lib/figma/select-controls/FilterUser.svelte";
import {
    makeStorybookSelect,
    mobileParameters,
    workspaceUserSelectionInputs,
} from "$lib/storybook";
import type { WorkspaceUserSelectionInput } from "$lib/types/ui";

const meta: Meta<FilterUser> = {
    component: FilterUser,
    argTypes: {
        workspaceUserSelectionInput:
            makeStorybookSelect<WorkspaceUserSelectionInput>({
                "Unassigned": workspaceUserSelectionInputs[0],
                "All workspace users": workspaceUserSelectionInputs[1],
                "Workspace user": workspaceUserSelectionInputs[2],
            }),
        count: makeStorybookSelect({
            "Unknown tasks assigned": undefined,
            "0 tasks assigned": 0,
            "1 task assigned": 209,
            "4909012 tasks assigned": 4909012,
        }),
        active: {
            control: "boolean",
        },
    },
    args: {
        active: true,
        count: "no-tasks-assigned",
        workspaceUserSelectionInput: workspaceUserSelectionInputs[2],
        onSelect: console.error,
        onDeselect: console.error,
    },
};
export default meta;

type Story = StoryObj<FilterUser>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
