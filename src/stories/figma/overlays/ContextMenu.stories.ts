import type { Meta, StoryObj } from "@storybook/svelte";

import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";

import type { ContextMenuType } from "$lib/types/ui";
import {
    task,
    workspace,
    workspaceBoard,
    workspaceBoardSection,
    workspaceUserSearchModule,
    labelSearchModule,
    moveTaskModule,
} from "$lib/storybook";

const contextMenus: Record<string, ContextMenuType> = {
    profile: {
        kind: "profile" as const,
    },
    workspace: {
        kind: "workspace" as const,
    },
    sideNav: {
        kind: "sideNav" as const,
        workspace,
    },
    workspaceBoard: {
        kind: "workspaceBoard" as const,
        workspaceBoard,
    },
    workspaceBoardSection: {
        kind: "workspaceBoardSection" as const,
        workspaceBoard,
        workspaceBoardSection,
    },
    taskDashboard: {
        kind: "task" as const,
        task,
        location: "dashboard",
        moveTaskModule,
    },
    task: {
        kind: "task" as const,
        task,
        location: "task",
        moveTaskModule,
    },
    help: {
        kind: "help",
    },
    permissions: {
        kind: "permissions",
    },
    updateMember: {
        kind: "updateMember",
        workspaceUserSearchModule,
    },
    updateLabel: {
        kind: "updateLabel",
        labelSearchModule,
    },
};

const meta: Meta<ContextMenu> = {
    component: ContextMenu,
    argTypes: {},
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
