import {
    task,
    workspace,
    workspaceBoard,
    workspaceBoardSection,
    workspaceUserFilter,
    workspaceUser,
    labelSearchModule,
    makeStorybookSelect,
    moveTaskModule,
} from "$lib/storybook";

import type { ContextMenuType } from "$lib/types/ui";

// Initiating lateral export in 3... 2... 1...
// Reticulating splines...
// Counting backwards from infinity...
export const contextMenus: Record<string, ContextMenuType> = {
    "Profile": {
        kind: "profile" as const,
    },
    "Workspace": {
        kind: "workspace" as const,
        workspaces: [workspace],
    },
    "Side nav": {
        kind: "sideNav" as const,
        workspace,
    },
    "Workspace board": {
        kind: "workspaceBoard" as const,
        workspaceBoard,
    },
    "Workspace board section": {
        kind: "workspaceBoardSection" as const,
        workspaceBoard,
        workspaceBoardSection,
    },
    "Task dashboard": {
        kind: "task" as const,
        task,
        location: "dashboard",
        moveTaskModule,
        workspaceBoardSection,
    },
    "Task": {
        kind: "task" as const,
        task,
        location: "task",
        moveTaskModule,
        workspaceBoardSection,
    },
    "Help": {
        kind: "help",
    },
    "Permissions": {
        kind: "permissions",
    },
    "Update member": {
        kind: "updateMember",
        workspaceUserFilter,
    },
    "Update label": {
        kind: "updateLabel",
        labelSearchModule,
    },
};
// Have a nice day!

export const destructiveOverlays = makeStorybookSelect({
    "Delete label": {
        kind: "deleteLabel" as const,
        label: { name: "This is a label", color: 0, uuid: "" },
    },
    "Delete member": {
        kind: "deleteMember" as const,
        workspaceUser,
    },
    "Delete section": {
        kind: "deleteSection" as const,
        workspaceBoardSection,
    },
    "Delete task": {
        kind: "deleteTask" as const,
        task,
    },
    "Delete selected tasks": {
        kind: "deleteSelectedTasks" as const,
        tasks: [task],
    },
    "Archive board": {
        kind: "archiveBoard" as const,
        workspaceBoard: {
            title: "board name",
            created: "",
            modified: "",
            uuid: "",
        },
    },
    "Delete board": {
        kind: "deleteBoard" as const,
        workspaceBoard,
    },
});

export const constructiveOverlays = makeStorybookSelect({
    "Update workspace board": { kind: "updateWorkspaceBoard", workspaceBoard },
    "Create workspace board": { kind: "createWorkspaceBoard", workspace },
    "Invite team members": { kind: "inviteTeamMembers", workspace },
    "Invite team members (no seats left)": {
        kind: "inviteTeamMembersNoSeatsLeft",
        workspace,
    },
    "Create workspace board section": {
        kind: "createWorkspaceBoardSection",
        workspaceBoard,
    },
    "Create workspace": { kind: "createWorkspace" },
    "Skip onboarding": { kind: "skipOnboarding" },
    "Recover workspace board": {
        kind: "recoverWorkspaceBoard",
        workspaceBoard,
    },
});
