// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import FilterLabels from "$lib/figma/navigation/side-nav/FilterLabels.svelte";
import type { FilterLabelMenuState } from "$lib/figma/types";
import { makeStorybookSelect, mappedLabels } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const states = makeStorybookSelect<FilterLabelMenuState>({
    List: { kind: "list" },
    Create: { kind: "create" },
    Update: { kind: "update", label: mappedLabels[0] },
});

const meta: Meta<FilterLabels> = {
    component: FilterLabels,
    argTypes: {
        state: states,
    },
};
export default meta;

type Story = StoryObj<FilterLabels>;

export const List: Story = {
    args: {
        state: "list",
    },
};
export const Create: Story = {
    args: {
        state: "create",
    },
};
export const Update: Story = {
    args: {
        state: "update",
    },
};
