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

import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";
import { makeStorybookSelect } from "$lib/storybook";

import { contextMenus } from "./config";

const meta: Meta<ContextMenu> = {
    component: ContextMenu,
    argTypes: {
        target: makeStorybookSelect(contextMenus),
    },
};
export default meta;

type Story = StoryObj<ContextMenu>;

export const Profile: Story = {
    args: {
        target: "profile",
    },
};

export const Workspace: Story = {
    args: {
        target: "workspace",
    },
};

export const SideNav: Story = {
    args: {
        target: "side-nav",
    },
};

export const WorkspaceBoard: Story = {
    args: {
        target: "workspace-board",
    },
};

export const WorkspaceBoardSection: Story = {
    args: {
        target: "workspace-board-section",
    },
};

export const TaskDashboard: Story = {
    args: {
        target: "task-dashboard",
    },
};

export const Task: Story = {
    args: {
        target: "task",
    },
};

export const Help: Story = {
    args: {
        target: "help",
    },
};

export const Permissions: Story = {
    args: {
        target: "permissions",
    },
};

export const UpdateWorkspaceUser: Story = {
    args: {
        target: "update-workspace-user",
    },
};

export const UpdateLabel: Story = {
    args: {
        target: "update-label",
    },
};
