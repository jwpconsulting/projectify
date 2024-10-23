// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Label from "$lib/figma/buttons/Label.svelte";
import { labels } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Label> = {
    component: Label,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Label>;

export const Default: Story = {
    args: {
        label: labels[0],
    },
};

export const Apply: Story = {
    args: {
        label: labels[labels.length - 1],
    },
};

export const WithAction: Story = {
    args: {
        label: labels[labels.length - 1],
        action: console.log,
    },
};
