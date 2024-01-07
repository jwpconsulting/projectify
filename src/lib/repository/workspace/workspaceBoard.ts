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

// WorkspaceBoard CRUD
// Create
export async function createWorkspaceBoard(
    workspace: Workspace,
    workspaceBoard: { title: string; description: string; deadline?: string },
    repositoryContext: RepositoryContext,
): Promise<WorkspaceBoard> {
    const { title, description, deadline } = workspaceBoard;
    const { uuid: workspace_uuid } = workspace;
    const response = await postWithCredentialsJson<Workspace>(
        `/workspace/workspace-board/`,
        { workspace_uuid, title, description, deadline },
        repositoryContext,
    );
    if (response.kind !== "ok") {
        console.error("TODO handle", response);
        throw new Error("Error while creating workspace  board");
    }
    return response.data;
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
    workspaceBoard: Pick<
        WorkspaceBoard,
        "title" | "description" | "uuid" | "deadline"
    >,
    repositoryContext: RepositoryContext,
) {
    return failOrOk(
        await putWithCredentialsJson(
            `/workspace/workspace-board/${workspaceBoard.uuid}`,
            workspaceBoard,
            repositoryContext,
        ),
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
) {
    failOrOk(
        await postWithCredentialsJson(
            `/workspace/workspace-board/${uuid}/archive`,
            { archived },
            repositoryContext,
        ),
    );
}
