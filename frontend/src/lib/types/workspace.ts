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
import type { TimestampedType } from "$lib/types/base";
import type { User } from "$lib/types/user";
import type { components } from "./schema";

export type TeamMemberRole =
    | "OBSERVER"
    | "CONTRIBUTOR"
    | "MAINTAINER"
    | "OWNER";

export type TeamMember = {
    user: User;
    uuid: string;
    job_title: string | null;
    role: TeamMemberRole;
} & TimestampedType;

export type Label = components["schemas"]["LabelBase"];

export type SubTask = components["schemas"]["SubTaskBase"];

export type CreateUpdateSubTask = components["schemas"]["SubTaskCreateUpdate"];

type ChatMessage = {
    author: TeamMember;
    uuid: string;
    text: string;
} & TimestampedType;

// All the info we can receive from the API
export type Task = {
    title: string;
    description: string | null;
    _order: number;
    uuid: string;
    // TODO the following should be a Date
    due_date: string | null;
    number: number;
    labels: readonly Label[];
    assignee?: TeamMember;
    section?: Section;
    sub_tasks?: readonly SubTask[];
    chat_messages?: readonly ChatMessage[];
} & TimestampedType;

export type TaskDetail = components["schemas"]["TaskDetail"];

export type Section = TaskDetail["section"];

export type SectionDetail = components["schemas"]["SectionDetail"];

export type Project = components["schemas"]["ProjectBase"];
export type ProjectDetail = components["schemas"]["ProjectDetail"];
export type ProjectDetailSection = ProjectDetail["sections"][number];
export type ProjectDetailTask = ProjectDetailSection["tasks"][number];

export type SectionWithTasks = ProjectDetail["sections"][number];

// Only used for search results
export type TaskWithSection = SectionWithTasks["tasks"][number] & {
    section: Pick<Section, "uuid" | "title">;
};

export type Workspace = components["schemas"]["WorkspaceBase"];
export type WorkspaceDetail = components["schemas"]["WorkspaceDetail"];
export type WorkspaceDetailProject = WorkspaceDetail["projects"][number];

export type WorkspaceQuota = WorkspaceDetail["quota"];

export type Quota = components["schemas"]["SingleQuota"];
