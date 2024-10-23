// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import Workspace from "$lib/figma/overlays/context-menu/Workspace.svelte";
import { workspace } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<Workspace> = {
    component: Workspace,
    argTypes: {},
    args: { workspaces: [workspace] },
};
export default meta;

type Story = StoryObj<Workspace>;

export const Default: Story = {};
