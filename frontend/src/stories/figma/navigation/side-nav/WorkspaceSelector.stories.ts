// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
import {
    workspace,
    mobileParameters,
    makeStorybookSelect,
} from "$lib/storybook";
import type { Workspace } from "$lib/types/workspace";

const meta: Meta<WorkspaceSelector> = {
    component: WorkspaceSelector,
    argTypes: {
        workspace: makeStorybookSelect<Workspace | undefined>({
            "Workspace": workspace,
            "No workspace": undefined,
        }),
        workspaces: makeStorybookSelect<Workspace[] | undefined>({
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
