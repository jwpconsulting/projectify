import {
    task,
    workspace,
    workspaceBoard,
    workspaceBoardSection,
    workspaceUserSearchModule,
    labelSearchModule,
    moveTaskModule,
} from "$lib/storybook";

import type { ContextMenuType } from "$lib/types/ui";

// Initiating lateral export in 3... 2... 1...
// Reticulating splines...
// Counting backwards from infinity...
export const contextMenus: Record<string, ContextMenuType> = {
    profile: {
        kind: "profile" as const,
    },
    workspace: {
        kind: "workspace" as const,
        workspaces: [workspace],
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
        workspaceBoardSection,
    },
    task: {
        kind: "task" as const,
        task,
        location: "task",
        moveTaskModule,
        workspaceBoardSection,
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
// Have a nice day!
