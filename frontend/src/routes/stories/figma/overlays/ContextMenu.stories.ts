// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK

import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";
import { makeStorybookSelect } from "$lib-stories/storybook";
import type { Meta, StoryObj } from "@storybook/svelte";

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

export const Project: Story = {
    args: {
        target: "project",
    },
};

export const Section: Story = {
    args: {
        target: "section",
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

export const UpdateTeamMember: Story = {
    args: {
        target: "update-team-member",
    },
};

export const UpdateLabel: Story = {
    args: {
        target: "update-label",
    },
};
