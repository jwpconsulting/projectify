// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK

import CreateOrUpdateLabel from "$lib/figma/navigation/side-nav/filter-labels/CreateOrUpdateLabel.svelte";
import { makeStorybookSelect, mappedLabels } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const states = makeStorybookSelect({
    "Create label": { kind: "create" },
    "Update label": { kind: "update", label: mappedLabels[0] },
});

const meta: Meta<CreateOrUpdateLabel> = {
    component: CreateOrUpdateLabel,
    argTypes: { state: states },
};
export default meta;

type Story = StoryObj<CreateOrUpdateLabel>;

export const Create: Story = {
    args: { state: "create-label" },
};

export const Update: Story = {
    args: { state: "update-label" },
};
