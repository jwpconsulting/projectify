// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<FilterLabelMenu> = {
    component: FilterLabelMenu,
    args: {
        mode: { kind: "filter" },
    },
};
export default meta;

type Story = StoryObj<FilterLabelMenu>;

export const Default: Story = {};
