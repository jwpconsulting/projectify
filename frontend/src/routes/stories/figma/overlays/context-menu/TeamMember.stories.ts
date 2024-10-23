// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import TeamMember from "$lib/figma/overlays/context-menu/TeamMember.svelte";
import { teamMemberAssignment } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TeamMember> = {
    component: TeamMember,
    args: { teamMemberAssignment },
};
export default meta;

type Story = StoryObj<TeamMember>;

export const Default: Story = {};
