// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import FilterLabelsClosed from "$lib/figma/navigation/side-nav/FilterLabelsClosed.svelte";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<FilterLabelsClosed> = {
    component: FilterLabelsClosed,
};
export default meta;

type Story = StoryObj<FilterLabelsClosed>;

export const Default: Story = {};
