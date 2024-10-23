// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Collapsed from "$lib/figma/navigation/side-nav/Collapsed.svelte";
import { workspace } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Collapsed> = {
    component: Collapsed,
    args: {
        workspace,
        workspaces: [workspace],
    },
};
export default meta;

type Story = StoryObj<Collapsed>;

export const Default: Story = {};
