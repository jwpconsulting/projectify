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
    ArchivedWorkspaceBoard,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardDetail,
} from "$lib/types/workspace";

import type { ApiResponse } from "../types";

// WorkspaceBoard CRUD
// Create
export async function createWorkspaceBoard(
    workspace: Workspace,
    workspaceBoard: Pick<WorkspaceBoard, "title" | "description">,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<WorkspaceBoard, unknown>> {
    const { uuid: workspace_uuid } = workspace;
    const response = await postWithCredentialsJson<Workspace>(
        `/workspace/workspace-board/`,
        { ...workspaceBoard, workspace_uuid },
        repositoryContext,
    );
    return response;
}

// Read
export async function getWorkspaceBoard(
    uuid: string,
    repositoryContext: RepositoryContext,
): Promise<WorkspaceBoardDetail | undefined> {
    return handle404(
        await getWithCredentialsJson<WorkspaceBoardDetail>(
            `/workspace/workspace-board/${uuid}`,
            repositoryContext,
        ),
    );
}

export async function getArchivedWorkspaceBoards(
    workspace_uuid: string,
    repositoryContext: RepositoryContext,
): Promise<undefined | ArchivedWorkspaceBoard[]> {
    return handle404(
        await getWithCredentialsJson<ArchivedWorkspaceBoard[]>(
            `/workspace/workspace/${workspace_uuid}/archived-workspace-boards/`,
            repositoryContext,
        ),
    );
}

// Update
export async function updateWorkspaceBoard(
    workspaceBoard: Pick<WorkspaceBoard, "title" | "description" | "uuid">,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, unknown>> {
    return await putWithCredentialsJson(
        `/workspace/workspace-board/${workspaceBoard.uuid}`,
        workspaceBoard,
        repositoryContext,
    );
}
// Delete
export async function deleteWorkspaceBoard(
    { uuid }: WorkspaceBoard,
    repositoryContext: RepositoryContext,
): Promise<void> {
    failOrOk(
        await deleteWithCredentialsJson(
            `/workspace/workspace-board/${uuid}`,
            repositoryContext,
        ),
    );
}

export async function archiveWorkspaceBoard(
    { uuid }: WorkspaceBoard,
    archived: boolean,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, unknown>> {
    return await postWithCredentialsJson(
        `/workspace/workspace-board/${uuid}/archive`,
        { archived },
        repositoryContext,
    );
}
