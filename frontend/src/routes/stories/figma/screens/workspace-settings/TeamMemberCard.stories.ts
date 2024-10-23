// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import TeamMemberCard from "$lib/figma/screens/workspace-settings/TeamMemberCard.svelte";
import { teamMember } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TeamMemberCard> = {
    component: TeamMemberCard,
    args: { teamMember },
};
export default meta;

type Story = StoryObj<TeamMemberCard>;

export const Default: Story = {};
