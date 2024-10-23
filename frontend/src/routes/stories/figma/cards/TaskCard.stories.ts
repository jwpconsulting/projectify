// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import TaskCard from "$lib/figma/cards/TaskCard.svelte";
import { mobileParameters, task } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<TaskCard> = {
    component: TaskCard,
    argTypes: {},
    args: {
        task,
    },
    parameters: {
        layout: "fullscreen",
    },
};
export default meta;

type Story = StoryObj<TaskCard>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
