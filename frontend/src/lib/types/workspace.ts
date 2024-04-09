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
import type { TimestampedType, TitleDescriptionType } from "$lib/types/base";
import type { User } from "$lib/types/user";

export type TeamMemberRole =
    | "OBSERVER"
    | "CONTRIBUTOR"
    | "MAINTAINER"
    | "OWNER";

export type TeamMember = {
    user: User;
    uuid: string;
    job_title?: string;
    role: TeamMemberRole;
} & TimestampedType;

export interface Label {
    name: string;
    color: number;
    uuid: string;
}

export type SubTask = {
    uuid: string;
    done: boolean;
    order: number;
} & TimestampedType &
    TitleDescriptionType;

export type CreateUpdateSubTask = {
    done: boolean;
    // This will only exist for a sub task that is already inside a task
    uuid?: string;
} & TitleDescriptionType;

type ChatMessage = {
    author: TeamMember;
    uuid: string;
    text: string;
} & TimestampedType;

// All the info we can receive from the API
export type Task = {
    _order: number;
    uuid: string;
    // TODO the following should be a Date
    due_date?: string;
    number: number;
    labels: Label[];
    assignee?: TeamMember;
    section?: Section;
    sub_tasks?: SubTask[];
    chat_messages?: ChatMessage[];
} & TimestampedType &
    TitleDescriptionType;

export type TaskWithSection = Task & {
    section: Section;
};

// TODO rename TaskDetail
export type TaskWithWorkspace = Task & {
    sub_tasks: SubTask[];
    section: Section & {
        project: Project & {
            workspace: Workspace;
        };
    };
};

export type CreateSection = TitleDescriptionType;

export type Section = {
    _order: number;
    uuid: string;
    tasks?: Task[];
    project?: Project;
} & TimestampedType &
    CreateSection;

export type SectionWithTasks = Pick<Section, "uuid" | "_order" | "title"> &
    Required<Pick<Section, "tasks">>;

export type SectionDetail = Section &
    Required<Pick<Section, "project" | "tasks">>;

export type Project = {
    due_date?: string;
    uuid: string;
    sections?: Section[];
    archived?: string;
    workspace?: Workspace;
} & TimestampedType &
    TitleDescriptionType;

export type ProjectDetail = Project & {
    workspace: Workspace;
    sections: SectionWithTasks[];
};

export type ArchivedProject = Project & { archived: string };

export interface Quota {
    current: number | null;
    limit: number | null;
    can_create_more: boolean;
}

export interface WorkspaceQuota {
    workspace_status: "full" | "trial" | "inactive";
    chat_messages: Quota;
    labels: Quota;
    sub_tasks: Quota;
    tasks: Quota;
    task_labels: Quota;
    projects: Quota;
    sections: Quota;
    team_members_and_invites: Quota;
}

interface TeamMemberInvite {
    email: string;
    created: string;
}

export type Workspace = {
    picture: string | null;
    team_members?: TeamMember[];
    team_member_invites?: TeamMemberInvite[];
    projects?: Project[];
    labels?: Label[];
    uuid: string;
    quota?: WorkspaceQuota;
} & TimestampedType &
    TitleDescriptionType;

export type WorkspaceDetail = Required<
    Pick<
        Workspace,
        | "projects"
        | "labels"
        | "team_members"
        | "quota"
        | "team_member_invites"
    >
> &
    Workspace;
