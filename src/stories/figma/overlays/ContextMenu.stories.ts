import type { Meta, StoryObj } from "@storybook/svelte";

import { makeStorybookSelect } from "$lib/storybook";

import { contextMenus } from "./config";

import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";

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

export const UpdateMember: Story = {
    args: {
        target: "update-member",
    },
};

export const UpdateLabel: Story = {
    args: {
        target: "update-label",
    },
};
