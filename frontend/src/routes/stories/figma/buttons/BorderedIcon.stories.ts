// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<BorderedIcon> = {
    component: BorderedIcon,
};
export default meta;

type Story = StoryObj<BorderedIcon>;

export const Workspace: Story = {
    args: { type: "workspace" },
};

export const Filter: Story = {
    args: { type: "filter" },
};
