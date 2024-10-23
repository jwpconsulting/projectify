// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Full from "$lib/figma/navigation/side-nav/Full.svelte";
import { workspace } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Full> = {
    component: Full,
    args: {
        workspace,
        workspaces: [workspace],
    },
};
export default meta;

type Story = StoryObj<Full>;

export const Default: Story = {};
