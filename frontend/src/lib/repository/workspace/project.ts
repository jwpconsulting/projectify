// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
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
import {
    deleteWithCredentialsJson,
    failOrOk,
    getWithCredentialsJson,
    handle404,
    postWithCredentialsJson,
    putWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    ArchivedProject,
    Workspace,
    Project,
    ProjectDetail,
} from "$lib/types/workspace";

import type { ApiResponse } from "../types";

// Project CRUD
// Create
export async function createProject(
    workspace: Workspace,
    project: Pick<Project, "title" | "description">,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<Project, unknown>> {
    const { uuid: workspace_uuid } = workspace;
    const response = await postWithCredentialsJson<Project>(
        `/workspace/project/`,
        { ...project, workspace_uuid },
        repositoryContext,
    );
    return response;
}

// Read
export async function getProject(
    uuid: string,
    repositoryContext: RepositoryContext,
): Promise<ProjectDetail | undefined> {
    return handle404(
        await getWithCredentialsJson<ProjectDetail>(
            `/workspace/project/${uuid}`,
            repositoryContext,
        ),
    );
}

export async function getArchivedProjects(
    workspace_uuid: string,
    repositoryContext: RepositoryContext,
): Promise<undefined | ArchivedProject[]> {
    return handle404(
        await getWithCredentialsJson<ArchivedProject[]>(
            `/workspace/workspace/${workspace_uuid}/archived-projects/`,
            repositoryContext,
        ),
    );
}

// Update
export async function updateProject(
    project: Pick<Project, "title" | "description" | "uuid">,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, unknown>> {
    return await putWithCredentialsJson(
        `/workspace/project/${project.uuid}`,
        project,
        repositoryContext,
    );
}
// Delete
export async function deleteProject(
    { uuid }: Project,
    repositoryContext: RepositoryContext,
): Promise<void> {
    failOrOk(
        await deleteWithCredentialsJson(
            `/workspace/project/${uuid}`,
            repositoryContext,
        ),
    );
}

export async function archiveProject(
    { uuid }: Project,
    archived: boolean,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, unknown>> {
    return await postWithCredentialsJson(
        `/workspace/project/${uuid}/archive`,
        { archived },
        repositoryContext,
    );
}
