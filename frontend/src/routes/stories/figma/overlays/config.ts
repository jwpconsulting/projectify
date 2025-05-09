// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import {
    task,
    workspace,
    project,
    section,
    teamMemberAssignment,
    teamMember,
    labelAssignment,
    makeStorybookSelect,
    projectDetail,
    projectDetailTask,
    projectDetailSection,
} from "$lib-stories/storybook";
import type { ConstructiveOverlayType, ContextMenuType } from "$lib/types/ui";

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
    "Project": {
        kind: "project" as const,
        workspace,
        project,
    },
    "Section": {
        kind: "section" as const,
        project: projectDetail,
        section: projectDetailSection,
    },
    "Task": {
        kind: "task" as const,
        task,
        location: "task",
    },
    "Task search": {
        kind: "task" as const,
        task: projectDetailTask,
        location: "dashboardSearch",
        project: projectDetail,
    },
    "Task dashboard": {
        kind: "task" as const,
        task: projectDetailTask,
        location: "dashboard",
        section: projectDetailSection,
        project: {
            ...project,
            archived: "",
            description: "",
            sections: [],
            workspace,
        },
    },
    // TODO name of component / kind should be update team member assignment?
    // TODO yep, I agree even one month later. Justus 2023-10-19
    "Update team member": {
        kind: "updateTeamMember",
        teamMemberAssignment,
    },
    "Update label": {
        kind: "updateLabel",
        labelAssignment,
    },
};
// Have a nice day!

export const destructiveOverlays = makeStorybookSelect({
    "Delete label": {
        kind: "deleteLabel" as const,
        label: {
            // XSS canary, not that we would ever forget to sanitize our
            // strings, hehehe.
            name: "<marquee>https://owasp.org/www-community/attacks/xss/</marquee>",
            color: 0,
            uuid: "",
        },
    },
    "Delete team member": {
        kind: "deleteTeamMember" as const,
        teamMember,
    },
    "Delete section": {
        kind: "deleteSection" as const,
        section,
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
        kind: "archiveProject" as const,
        project: {
            title: "veryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryveryvery long word",
            created: "",
            modified: "",
            uuid: "",
        },
    },
    "Delete board": {
        kind: "deleteProject" as const,
        project,
    },
});

export const constructiveOverlays =
    makeStorybookSelect<ConstructiveOverlayType>({
        "Update project": {
            kind: "updateProject",
            project,
        },
        "Create project": { kind: "createProject", workspace },
        "Create section": {
            kind: "createSection",
            project: projectDetail,
        },
        "Update section": {
            kind: "updateSection",
            section: projectDetailSection,
        },
        "Recover project": {
            kind: "recoverProject",
            project,
        },
    });
