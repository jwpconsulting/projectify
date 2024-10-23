// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
import {
    workspace,
    mobileParameters,
    makeStorybookSelect,
} from "$lib-stories/storybook";
import type { UserWorkspace } from "$lib/types/workspace";
import type { Meta, StoryObj } from "@storybook/svelte";

const meta: Meta<WorkspaceSelector> = {
    component: WorkspaceSelector,
    argTypes: {
        workspace: makeStorybookSelect<UserWorkspace | undefined>({
            "Workspace": workspace,
            "No workspace": undefined,
        }),
        workspaces: makeStorybookSelect<UserWorkspace[] | undefined>({
            "Workspaces": [workspace],
            "No workspaces": undefined,
        }),
    },
    args: {
        workspace: "workspace",
        workspaces: "workspaces",
        open: true,
    },
    parameters: mobileParameters,
};
export default meta;

type Story = StoryObj<WorkspaceSelector>;

export const Open: Story = {};

export const Closed: Story = { args: { open: false } };
