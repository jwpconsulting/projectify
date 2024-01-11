// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023, 2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { readable, writable } from "svelte/store";

import type { LabelLabel, SelectLabel } from "$lib/figma/types";
import type {
    LabelAssignment,
    WorkspaceUserAssignment,
} from "$lib/types/stores";
import type { WorkspaceUserSelectionInput } from "$lib/types/ui";
import type { User } from "$lib/types/user";
import type {
    Label,
    SubTask,
    Task,
    TaskWithWorkspaceBoardSection,
    WorkspaceBoard,
    WorkspaceBoardSectionWithTasks,
    WorkspaceUser,
} from "$lib/types/workspace";
import { getIndexFromLabelColor, labelColors } from "$lib/utils/colors";
import type { LabelColor } from "$lib/utils/colors";

import type { Customer } from "./types/corporate";

export const user1: User = {
    email: "this-email-is-very-long-so-you-know-we-mean-business@example.com",
    full_name: null,
    profile_picture: null,
};
export const user2: User = {
    email: "john@example.com",
    full_name: null,
    profile_picture: null,
};

const nullUuid = "00000000-0000-0000-0000-000000000000";

export const mappedLabels: Label[] = labelColors.map(
    (labelColor: LabelColor) => {
        return {
            name: labelColor,
            color: getIndexFromLabelColor(labelColor),
            uuid: nullUuid,
        };
    },
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
    uuid: nullUuid,
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
    uuid: nullUuid,
    title: "Project board with a long name, it is long",
    created: "",
    modified: "",
};

export const workspace = {
    uuid: nullUuid,
    title: "This is a workspace, the title is veeeeeryyy loooong",
    created: "",
    modified: "",
    picture: null,
    workspace_boards: [workspaceBoard],
    workspace_users: [workspaceUser],
};

export const customer: Customer = {
    seats_remaining: 18923,
    seats: 120899182918201,
    uuid: "not-a-real-uuid",
    subscription_status: "ACTIVE",
};

export const trialCustomer: Customer = {
    seats_remaining: 18923,
    seats: 120899182918201,
    uuid: "not-a-real-uuid",
    subscription_status: "UNPAID",
};

export const customCustomer: Customer = {
    seats_remaining: 18923,
    seats: 120899182918201,
    uuid: "not-a-real-uuid",
    subscription_status: "CUSTOM",
};

export const subTask: SubTask = {
    title: "Do the thing",
    description: "Description should not be shown",
    created: "",
    modified: "",
    uuid: nullUuid,
    done: false,
    order: 0,
};

export const task: TaskWithWorkspaceBoardSection = {
    title: "This task has a very long name, yes, it's long, and as you know that will tell us whether we have overflow problems or not.",
    created: "",
    modified: "",
    uuid: nullUuid,
    deadline: "2022-08-01",
    _order: 0,
    number: 1,
    labels: [...mappedLabels, ...mappedLabels],
    assignee: workspaceUser,
    sub_tasks: [subTask],
    workspace_board_section: {
        title: "section name that is long",
        created: "",
        modified: "",
        uuid: nullUuid,
        _order: 0,
        workspace_board: {
            uuid: nullUuid,
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
    uuid: nullUuid,
    deadline: "2022-08-01",
    _order: 0,
    number: 1337,
    labels: mappedLabels.slice(4),
    assignee: workspaceUser,
    sub_tasks: [],
};

export const workspaceBoardSection: WorkspaceBoardSectionWithTasks = {
    title: "section name that is very very very very very very long",
    created: "",
    modified: "",
    uuid: nullUuid,
    tasks: [task, task2],
    _order: 0,
};

export const mobileParameters = {
    viewport: {
        defaultViewport: "iphonese2",
    },
};

const noop = console.error.bind(null, "noop");

export const workspaceUserAssignment: WorkspaceUserAssignment = {
    select: noop,
    deselect: noop,
    subscribe: readable<WorkspaceUser | undefined>(undefined).subscribe,
    selected: writable({ kind: "unassigned" }),
};

export const labelAssignment: LabelAssignment = {
    select: noop,
    deselect: noop,
    selected: readable({ kind: "noLabel" }),
    subscribe: readable<Label[]>([]).subscribe,
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
        Object.entries(choices).map(([k, _v]) => [slugify(k), k]),
    );
    const options = Object.keys(labels);
    const mapping = Object.fromEntries(
        Object.entries(choices).map(([k, v]) => [slugify(k), v]),
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
