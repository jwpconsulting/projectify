import { Plus } from "@steeze-ui/heroicons";
import type { User } from "$lib/types/user";
import type { WorkspaceUserSelectionInput } from "$lib/types/ui";
import type {
    Label,
    WorkspaceUser,
    SubTask,
    WorkspaceBoard,
    WorkspaceBoardSection,
    Task,
} from "$lib/types/workspace";
import { labelColors, getIndexFromLabelColor } from "$lib/utils/colors";
import type { LabelColor } from "$lib/utils/colors";
import type { ButtonStyle, LabelLabel, SelectLabel } from "$lib/figma/types";
import { writable, readable } from "svelte/store";
import type {
    WorkspaceSearchModule,
    WorkspaceBoardSearchModule,
    WorkspaceUserSearchModule,
    LabelSearchModule,
} from "$lib/types/stores";

export const fr = "flex flex-row flex-wrap gap-2";
export const fc = "flex flex-col flex-wrap gap-2";
export const trueFalse = [true, false];
export const falseTrue = [false, true];

export const buttonStyles: ButtonStyle[] = [
    { kind: "primary" },
    { kind: "secondary" },
    { kind: "tertiary", icon: { position: "left", icon: Plus } },
    { kind: "tertiary", icon: { position: "right", icon: Plus } },
    { kind: "tertiary", icon: null },
];

export const user1: User = {
    email: "hello@example.com",
    full_name: undefined,
    profile_picture: undefined,
};
export const user2: User = {
    email: "john@example.com",
    full_name: undefined,
    profile_picture: undefined,
};
export const users = [user1, user2, null];

export const mappedLabels: Label[] = labelColors.map(
    (labelColor: LabelColor) => {
        return {
            name: labelColor,
            color: getIndexFromLabelColor(labelColor),
            uuid: `does-not-exist-${labelColor}`,
        };
    }
);

export const labels: LabelLabel[] = [
    ...mappedLabels.map((label: Label) => {
        return {
            kind: "label" as const,
            label,
        };
    }),
    { kind: "applyLabel" },
];
export const selectLabels: SelectLabel[] = [
    ...mappedLabels.map((label: Label) => {
        return {
            kind: "label" as const,
            label,
        };
    }),
    { kind: "allLabels" },
    { kind: "noLabel" },
];

export const workspaceUser: WorkspaceUser = {
    user: user1,
    uuid: "does-not-exist",
    role: "OWNER",
    created: "",
    modified: "",
};

export const workspaceUserSelectionInputs: WorkspaceUserSelectionInput[] = [
    { kind: "unassigned" },
    { kind: "allWorkspaceUsers" },
    { kind: "workspaceUser", workspaceUser },
];

export const workspaceBoard: WorkspaceBoard = {
    uuid: "does-not-exist",
    title: "Project board",
    created: "",
    modified: "",
};

export const workspace = {
    uuid: "does-not-exist",
    title: "This is a workspace",
    created: "",
    modified: "",
    workspace_boards: [workspaceBoard],
    workspace_users: [workspaceUser],
};

export const subTask: SubTask = {
    title: "Do the thing",
    description: "Description should not be shown",
    created: "",
    modified: "",
    uuid: "does-not-exist",
    done: true,
    order: 0,
};

export const task: Task = {
    title: "task name",
    created: "",
    modified: "",
    uuid: "does-not-exist",
    deadline: "2022-08-01",
    _order: 0,
    number: 1,
    labels: [],
    assignee: workspaceUser,
    sub_tasks: [subTask],
};

export const workspaceBoardSection: WorkspaceBoardSection = {
    title: "section name that is long",
    created: "",
    modified: "",
    uuid: "does-not-exist",
    tasks: [task],
    _order: 0,
};

export const mobileParameters = {
    viewport: {
        defaultViewport: "iphonese2",
    },
};

export const workspaceSearchModule: WorkspaceSearchModule = {
    workspaces: readable([workspace]),
    currentWorkspace: readable(workspace),
};

export const workspaceBoardSearchModule: WorkspaceBoardSearchModule = {
    currentWorkspace: readable(workspace),
    currentWorkspaceBoard: readable(workspaceBoard),
    currentWorkspaceBoardUuid: readable("this-does-not-exist"),
};

const noop = () => {};

export const workspaceUserSearchModule: WorkspaceUserSearchModule = {
    select: noop,
    deselect: noop,
    selected: writable({ kind: "allWorkspaceUsers" }),
    tasksPerUser: readable({ unassigned: 0, assigned: new Map() }),
    search: writable(""),
    searchResults: readable([workspaceUser]),
};

export const labelSearchModule: LabelSearchModule = {
    select: noop,
    deselect: noop,
    selected: writable({ kind: "allLabels" }),
    search: writable(""),
    searchResults: readable(mappedLabels),
};
