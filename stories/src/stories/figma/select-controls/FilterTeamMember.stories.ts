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

import FilterTeamMember from "$lib/figma/select-controls/FilterTeamMember.svelte";
import {
    makeStorybookSelect,
    mobileParameters,
    teamMemberSelectionInputs,
} from "$lib/storybook";
import type { TeamMemberSelectionInput } from "$lib/types/ui";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<FilterTeamMember> = {
    component: FilterTeamMember,
    argTypes: {
        teamMemberSelectionInput:
            makeStorybookSelect<TeamMemberSelectionInput>({
                "Unassigned": teamMemberSelectionInputs[0],
                "All team members": teamMemberSelectionInputs[1],
                "Team member": teamMemberSelectionInputs[2],
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
        teamMemberSelectionInput: teamMemberSelectionInputs[2],
        onSelect: console.error,
        onDeselect: console.error,
    },
};
export default meta;

type Story = StoryObj<FilterTeamMember>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
