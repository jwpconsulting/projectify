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
import type { LabelAssignment, TeamMemberAssignment } from "$lib/types/stores";
import type { TeamMemberSelectionInput } from "$lib/types/ui";
import type { CurrentUser, User } from "$lib/types/user";
import type {
    Label,
    SectionDetail,
    SubTask,
    ProjectDetail,
    WorkspaceDetail,
    WorkspaceQuota,
    TaskDetail,
    ProjectDetailTask,
    ProjectDetailSection,
    WorkspaceDetailTeamMember,
    WorkspaceDetailProject,
} from "$lib/types/workspace";
import { getIndexFromLabelColor, labelColors } from "$lib/utils/colors";
import type { LabelColor } from "$lib/utils/colors";

import type { Customer } from "$lib/types/corporate";

export const user1: CurrentUser & User & { kind: "authenticated" } = {
    email: "this-email-is-very-long-so-you-know-we-mean@business.com",
    preferred_name: null,
    profile_picture: null,
    kind: "authenticated" as const,
};
export const user2: CurrentUser & User = {
    email: "john@example.com",
    preferred_name: null,
    profile_picture: null,
    kind: "authenticated" as const,
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

export const teamMember: WorkspaceDetailTeamMember = {
    user: user1,
    uuid: nullUuid,
    role: "OWNER",
    job_title: null,
};

export const teamMemberSelectionInputs: TeamMemberSelectionInput[] = [
    { kind: "unassigned" },
    { kind: "allTeamMembers" },
    { kind: "teamMember", teamMember },
];

export const project: WorkspaceDetailProject = {
    uuid: nullUuid,
    title: "Project with a long name, it is long",
    description: null,
    archived: null,
};

const quota: WorkspaceQuota = {
    workspace_status: "full",
    chat_messages: { current: null, limit: null, can_create_more: false },
    labels: { current: null, limit: null, can_create_more: false },
    sub_tasks: { current: null, limit: null, can_create_more: false },
    tasks: { current: null, limit: null, can_create_more: false },
    task_labels: { current: null, limit: null, can_create_more: false },
    projects: { current: null, limit: null, can_create_more: false },
    sections: { current: null, limit: null, can_create_more: false },
    team_members_and_invites: {
        current: null,
        limit: null,
        can_create_more: false,
    },
};

export const workspace: WorkspaceDetail = {
    uuid: nullUuid,
    title: "This is a workspace, the title is veeeeeryyy loooong",
    description: null,
    picture: null,
    projects: [project],
    team_members: [teamMember],
    team_member_invites: [],
    labels: [],
    quota,
};

export const projectDetail: ProjectDetail = {
    uuid: nullUuid,
    sections: [],
    workspace,
    title: "Project with a long name, it is long",
    description: null,
    archived: null,
};

export const customer: Customer = {
    seats: 120899182918201,
    uuid: "not-a-real-uuid",
    subscription_status: "ACTIVE",
};

export const trialCustomer: Customer = {
    seats: 120899182918201,
    uuid: "not-a-real-uuid",
    subscription_status: "UNPAID",
};

export const customCustomer: Customer = {
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
    _order: 0,
};

export const section: TaskDetail["section"] = {
    title: "section name that is very very very very very very long",
    description: null,
    uuid: nullUuid,
    project: { ...projectDetail, due_date: null },
    _order: 0,
};

export const sectionDetail: SectionDetail = {
    ...section,
    tasks: [],
    created: "",
    modified: "",
};

export const task: TaskDetail = {
    title: "This task has a very long name, yes, it's long, and as you know that will tell us whether we have overflow problems or not.",
    description: null,
    uuid: nullUuid,
    due_date: "2022-08-01",
    number: 1,
    created: "",
    modified: "",
    _order: 0,
    labels: [...mappedLabels, ...mappedLabels],
    assignee: teamMember,
    sub_tasks: [subTask],
    section,
    chat_messages: [],
};

export const projectDetailSection: ProjectDetailSection = {
    _order: 0,
    tasks: [],
    title: "A second task, worthy of being a task, and having a wordy title",
    description: null,
    uuid: nullUuid,
};

export const projectDetailTask: ProjectDetailTask = {
    title: "A second task, worthy of being a task, and having a wordy title",
    description: null,
    uuid: nullUuid,
    due_date: "2022-08-01",
    number: 1337,
    labels: mappedLabels.slice(4),
    assignee: teamMember,
    sub_task_progress: 1,
};

export const mobileParameters = {
    viewport: {
        defaultViewport: "iphonese2",
    },
};

const noop = console.error.bind(null, "noop");

export const teamMemberAssignment: TeamMemberAssignment = {
    select: noop,
    deselect: noop,
    subscribe: readable<WorkspaceDetailTeamMember | null>(null).subscribe,
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
