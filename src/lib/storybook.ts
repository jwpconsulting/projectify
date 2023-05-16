import { Plus } from "@steeze-ui/heroicons";
import { readable, writable } from "svelte/store";
import type { User } from "$lib/types/user";
import type { WorkspaceUserSelectionInput } from "$lib/types/ui";
import type {
    CreateTask,
    Label,
    NewTask,
    SubTask,
    Task,
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";
import { getIndexFromLabelColor, labelColors } from "$lib/utils/colors";
import type { LabelColor } from "$lib/utils/colors";
import type { ButtonStyle, LabelLabel, SelectLabel } from "$lib/figma/types";
import type {
    CreateTaskModule,
    LabelSearchModule,
    MoveTaskModule,
    SideNavModule,
    TaskModule,
    WorkspaceBoardSearchModule,
    WorkspaceBoardSectionModule,
    WorkspaceSearchModule,
    WorkspaceUserSearchModule,
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
    title: "Project board with a long name, it is long",
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
    workspace_board_section: {
        title: "section name that is long",
        created: "",
        modified: "",
        uuid: "does-not-exist",
        _order: 0,
        workspace_board: {
            uuid: "does-not-exist",
            title: "Project board with a long name, it is long",
            created: "",
            modified: "",
        },
    },
};

const task2: Task = {
    title: "A second task, worthy of being a task, and having a wordy title",
    created: "",
    modified: "",
    uuid: "does-not-exist-either",
    deadline: "2022-08-01",
    _order: 0,
    number: 1337,
    labels: mappedLabels.slice(4),
    assignee: workspaceUser,
    sub_tasks: [],
};

export const newTask: NewTask = {
    workspace_board_section: {
        title: "section name that is long",
        created: "",
        modified: "",
        uuid: "does-not-exist",
        _order: 0,
        workspace_board: {
            uuid: "does-not-exist",
            title: "Project board with a long name, it is long",
            created: "",
            modified: "",
        },
    },
};

export const workspaceBoardSection: WorkspaceBoardSection = {
    title: "section name that is long",
    created: "",
    modified: "",
    uuid: "does-not-exist",
    tasks: [task, task2],
    _order: 0,
};

export const mobileParameters = {
    viewport: {
        defaultViewport: "iphonese2",
    },
};

const noop = console.error.bind(null, "noop");

const noopAsync = async () => {
    await new Promise((resolve) => resolve(null));
    console.error("noopAsync");
};

export const workspaceSearchModule: WorkspaceSearchModule = {
    workspaces: readable([workspace]),
    currentWorkspace: readable(workspace),
    setWorkspaces: noopAsync,
};

export const workspaceBoardSearchModule: WorkspaceBoardSearchModule = {
    currentWorkspace: readable(workspace),
    currentWorkspaceBoard: readable(workspaceBoard),
    currentWorkspaceBoardUuid: readable("this-does-not-exist"),
};

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
    async createLabel(c: number, n: string) {
        await new Promise((resolve) => resolve(null));
        console.log("Creating label with color", c, "and name", n);
    },
};

export const sideNavModule: SideNavModule = {
    sideNavOpen: writable(true),
    toggleSideNavOpen: noop,
    showWorkspaceContextMenu: noop,
    showSideNavContextMenu: noop,
};

export const workspaceBoardSectionModule: WorkspaceBoardSectionModule = {
    workspaceBoardSectionClosed: writable(new Set()),
    toggleWorkspaceBoardSectionOpen: noop,
    switchWithPrevSection: noop,
    switchWithNextSection: noop,
};

export const createTaskModule: CreateTaskModule = {
    newTask,
    createTask: writable<Partial<CreateTask>>({}),
    canCreateOrUpdate: readable(false),
    createOrUpdateTask() {
        console.log("Called createOrUpdateTask");
    },
    workspaceUserSearchModule,
    labelSearchModule,
};

export const taskModule: TaskModule = {
    task,
    updateTask: writable<Partial<Task>>({}),
    canCreateOrUpdate: readable(false),
    createOrUpdateTask() {
        console.log("Updating this task");
    },
    showUpdateWorkspaceUser() {
        console.log("Showing workspace user context menu");
    },
    showUpdateLabel() {
        console.log("Showing label context menu");
    },
    workspaceUserSearchModule,
    labelSearchModule,
};

export const moveTaskModule: MoveTaskModule = {
    moveToBottom: noopAsync,
    moveToTop: noopAsync,
    moveToWorkspaceBoardSection: noopAsync,
};

export const createMoveTaskModule = (
    a: WorkspaceBoardSection,
    t: Task,
    ts: Task[]
): MoveTaskModule => {
    console.debug("Calling dummy createMoveTaskModule with", {
        a,
        t,
        ts,
    });
    return {
        moveToBottom: noopAsync,
        moveToTop: noopAsync,
        moveToWorkspaceBoardSection: noopAsync,
    };
};
