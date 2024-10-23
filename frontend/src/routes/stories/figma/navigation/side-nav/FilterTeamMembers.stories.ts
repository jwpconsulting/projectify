// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import FilterTeamMembers from "$lib/figma/navigation/side-nav/FilterTeamMembers.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<FilterTeamMembers> = {
    component: FilterTeamMembers,
};
export default meta;

type Story = StoryObj<FilterTeamMembers>;

export const Default: Story = {};
