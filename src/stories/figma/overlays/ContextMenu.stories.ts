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
        target: contextMenus.profile,
    },
};

export const Workspace: Story = {
    args: {
        target: contextMenus.workspace,
    },
};

export const SideNav: Story = {
    args: {
        target: contextMenus.sideNav,
    },
};

export const WorkspaceBoard: Story = {
    args: {
        target: contextMenus.workspaceBoard,
    },
};

export const WorkspaceBoardSection: Story = {
    args: {
        target: contextMenus.workspaceBoardSection,
    },
};

export const TaskDashboard: Story = {
    args: {
        target: contextMenus.taskDashboard,
    },
};

export const Task: Story = {
    args: {
        target: contextMenus.task,
    },
};

export const Help: Story = {
    args: {
        target: contextMenus.help,
    },
};

export const Permissions: Story = {
    args: {
        target: contextMenus.permissions,
    },
};

export const UpdateMember: Story = {
    args: {
        target: contextMenus.updateMember,
    },
};

export const UpdateLabel: Story = {
    args: {
        target: contextMenus.updateLabel,
    },
};
