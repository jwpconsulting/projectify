import { readable, writable } from "svelte/store";

import type { Customer } from "./types/corporate";

import type { LabelLabel, SelectLabel } from "$lib/figma/types";
import type {
    CreateTaskModule,
    LabelAssignment,
    MoveTaskModule,
    TaskModule,
    WorkspaceUserAssignment,
} from "$lib/types/stores";
import type {
    BreadCrumbWorkspaceBoardSection,
    WorkspaceUserSelectionInput,
} from "$lib/types/ui";
import type { User } from "$lib/types/user";
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

export const fr = "flex flex-row flex-wrap gap-2";
export const fc = "flex flex-col flex-wrap gap-2";
export const trueFalse = [true, false];
export const falseTrue = [false, true];

export const user1: User = {
    email: "this-email-is-very-long-so-you-know-we-mean-business@example.com",
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

export const customer: Customer = {
    seats_remaining: 18923,
    seats: 120899182918201,
    uuid: "not-a-real-uuid",
    subscription_status: "I SHOULD HAVE VALIDATION",
};

export const subTask: SubTask = {
    title: "Do the thing",
    description: "Description should not be shown",
    created: "",
    modified: "",
    uuid: "does-not-exist",
    done: false,
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

const newTask: NewTask = {
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

export const breadCrumbWorkspaceBoardSection: BreadCrumbWorkspaceBoardSection =
    {
        title: "section name that is long",
        created: "",
        modified: "",
        uuid: "does-not-exist",
        tasks: [task, task2],
        _order: 0,
        workspace_board: workspaceBoard,
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

export const workspaceUserAssignment: WorkspaceUserAssignment = {
    select: noop,
    deselect: noop,
    selected: writable({ kind: "allWorkspaceUsers" }),
};

export const labelAssignment: LabelAssignment = {
    select: noop,
    deselect: noop,
    selected: readable({ kind: "noLabel" }),
    evaluate: async () => {
        await new Promise(console.log);
        return [];
    },
};

export const createTaskModule: CreateTaskModule = {
    newTask,
    createTask: writable<Partial<CreateTask>>({}),
    canCreateOrUpdate: readable(false),
    createOrUpdateTask() {
        console.log("Called createOrUpdateTask");
    },
    workspaceUserAssignment,
    labelAssignment,
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
    workspaceUserAssignment,
    labelAssignment,
};

export const moveTaskModule: MoveTaskModule = {
    moveToBottom: noopAsync,
    moveToTop: noopAsync,
    moveToWorkspaceBoardSection: noopAsync,
};

type ArgTypeOption<T> = Record<string, T>;

interface ArgType<T> {
    options: string[];
    mapping: Record<string, T>;
    control: {
        type: "radio";
        labels: Record<string, string>;
    };
}

function slugify(t: string): string {
    // https://stackoverflow.com/a/1054862
    return t
        .toLowerCase()
        .replace(/ /g, "-")
        .replace(/[^\w-]+/g, "");
}

export function makeStorybookSelect<T>(choices: ArgTypeOption<T>): ArgType<T> {
    const labels = Object.fromEntries(
        Object.entries(choices).map(([k, _v]) => [slugify(k), k])
    );
    const options = Object.keys(labels);
    const mapping = Object.fromEntries(
        Object.entries(choices).map(([k, v]) => [slugify(k), v])
    );
    return {
        options,
        mapping,
        control: {
            type: "radio",
            labels,
        },
    };
}
