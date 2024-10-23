// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Chevrons from "$lib/figma/cards/task-card/Chevrons.svelte";
import { task } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Chevrons> = {
    component: Chevrons,
    argTypes: {},
};
export default meta;

type Story = StoryObj<Chevrons>;

export const Default: Story = {
    args: {
        task,
    },
};
