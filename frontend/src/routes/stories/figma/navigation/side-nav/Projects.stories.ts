// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK

import Boards from "$lib/figma/navigation/side-nav/Projects.svelte";
import { workspace } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Boards> = {
    component: Boards,
    args: {
        workspace,
    },
};
export default meta;

type Story = StoryObj<Boards>;

export const Default: Story = {};
