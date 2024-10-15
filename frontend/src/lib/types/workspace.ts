// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK
import type { components } from "./schema";

export type TeamMemberRole = components["schemas"]["RoleEnum"];

export type Label = components["schemas"]["LabelBase"];

export type SubTask = components["schemas"]["SubTaskBase"];

export type CreateUpdateSubTask = components["schemas"]["SubTaskCreateUpdate"];

// All the info we can receive from the API
export type Task = components["schemas"]["TaskWithSubTask"];
export type TaskDetail = components["schemas"]["TaskDetail"];
export type TaskDetailAssignee = TaskDetail["assignee"] & object;

export type TaskDetailSection = TaskDetail["section"];

export type SectionDetail = components["schemas"]["SectionDetail"];

export type ArchivedProject = components["schemas"]["ArchivedProject"];
export type ProjectDetail = components["schemas"]["ProjectDetail"];
export type ProjectDetailWorkspace = ProjectDetail["workspace"];
export type ProjectDetailSection = ProjectDetail["sections"][number];
export type ProjectDetailTask = ProjectDetailSection["tasks"][number];
export type ProjectDetailAssignee = ProjectDetailTask["assignee"] & object;

// Only used for search results
export type TaskWithSection = ProjectDetailSection["tasks"][number] & {
    section: Pick<TaskDetailSection, "uuid" | "title">;
};

export type WorkspaceDetail = components["schemas"]["WorkspaceDetail"];
export type WorkspaceDetailProject = WorkspaceDetail["projects"][number];
export type WorkspaceDetailTeamMember =
    WorkspaceDetail["team_members"][number];

export type WorkspaceQuota = WorkspaceDetail["quota"];

export type Quota = components["schemas"]["SingleQuota"];

export type UserWorkspace = components["schemas"]["UserWorkspace"];
