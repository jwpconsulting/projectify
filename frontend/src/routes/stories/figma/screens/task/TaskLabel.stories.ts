// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
import { makeStorybookSelect, mappedLabels } from "$lib-stories/storybook";
import type { Label } from "$lib/types/workspace";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TaskLabel> = {
    component: TaskLabel,
    argTypes: {
        labels: makeStorybookSelect<Label[]>({
            "0 labels selected": [],
            "1 labels selected": mappedLabels.slice(0, 1),
            "3 labels selected": mappedLabels.slice(1, 4),
        }),
    },
    args: {
        labels: "3-labels-selected",
    },
};
export default meta;

type Story = StoryObj<TaskLabel>;

export const Default: Story = {};

export const ApplyLabel: Story = {
    args: {
        labels: "0-labels-selected",
    },
};
