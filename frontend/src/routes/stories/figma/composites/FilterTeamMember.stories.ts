// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import FilterTeamMember from "$lib/figma/composites/FilterTeamMember.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<FilterTeamMember> = {
    component: FilterTeamMember,
};
export default meta;

type Story = StoryObj<FilterTeamMember>;

export const Default: Story = {};
