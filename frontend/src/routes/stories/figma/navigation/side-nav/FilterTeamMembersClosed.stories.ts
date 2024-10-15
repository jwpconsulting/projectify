// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import FilterTeamMembersClosed from "$lib/figma/navigation/side-nav/FilterTeamMembersClosed.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<FilterTeamMembersClosed> = {
    component: FilterTeamMembersClosed,
};
export default meta;

type Story = StoryObj<FilterTeamMembersClosed>;

export const Default: Story = {};
