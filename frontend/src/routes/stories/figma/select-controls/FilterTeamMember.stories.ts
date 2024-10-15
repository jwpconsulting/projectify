// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import FilterTeamMember from "$lib/figma/select-controls/FilterTeamMember.svelte";
import {
    makeStorybookSelect,
    mobileParameters,
    teamMemberSelectionInputs,
} from "$lib-stories/storybook";
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
